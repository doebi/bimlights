# -*- coding: utf-8 -*
from datetime import datetime, timedelta
from lxml import etree
import time
import urllib

mindelta = timedelta(seconds=30)
url = "http://www.linzag.at/static/XML_DM_REQUEST"

def initSession(stopID):
    data = {
        "useRealtime": "1",
        "sessionID": "0",
        "type_dm": "stopID",
        "name_dm": stopID,
    }
    r = urllib.urlopen(url, urllib.urlencode(data))
    data = etree.fromstring(r.read())
    request = data[1]
    lines = request[3]
    sl = {
        '1': [],
        '2': [],
        '3': [],
    }
    for l in lines:
        number = l.get('number')
        index = l.get('index')
        if number in ['1', '2', '3']:
            sl[number].append(index)
    sid = data.get('sessionID')
    return (sid, sl)


def nextDeparture(sid, line):
    data = {
        "sessionID": sid,
        "requestID": "1",
        "itdDateTimeDepArr": "dep",
    }
    datastring = urllib.urlencode(data)
    for i in line:
        datastring += '&dmLineSelection=' + i

    r = urllib.urlopen(url, datastring)
    data = etree.fromstring(r.read())
    now = datetime.strptime(data.get('now'), "%Y-%m-%dT%H:%M:%S")
    #print 'real now: ' + str(now)
    #print time.strftime("%H:%M:%S", now)
    request = data[1]
    departures = request[-1]
    n = departures[0]

    datetimeobj = n[0]
    dateobj = datetimeobj[0]
    timeobj = datetimeobj[1]

    deptimestring = "%s-%s-%sT%s:%s:%s" %(dateobj.get('year'), dateobj.get('month'), dateobj.get('day'), timeobj.get('hour'), timeobj.get('minute'), '0')

    dep = datetime.strptime(deptimestring, "%Y-%m-%dT%H:%M:%S")
    delta = dep - now
    #print("+---=" + str(dep))
    return (delta < mindelta, dep)


def getDepartures(stopID):
    (sid, lines) = initSession(stopID)
    deptimes = []
    departure = {}
    for l in lines:
        if len(lines[l]) > 0:
            (nd, deptime) = nextDeparture(sid, lines[l])
            departure[l] = nd
            deptimes.append(deptime)
    departure['time'] = min(deptimes).strftime("%Y-%m-%dT%H:%M:%S")
    return departure
