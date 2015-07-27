import sqlite3
import json
import os

#remove old db
os.remove('departures.db')

conn = sqlite3.connect('departures.db')
c = conn.cursor()

#create table
c.execute("CREATE TABLE stations (id text, state text, deptime text)")

#read stations from file
text = open('station-led-mapping.json')
stations = json.loads(text.read())
for s in stations:
    c.execute("INSERT INTO stations VALUES ('%s', '000', '2014-02-21T00:00:00')" %s)

#save to db
conn.commit()
conn.close()
