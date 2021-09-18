import sqlite3
import json


con=sqlite3.connect("amazon.db")
cur = con.cursor()
f = open("Pet_Supplies_5.json")

create = """
create table petSupplies(
    row integer primary key autoincrement,
    user varchar(25) not null,
    rating decimal(2,1),
    itemID varchar(25) not null
)
"""
drop = "drop table petSupplies"

def insert(data):
    insert = """
    insert into petSupplies (user,rating,itemID) values
    {}
    """.format(",".join([str(i) for i in data]))
    return insert

load = []
cur.execute(drop)
cur.execute(create)
con.commit()
while True:
    # Get next line from file
    line = f.readline()
    try:
        j = json.loads(line)
        data = (j["reviewerID"],j["overall"],j["asin"])
        load.append(data)
    except:
        print("failed to read")
    if len(load) > 10000:
        print("load inserted")
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

# data = ((1,2,3),(1,2,3),(1,2,3))
# print(insert(data))