

def calcCorrelations(cur,item,threshold):
    small = f"""select itemID1,correlation,occurances from
    (select corr(rating1,rating2) correlation,itemID2,itemID1 from 
    ((select itemID as itemID2,user as user2,rating as rating2  from petSupplies where itemID = "{item}") 
    inner join  (select itemID itemID1,user as user1,rating as rating1 from petSupplies)
    on  user1 = user2) group by itemID1)  
    inner join (select itemID id, occurances from itemInfo where occurances > {threshold}) on itemID1=id order by correlation desc"""
    cur.execute(small)
    result = cur.fetchmany(1000)
    return result

def formatCorrelations(results):
    #currently in this order in calcCorrelations
    #itemID1,correlation,occurances
    j = {"items":[]}
    for result in results:
        j["items"].append({"Product ID":result[0],"Correlation":result[1],"Frequency":results[2]})
    return j



