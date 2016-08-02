#!/usr/bin/env python3

import sys, os, math, json


# This works well enough for great circle distance
DUBLIN_LAT = 53.3381985
DUBLIN_LON = -6.2592576
EARTH_RADIUS = 6371.0  # In kilometers (on tropics)
MAX_DISTNACE = 100.0   # In kilometers

# But earth is not really a sphere,
# we should use WSG84 (World Geodesic System):
ACCURACY = 0.000000001  # Of gamma, about 1.0 =~ 1000 kilometers
FLAT = 298.257223563    # Flattening of the ellipsoid
MAJOR = 6378137.0       # Major radius (equator), in meters
MINOR = 6356752.314245  # Minor radius (poles, (1 - 1/FLAT)*MAJOR), in meters


def yield_jsons(input):
    with open(input) as infile:
        for line in infile:
            # ignore empty lines (just in case)
            json_line = line.strip()
            if json_line:
                try:
                    json_obj = json.loads(json_line)
                    yield json_obj
                except json.decoder.JSONDecodeError:
                    # oh well, a bad line, ignore and continue the loop
                    pass


# treat badly encoded floats as missing data
def get_float(x):
    try:
        return float(x)
    except ValueError:
        return None


def print_invites(input):
    invites = {}
    for j in yield_jsons(input):
        lat, lon = get_float(j.get('latitude')), get_float(j.get('longitude'))
        user_id, name = j.get('user_id'), j.get('name')
        if None in [lat, lon, user_id, name]:
            # bad data, ignore
            continue
        # Great Circle Distance is faster
        # Vincenty is more accurate (and its output is in meters, so adjust)
        #distance = dublin_gcd(lat, lon)
        distance = dublin_vincenty(lat, lon)/1000.0
        if MAX_DISTNACE >= distance:
            invites[user_id] = name
    for k in sorted(invites.keys()):
        print('%3i' % k, invites[k])


# We should really be using math.radians,
# but for educational purposes we will write it by hand.
def radians(x):
    return math.pi*(x/180.0)


# Great Circle Distance
def gcd(x1, y1, x2, y2):
    x1r, y1r, x2r, y2r = list(map(radians, [x1, y1, x2, y2]))
    angle = math.acos( math.sin(x1r) * math.sin(x2r)
                     + math.cos(x1r) * math.cos(x2r) * math.cos(abs(y1r-y2r)))
                     # The abs() call is not needed since cos(x) == cos(-x),
                     # but it is in there to allow for easier reasoning.
    # On the other hand abs() is needed here
    # since a negative distance is meaningless.
    return abs(EARTH_RADIUS * angle)


def dublin_gcd(x, y):
    return gcd(DUBLIN_LAT, DUBLIN_LON, x, y)


# Vincenty's geodesic algorithm
# https://en.wikipedia.org/wiki/Vincenty%27s_formulae
# Since Great Circle Distance has several issues with places that are very far
# away and is poor in dealing with floating point precision on machines, we
# also implement the major geodesic algorithm.  The output distance is in
# meters, to reduce even further floating point precision problems.
def vincenty(x1, y1, x2, y2):
    x1r, y1r, x2r, y2r = list(map(radians, [x1, y1, x2, y2]))
    flat_inv = 1/FLAT
    lon_diff = y2r - y1r
    # reduced latitudes and cached sin/cos
    red_lat1 = math.atan((1-flat_inv) * math.tan(x1r))
    red_lat2 = math.atan((1-flat_inv) * math.tan(x2r))
    sinu1 = math.sin(red_lat1)
    sinu2 = math.sin(red_lat2)
    cosu1 = math.cos(red_lat1)
    cosu2 = math.cos(red_lat2)
    cur_gamma = lon_diff  # initial value for iteration
    prev_gamma = None
    while not prev_gamma or ACCURACY < abs(cur_gamma - prev_gamma):
        singm = math.sin(cur_gamma)
        cosgm = math.cos(cur_gamma)
        sint = math.sqrt( (cosu2*singm)**2
                        + (cosu1*sinu2 - sinu1*cosu2*cosgm)**2
                        )
        cost = sinu1*sinu2 + cosu1*cosu2*cosgm
        t = math.atan(sint/cost)
        sina = cosu1*cosu2*singm/sint
        sin2a = sina**2
        cos2a = 1 - sin2a
        costm = cost - 2*sinu1*sinu2/cos2a
        c = (flat_inv/16)*cos2a*(4 + flat_inv*(4 - 3*cos2a))
        prev_gamma = cur_gamma
        cur_gamma = lon_diff + (1-c)*flat_inv*sina*(
                t + c*sint*(costm + c*cost*(-1 + 2*costm**2))
                )
    u2 = cos2a*(MAJOR**2 - MINOR**2)/MINOR**2
    majord = 1 + (u2/16384)*(4096 + u2*(-768 + u2*(320 - 175*u2)))
    minord = (u2/1024)*(256 + u2*(-128 + u2*(74 - 47*u2)))
    deltat = minord*sint*( costm
                         + (1.0/4)*minord*( cost*(-1 + 2*costm**2)
                                          - ( (1.0/6)*minord*costm
                                            * (-3 + 4*sint**2)
                                            * (-3 + 4*costm**2)
                                            )
                                          )
                         )
    distance = MINOR*majord*(t - deltat)
    return distance


def dublin_vincenty(x, y):
    return vincenty(DUBLIN_LAT, DUBLIN_LON, x, y)


# Test one equation against the other,
# Great Circle Distance versus Vincenty.
# Requires the test file to be named 'customers.json'
#
# Unfortunately great circle distance is often plain bad and its accuracy is
# poor, therefore we need a huge accuracy allowance in the tests.
def test_eq(input):
    test_accuraccy = 1.0  # 1Km
    for j in yield_jsons(input):
        lat, lon = get_float(j.get('latitude')), get_float(j.get('longitude'))
        d_gcd = dublin_gcd(lat, lon)
        # Vincenty gives the distance in meters, adjust
        d_vin = dublin_vincenty(lat, lon)/1000.0
        delta = abs(d_gcd - d_vin)
        if test_accuraccy >= delta:
            print( 'Test passed [%10.6f] =~ [%10.6f]    (d %10.6f)'
                 % (d_gcd, d_vin, delta)
                 )
        else:
            print( 'TEST FAILED [%10.6f] =! [%10.6f]    (d %10.6f)'
                 % (d_gcd, d_vin, delta)
                 )


if '__main__' == __name__:
    usage = 'invite.py [help] [test] [customers file]'
    # trivial argument parsing (get the first or a default)
    input = (sys.argv[1:2] or ['customers.json'])[0]
    if 'help' == input:
        print(usage)
        exit(0)
    elif 'test' == input:
        test_eq('customers.json')
        exit(0)
    elif not os.path.isfile(input):
        print(input, ': not a regular file')
        exit(1)
    print_invites(input)

