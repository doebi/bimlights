import urllib
import json
import numpy as np

position_url = "http://linz.faehrt.at/get_positions.php?bbox=13%2C47%2C15%2C49"

with open("station-led-mapping.json", "r") as f:
    stations = json.loads(f.read())

def distance(a, b):
    x = max(a[0], b[0]) - min(a[0], b[0])
    y = max(a[1], b[1]) - min(a[1], b[1])
    return float(np.sqrt(x**2 + y**2))

def getNextStation(f):
    m = 100
    for s in stations['stations']:
        s_loc = s['coordinates']
        f_loc = f['geometry']['coordinates']
        d = distance(s_loc, f_loc)
        if d < m:
            m = d
            n = s
    return n

def sumStates(a, b):
    c = ""
    for i in [0, 1, 2]:
        c += str(int(a[i]) or int(b[i]))
    return c

def buildData():
    r = urllib.urlopen(position_url)
    data = json.loads(r.read())
    led_data = ["000"]*50

    for f in data['features']:
        n = getNextStation(f)
        i = n['led']
        d = led_data[i]
        lfid = f['properties']['lfid']
        if lfid in [1, 2]:
            state = "100"
        elif lfid in [3, 4]:
            state = "010"
        elif lfid in [5, 6]:
            state = "001"
        else:
            state = "000"
        led_data[i] = sumStates(d, state)

    dump = ""
    for l in led_data:
        dump += l
    return dump
