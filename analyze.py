import sqlite3

con=sqlite3.connect("amazon.db")
cur = con.cursor()

print(cur.execute("select itemID,count(*) c from petSupplies group by itemID order by c desc limit 5").fetchall())

