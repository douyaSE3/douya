
import MySQLdb

conn1 = MySQLdb.connect(host='localhost', user='root',passwd='admin',db='test',charset='utf8')  
cursor1 = conn1.cursor()  
sql1 = "SELECT * FROM place"
cursor1.execute(sql1)
result1 = cursor1.fetchall()

conn2 = MySQLdb.connect(host='localhost', user='root',passwd='admin',db='douya',charset='utf8')  
cursor2 = conn2.cursor()  

for i in result1:
    sql2 = "INSERT INTO place_place (id,name,description) VALUES ("+str(i[0])+",'"+i[1].strip()+"','"+i[4]+"')"
    cursor2.execute(sql2)
conn2.commit()

for i in result1:
    try:
        if i[3]!='':       
            sql2 = "UPDATE place_place SET parent_id = "+str(i[3])+" WHERE id = "+str(i[0])
            cursor2.execute(sql2)
    except:
        pass

conn2.commit()