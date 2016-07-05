from math import cos, asin, sin, sqrt, atan2, pi, degrees, radians
from secrets import APIKEY
import datetime
import json, polyline
import requests

# earth's radius in miles
e_radius = 3959

def distance(ll1, ll2):
    lat1, lon1 = ll1
    lat2, lon2 = ll2
    # Using the Haversine formula
    p = 0.017453292519943295 #math.pi / 180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 2 * e_radius * asin(sqrt(a))

def directionmatrix (origin, destination, mode):
    base_url = 'https://maps.googleapis.com/maps/api/directions/json'
    geo = {
        'origin': origin,
        'destination': destination,
        'mode': mode,
        'key': APIKEY}
    r = requests.get(base_url, params=geo)
    response = r.json()
    route = response['routes'][0]
    polyline = route['overview_polyline']['points']
    legs = route['legs'][0]
    time = legs['duration']['value']
    return dict(time=time, polyline=polyline)

# nine_am = int(time.mktime(time.struct_time([2016,7,14,9,00,0,0,0,0])))

def directions (origin, destination):
    base_url = 'https://maps.googleapis.com/maps/api/directions/json'
    geo = {
        'origin': origin,
        'destination': destination,
        'mode': 'driving',
        'key': APIKEY}
    r = requests.get(base_url, params=geo)
    response  = r.json()
    route = response['routes'][0]
    legs = route['legs'][0]
    return dict(route=route,legs=legs)

def getoverviewpline (dirs):
    polyline = dirs['route']['overview_polyline']['points']
    return polyline

def decodepolyline(polyline):
    return polyline.decode(polyline)

# example_dirs = directions('denver, colorado','reno, nevada')

# example_waypoints = getoverviewpline(example_dirs)

# example for testing, this is a polyline from Denver, CO to Reno, NV
# hard-coded to avoid using up API calls unnecessarily
# ex_waypts = [(39.73924, -104.99025), (39.74678, -105.01813), (39.77182, -104.99019), (39.88552, -104.98742), (40.05219, -104.98031), (40.27255, -104.98005), (40.35819, -104.98299), (40.49966, -104.99159), (40.62454, -105.00114), (40.71077, -104.99464), (40.75186, -104.99228), (40.75508, -105.00743), (40.75482, -105.09512), (40.77322, -105.1325), (40.77898, -105.15332), (40.76551, -105.16988), (40.77678, -105.18531), (40.79469, -105.21702), (40.89183, -105.29045), (40.94619, -105.34344), (40.97973, -105.39029), (41.03998, -105.45135), (41.07535, -105.49435), (41.13333, -105.55181), (41.17708, -105.5905), (41.20815, -105.5993), (41.29628, -105.59436), (41.31288, -105.61442), (41.34271, -105.62358), (41.35097, -105.6595), (41.35333, -105.73244), (41.36468, -105.77853), (41.39331, -105.82267), (41.41724, -105.85359), (41.43775, -105.92279), (41.4605, -105.9808), (41.50799, -106.05316), (41.54466, -106.08466), (41.56642, -106.14131), (41.61031, -106.23098), (41.66852, -106.3687), (41.68781, -106.3806), (41.70589, -106.41028), (41.75418, -106.51441), (41.73976, -106.61866), (41.73062, -106.6986), (41.74298, -106.78013), (41.74963, -106.94296), (41.77334, -107.07788), (41.78935, -107.19985), (41.77746, -107.30498), (41.78902, -107.38068), (41.77693, -107.44971), (41.7169, -107.77977), (41.70459, -107.89614), (41.6724, -107.98614), (41.6514, -108.13028), (41.62999, -108.28728), (41.63947, -108.4734), (41.64847, -108.63237), (41.64762, -108.68347), (41.66546, -108.72626), (41.68388, -108.80612), (41.69222, -108.89739), (41.67354, -108.92493), (41.66735, -108.96943), (41.59631, -109.16455), (41.59534, -109.19824), (41.6102, -109.22253), (41.57941, -109.25625), (41.53964, -109.35591), (41.52772, -109.42956), (41.5446, -109.48064), (41.56455, -109.55211), (41.54383, -109.65307), (41.54306, -109.79984), (41.53646, -109.93192), (41.41945, -110.13824), (41.38553, -110.21882), (41.36818, -110.29425), (41.34985, -110.38158), (41.32589, -110.46867), (41.29763, -110.55624), (41.2991, -110.67855), (41.29758, -110.69809), (41.30901, -110.7352), (41.29359, -110.77848), (41.27027, -110.82751), (41.2697, -110.86513), (41.26784, -110.93309), (41.25922, -110.95961), (41.24748, -111.01779), (41.24886, -111.0635), (41.21042, -111.09723), (41.15761, -111.14284), (41.12847, -111.16219), (41.12173, -111.18689), (41.08582, -111.23499), (41.01744, -111.36709), (40.98587, -111.41136), (40.96851, -111.4392), (40.94942, -111.42095), (40.90442, -111.39789), (40.84288, -111.38737), (40.81015, -111.40409), (40.80666, -111.42965), (40.78391, -111.45878), (40.73975, -111.48026), (40.72169, -111.52236), (40.73085, -111.5496), (40.75441, -111.59031), (40.73912, -111.67044), (40.7519, -111.71378), (40.73253, -111.75445), (40.71425, -111.78595), (40.71758, -111.83634), (40.72479, -111.94726), (40.71684, -112.13312), (40.72242, -112.22848), (40.68648, -112.27086), (40.66284, -112.33123), (40.67552, -112.40066), (40.71631, -112.54472), (40.74532, -112.645), (40.75844, -112.77155), (40.82243, -112.89143), (40.76882, -112.98466), (40.72609, -113.14097), (40.73127, -113.47734), (40.74056, -113.91121), (40.73808, -114.04456), (40.75539, -114.11694), (40.84471, -114.21016), (40.8984, -114.27227), (40.90622, -114.30208), (41.03256, -114.49313), (41.07219, -114.54285), (41.07788, -114.57925), (41.07156, -114.63319), (41.11308, -114.78661), (41.10341, -114.96942), (41.1015, -115.08841), (41.08327, -115.27048), (41.02217, -115.39764), (40.97934, -115.43852), (40.96005, -115.46118), (40.94945, -115.54004), (40.94952, -115.62918), (40.92596, -115.67764), (40.88083, -115.71706), (40.83606, -115.78888), (40.78776, -115.86317), (40.7487, -115.94368), (40.72204, -115.97042), (40.71649, -116.00352), (40.72795, -116.04851), (40.72489, -116.09415), (40.71137, -116.15422), (40.68546, -116.18612), (40.65064, -116.29393), (40.63805, -116.34282), (40.66311, -116.42277), (40.69348, -116.49786), (40.7004, -116.5354), (40.67931, -116.61833), (40.67322, -116.70448), (40.65355, -116.75758), (40.61574, -116.79678), (40.61753, -116.90056), (40.64516, -116.95099), (40.69199, -117.00037), (40.72941, -117.04807), (40.82834, -117.17449), (40.88545, -117.27364), (40.92125, -117.37333), (40.92769, -117.42333), (40.95398, -117.50045), (40.98947, -117.54807), (41.02426, -117.58312), (41.00852, -117.63645), (40.96933, -117.74518), (40.94279, -117.77575), (40.8951, -117.89592), (40.87324, -117.93968), (40.72823, -118.03479), (40.67509, -118.08257), (40.64152, -118.19317), (40.59811, -118.25287), (40.55914, -118.27603), (40.48, -118.28398), (40.37243, -118.30541), (40.31488, -118.33518), (40.19667, -118.43821), (40.15423, -118.49333), (40.08935, -118.60055), (40.06719, -118.64397), (40.02797, -118.67204), (39.97135, -118.69728), (39.92384, -118.7962), (39.86979, -118.88962), (39.81629, -118.9977), (39.77414, -119.03707), (39.70052, -119.10147), (39.62945, -119.19289), (39.61328, -119.22436), (39.61837, -119.28098), (39.59786, -119.36007), (39.58072, -119.47064), (39.56748, -119.47779), (39.56843, -119.53023), (39.54312, -119.5958), (39.51058, -119.65897), (39.53447, -119.74216), (39.53661, -119.79706), (39.52956, -119.81415)]
# waypoints = [[tuple[0], tuple[1]] for tuple in ex_waypts]
#
def latlongdists(latlons):
    list_distances = []
    for indx, latlong in enumerate(latlons):
        if indx < len(latlons)-2:
            dist = distance(latlons[indx], latlons[indx+1])
            list_distances.append(dist)
    return list_distances

def interpolate (latlng1, latlng2, dist):
    lat1 = radians(latlng1[0])
    lon1 = radians(latlng1[1])
    lat2 = radians(latlng2[0])
    lon2 = radians(latlng2[1])
    d = distance(latlng1, latlng2)
    f = dist/d
    d_r = d/e_radius
    A = sin((1-f)*d_r)/sin(d_r)
    B = sin(f*d_r)/sin(d_r)
    x = A*cos(lat1)*cos(lon1) +  B*cos(lat2)*cos(lon2)
    y = A*cos(lat1)*sin(lon1) +  B*cos(lat2)*sin(lon2)
    z = A*sin(lat1)           +  B*sin(lat2)
    lat = atan2(z,sqrt(x**2+y**2))
    lat_deg = degrees(lat)
    lon = atan2(y,x)
    lon_deg = degrees(lon)
    return (lat_deg, lon_deg)


def even_spacer(latlons, separation = 30):
    even_list = []
    even_list.append((latlons[0]))
    current_waypoint = latlons[0]
    leg_dist = 0
    for index, waypoint in enumerate(latlons):
        delta_dist = distance(current_waypoint, waypoint)
        leg_dist += delta_dist
        if leg_dist>separation:
            prev = latlons[index-1]
            next = latlons[index]
            rev_dist = leg_dist - separation
            mid_point = interpolate(next,prev, rev_dist)
            current_waypoint = mid_point
            leg_dist = 0
            leg_dist += rev_dist
            even_list.append(mid_point)
        else:
            current_waypoint = waypoint
    even_list.append(latlons[-1])
    return even_list

def make_route(origin, destination, separation, starttime = datetime.datetime.now()):
    dirs = directionmatrix(origin, destination, mode="DRIVING")
    lat_long_list = polyline.decode(dirs.get('polyline'))
    total_dist = sum(latlongdists(lat_long_list)) # in miles
    transit_time = dirs.get('time') # in seconds
    avg_speed = total_dist / transit_time # miles per second
    even_split_list = even_spacer(lat_long_list, separation)
    out_route = []
    current_time = starttime
    for i, element in even_split_list:
        current_time = current_time + datetime.timedelta(0, separation/avg_speed)
        out_route.append({'latlon': element, 'time': current_time})
    for element in out_route:
        print 'latlon = ' + str(element.get('latlon')) + ' and time = ' + str(element.get('time'))
    print str(avg_speed * 3600) + " mph" # converted to mph
make_route('chicago, IL', 'denver, CO', 30)

# example_waypoints = getoverviewpline(example_dirs)
# make_route('denver, colorado','reno, nevada')
# print decodepolyline(example_waypoints)
# print decodepolyline(example_dirs.get('route').get('overview_polyline').get('points'))

# dist_list = latlongdists(waypoints)
# dist_list = [ round(elem, 2) for elem in dist_list]
# print(dist_list)
# print(waypoints)
# even_waypoints = even_spacer(waypoints)

# print(latlongdists(even_waypoints))
# print even_waypoints

# print(sorted(list_distances))
# print(sum(list_distances))

