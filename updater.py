import sqlite3
import time
import bimapi
from datetime import datetime, timedelta

class Updater:
    def __init__(self):
        self.running = False
        self.conn = sqlite3.connect('departures.db')
        self.c = self.conn.cursor()

    def isRunning(self):
        return self.running

    def update(self):
        self.running = True
        stations = []
        for row in self.c.execute("SELECT * FROM stations"):
            stations.append(row)
        ns = len(stations)
        cs = 0

        for row in stations:
            now = datetime.now()
            deptime = datetime.strptime(row[2], "%Y-%m-%dT%H:%M:%S")
            #print 'mynow: ' + str(now)
            #print 'departure: ' + str(deptime)
            d = timedelta(minutes=-1)
            if deptime <= now:
                cs += 1
                stopID = row[0]
                #print ' + updating: ' + stopID
                states = bimapi.getDepartures(stopID)
                state = ""
                for i in ['1', '2', '3']:
                    try:
                        state += str(int(states[i]))
                    except:
                        state += '0'
                print(states['time'] + ": " + state)
                self.c.execute("UPDATE stations SET state = '%s', deptime = '%s' WHERE id = '%s'" %(state, states['time'], stopID))
                self.conn.commit()
            else:
                print ' - skipping: ' + row[0]
        self.running = False
        print("%d out of %d updated" %(cs, ns))
