
#coding=utf-8
import MySQLdb

conn=MySQLdb.connect(host='localhost',user='root',passwd='admin',db='douya',charset='utf8')
cur=conn.cursor()
cur.execute('create table place_place_v2(id int not null primary key,Chinese_name longtext,English_name longtext,description longtext not null,parent_id int)')
sql="SELECT * FROM place_place"
cur.execute(sql)
res1=cur.fetchall()
for i in res1:
	if i[0]=='':
		break
	lastch=0
	k=0
	s0=i[1].strip()
	s0=s0.replace('&amp;AMP;','')
	s0=s0.replace('&amp;#039;','')
	s0=s0.replace('?','')
	for j in s0:
		if ord(j)>=0x4e00 and ord(j)<=0x9fa6:
			lastch=k
		k=k+1
	if lastch==0:
		chinese=""
		english=s0
	else:
		chinese=s0[0:lastch+1]
		english=s0[lastch+1:k]
	print i[0]
	cur.execute("INSERT INTO place_place_v2 (id,Chinese_name,English_name,description,parent_id) VALUES (%s,%s,%s,%s,%s)",(i[0],chinese,english,i[2],i[3]))
conn.commit()
cur.close()
conn.close()