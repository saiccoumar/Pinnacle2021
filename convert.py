import sqlite3
import json
import csv

#example call: convert("amazon.db","Movies_and_TV_5.json",("id","asin","overall"))
def convertJSON(db,inputFile,keys):
    con=sqlite3.connect(db)
    cur = con.cursor()
    f = open(inputFile)

    create = """
    create table if not exists itemRatings(
        row integer primary key autoincrement,
        user varchar(25) not null,
        rating decimal(2,1),
        itemID varchar(25) not null
    )
    """
    drop = "drop table if exists itemRatings"

    def insert(data):
        insert = """
        insert into itemRatings (user,rating,itemID) values
        {}
        """.format(",".join(tuple(str(i) for i in data)))
        #print(insert[:200])
        return insert

    load = []
    #possibly execute drop table here to reset tablespace
    cur.execute(drop)
    cur.execute(create)
    con.commit()
    line = f.readline()
    while line:
        # Get next line from file https://www.geeksforgeeks.org/read-a-file-line-by-line-in-python/
        line = f.readline()
        try:
            j = json.loads(line)
            data = []
            for key in keys:
                data.append(j[key])
            load.append(tuple(data))
        except:
            print("failed to read")
        if len(load) > 10000:
           # print("load inserted")
            cur.execute(insert(load))
            con.commit()
            load = []
        # if line is empty
        # end of file is reached
        if not line:
            break
        #print(line)
    if len(load):
        print("load inserted")
        cur.execute(insert(load))
        con.commit()
        load = []
    f.close()
    print("done")
    con.close()

def convertCSV(db,inputFile,keys): #keys are the indexes of each row you want to accept
    con=sqlite3.connect(db)
    cur = con.cursor()
    f = open(inputFile)

    create = """
    create table if not exists itemRatings(
        row integer primary key autoincrement,
        user varchar(25) not null,
        rating decimal(2,1),
        itemID varchar(25) not null
    )
    """
    drop = "drop table if exists itemRatings"

    def insert(data1):
        insert = """
        insert into itemRatings (user,rating,itemID) values
        {}
        """.format(",".join(tuple(str(i) for i in data1)))
        #print(insert[:200])
        return insert

    load = []
    #possibly execute drop table here to reset tablespace
    cur.execute(drop)
    cur.execute(create)
    con.commit()
    reader = csv.reader(f)
    headers = next(reader)
    data = []
    print(headers)
    
    for row in reader:
        load = [row[i] for i in keys]
        data.append(tuple(load))
        if len(data) > 1000000:
            print(load)
           # print("load inserted")
            cur.execute(insert(tuple(data)))
            con.commit()
            data = []
    cur.execute(insert(data))
    con.commit()
    con.close()



dbName = 'movies.db'
inputFile = 'Movies_and_TV_5.json'
# EXAMPLE CALL convert(dbName,inputFile,("reviewerID","overall","asin"))