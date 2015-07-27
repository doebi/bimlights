import sqlite3
import time
import bimapi
from threading import Thread
from datetime import datetime, timedelta

conn = sqlite3.connect('departures.db')

class UpdateThread(Thread):
    def __init__(self, sid):
        super(UpdateThread, self).__init__()
        self.sid = sid
        self.state = ""
        self.time = None

    def run(self):
        self.sid
        states = bimapi.getDepartures(self.sid)
        self.time = states['time']
        for i in ['1', '2', '3']:
            try:
                self.state += str(int(states[i]))
            except:
                self.state += '0'


def isTrainThere(state):
    for s in state:
        if s == "1":
            return True
    return False


def getStations(c):
    stations = []
    for row in c.execute("SELECT * FROM stations"):
        stations.append(row)
    return stations


def update():
    c = conn.cursor()

    stations = getStations(c)
    threads = []
    for row in stations:
        now = datetime.now()
        deptime = datetime.strptime(row[2], "%Y-%m-%dT%H:%M:%S")
        d = timedelta(minutes=-1)
        if deptime <= now or isTrainThere(row[1]):
            t = UpdateThread(row[0])
            threads.append(t)
            t.start()
            print("updating %s" %row[0])
    n = len(threads)
    while len(threads) > 0:
        for t in threads:
            if not t.is_alive():
                print("received " + t.sid + " with " + t.state + " at " + t.time)
                c.execute("UPDATE stations SET state = '%s', deptime = '%s' WHERE id = '%s'" %(t.state, t.time, t.sid))
                threads.remove(t)
    conn.commit()
    c.close()
    print("updated %d stations" %n)

while True:
    try:
        update()
        print("+++++++++++++++++++++++++++++++++++++++++++++++++")
    except:
        print("whoopsie");
    time.sleep(30)
