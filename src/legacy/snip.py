def getNextStation(f):
    m1 = 100
    m2 = 100
    for s in stations['stations']:
        s_loc = s['coordinates']
        f_loc = f['geometry']['coordinates']
        d = distance(s_loc, f_loc)
        if d < m2:
            m2 = d
            n2 = s
            if d < m1:
                m1 = d
                m2 = m1
                n1 = s
                n2 = n1
    return (n1, n2)
