import json
import sqlite3

database = sqlite3.connect(host="localhost",db="mysqlairport.db")
cur = database.cursor()
# cur.execute("CREATE TABLE airports(code text, latitude text, longitude text, name text, city text, state text, country text, woeid text, tz text, phone text, type text, email, text url text, runway_length text, elev text, icao text, direct_flights text, carriers text)")
sql = """CREATE TABLE AIRPORTS(code text, latitude text, longitude text, name text, 
		city text, state text, country text, woeid text, tz text, phone text, type text, 
		email, text url text, runway_length text, elev text, icao text, direct_flights text, carriers text)"""
cur.execute(sql)

with open('airports.json') as a:
	b = json.loads(a.read())
	for info in b:
		v_l = []
		v  = info.values()
		for i in v:
			v_l.append(i)
		sql = "INSERT INTO airports VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
		cur.execute(sql,(v_l[0], v_l[1], v_l[2], v_l[3], v_l[4], v_l[5], v_l[6], v_l[7], v_l[8], v_l[9], v_l[10], v_l[11], v_l[12], v_l[13], v_l[14], v_l[15], v_l[16], v_l[17]))
try:	
	database.commit()
except:
	database.rollback()

cur.close()
database.close()