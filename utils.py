import itertools

def calcCorrelations(cur,item,threshold):
    item = cur.execute(f"select itemID from itemInfo where name={item}").fetchone()
    small = f"""select name,correlation,occurances from
    (select corr(rating1,rating2) correlation,itemID2,itemID1 from 
    ((select itemID as itemID2,user as user2,rating as rating2  from itemRatings where itemID = "{item}") 
    inner join  (select itemID itemID1,user as user1,rating as rating1 from itemRatings)
    on  user1 = user2) group by itemID1)  
    inner join (select itemID id,name, occurances from itemInfo where occurances > {threshold}) on itemID1=id order by correlation desc"""
    cur.execute(small)
    result = cur.fetchmany(1000)
    return result

def autocomplete(con,string):
    con.create_collation("edits", collation(string).collate)
    if len(string)<8:
        titles = con.execute(f"select name from itemInfo where name like '%{string}%' order by name collate edits desc limit 5").fetchall()
    else:
        titles = con.execute(f"select name from itemInfo order by name collate edits desc limit 5").fetchall()
    print(titles[:5])
    titlesSingle = itertools.chain.from_iterable(titles)
    
    return {'data':list(titlesSingle)[:5]}


def editDistDP(str1, str2):
    m = len(str1)
    n = len(str2)
    # Create a table to store results of subproblems
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]
 
    # Fill d[][] in bottom up manner
    for i in range(m + 1):
        for j in range(n + 1):
 
            # If first string is empty, only option is to
            # insert all characters of second string
            if i == 0:
                dp[i][j] = j    # Min. operations = j
 
            # If second string is empty, only option is to
            # remove all characters of second string
            elif j == 0:
                dp[i][j] = i    # Min. operations = i
 
            # If last characters are same, ignore last char
            # and recur for remaining string
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
 
            # If last character are different, consider all
            # possibilities and find minimum
            else:
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert
                                   dp[i-1][j],        # Remove
                                   dp[i-1][j-1])    # Replace
 
    return dp[m][n]

class collation:
    def __init__(self,string):
        self.string = string

    def collate(self,str1,str2):
        str1Dist = editDistDP(str1,self.string)
        str2Dist = editDistDP(str2,self.string)
        if str1Dist < str2Dist:
            return 1
        elif str2Dist == str1Dist:
            return 0
        return -1

def formatCorrelations(results):
    #currently in this order in calcCorrelations
    #itemID1,correlation,occurances
    j = {"items":[]}
    for result in results:
        j["items"].append({"productID":result[0],"correlation":result[1],"frequency":result[2]})
    return j



