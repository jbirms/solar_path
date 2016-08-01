from __future__ import division
import os
import sys
# import numpy as np 
# import pandas as pd 
# from flask import Flask, request, send_from_directory
# from flask.json import jsonify
# from flask import make_response, request, current_app
# from functools import update_wrapper
# from wrapper import crossdomain 
import datetime as datetime
# import math

from math import cos, asin, sin, sqrt, atan2, pi, degrees, radians, ceil, floor
from secrets import APIKEY
import datetime, time
import json
from polyline import decode
import requests
from bisect import bisect_left

# app = Flask(__name__)
# earth's radius in meters
e_radius = 6371000

def distance(ll1, ll2):
    # lat1, lon1 = ll1
    # lat2, lon2 = ll2
    lat1 = ll1.get('loc').get('lat')
    lng1 = ll1.get('loc').get('lng')
    lat2 = ll2.get('loc').get('lat')
    lng2 = ll2.get('loc').get('lng')
    # Using the Haversine formula
    p = 0.017453292519943295 #pi / 180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lng2 - lng1) * p)) / 2
    return 2 * e_radius * asin(sqrt(a))

def quote(s1):
    return "'{}'".format(s1)

def build_dict(seq, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))

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
    # print route
    legs = route['legs'][0]
    return dict(route=route,legs=legs)
# dir1 = directions('455 broadway, new york, ny', '7 Lower Center St, Clinton, NJ')
# print dir1

def parse_directions(dirs):
    legs = dirs.get('legs').get('steps')
    out = []
    for leg in legs:
        out.append(dict(dist=leg.get('distance').get('value'), start_loc=leg.get('start_location'), end_loc=leg.get('end_location'), poly=leg.get('polyline').get('points'), seconds=leg.get('duration').get('value')))
    return out

def decodepolyline(polyline):
    line = decode(polyline)
    out_list = []
    for point in line:
        out_list.append({'loc': {'lat': point[1], 'lng': point[0]}})
    return out_list

def even_spacer(my_route, separation = 300):
# my_route list of dicts format: {'dist': 355, 'start_loc':{'lat':-41, 'lng':-75}, end_loc:{'lat':-40, 'lng':-76}, poly:'sdfaoweruv4r', 'seconds': 45}
    all_points = []
    timings = [0]
    timestamp = 0
    dist_traveled = 0
    all_points.append({'loc': my_route[0].get('start_loc'), 't': timestamp, 'dist': dist_traveled})
    for waypoint in my_route:
        avg_speed = waypoint.get('dist') / waypoint.get('seconds')
        # print avg_speed
        # print waypoint.get('poly')
        poly_list = decodepolyline(quote(waypoint.get('poly')))
        for index, point in enumerate(poly_list):
            if 0 < index < len(poly_list) - 1:
                leg_dist = distance(poly_list[index], poly_list[index+1])
                dist_traveled += leg_dist
                timestamp += leg_dist / avg_speed
                timings.append(round(timestamp))
                all_points.append({'loc': point.get('loc'), 't': round(timestamp), 'dist': round(dist_traveled)})
    out_list = []
    out_list.append(all_points[0])
    num = 0
    i = 1
    time_dict = build_dict(all_points, key="t")
    reduced_times = []
    while num < timestamp:
        num = i * separation
        reduced_times.append(timings[bisect_left(timings, num) - 1])
        i += 1
    for item in reduced_times:
        del time_dict[item]['index']
        out_list.append(time_dict[item])
    return out_list

# parameters: lat(default = 40.713, lng(default = -74.006), datetime(default = now), elevation(calculated from lat, lng), tilt_angle(default = 0deg), 
# .strftime("%m/%d/%Y"), time = datetime.datetime.now().strftime("%H:%M")
# formulae from pveducation.org
def solar_intensity(lat = 40.713, lng = -74.006, date_time = datetime.datetime.now()):
    # day_of_year = datetime.datetime.strptime(date_time, '%m/%d/%Y').timetuple().tm_yday
    day_of_year = date_time.timetuple().tm_yday
    declination_angle = degrees(asin(sin(radians(23.45)) * sin(2 * pi/365 * (day_of_year - 81))))
    # print 'declination_angle = ' + str(declination_angle)
    # ~~~equation of time~~~ to account for orbital eccentricity and axial wobble
    e_o_t = 9.87 * sin(2.0 * 2 * pi / 365 * (day_of_year - 81)) - 7.53 * cos(2 * pi / 365 * (day_of_year - 81)) - 1.5 * sin(2 * pi / 365 * (day_of_year - 81))
    gmt_diff = floor(lng / 15) # hour difference from GMT (+5 for EST)
    lstm = 15.0 * gmt_diff # local standard time meridian (edge of time zone)
    tc = 4.0 * (lng - lstm) + e_o_t # time correction factor
    local_solar_time = date_time + datetime.timedelta(0, tc/60.0)
    lst_dec = local_solar_time.hour + local_solar_time.minute / 60.0 + local_solar_time.second / 3600.0
    hour_angle = 15.0 * (lst_dec - 12.0)
    # print 'hour angle past solar noon = ' + str(hour_angle)
    # with a flat panel, the elevation angle is the incident angle
    elevation_angle = degrees(asin(sin(radians(declination_angle)) * sin(radians(lat)) + cos(radians(declination_angle)) * cos(radians(lat)) * cos(radians(hour_angle))))
    # print elevation_angle
    rad_from_vert = pi / 2 - radians(elevation_angle) # zenith angle in radians for airmass formula
    if rad_from_vert < pi / 2:
        air_mass = 1 / (cos(rad_from_vert) + 0.50572 * (96.07995 - degrees(rad_from_vert)) ** (-1.6364))
    else:
        air_mass = None
    e_0 = 1367 * (1 + 0.033 * cos(2 * pi * (day_of_year - 3) / 365))
    if air_mass:
        intensity = cos(rad_from_vert) * e_0 * 0.7 ** (air_mass ** 0.678)
        return intensity
    else:
        return 0
    # print elevation_angle
    # print intensity
# solar_intensity()
# {'dist': 355, 'start_loc':{'lat':-41, 'lng':-75}, end_loc:{'lat':-40, 'lng':-76}, poly:'sdfaoweruv4r', 'seconds': 45}

def route(origin, destination, separation, starttime = datetime.datetime.now()):
    out_route = even_spacer(parse_directions(directions(origin, destination)), separation)
    # intensity_list = []
    for point in out_route:
        point['t'] = starttime + datetime.timedelta(0, point.get('t'))
        intensity = round(solar_intensity(point.get('loc').get('lat'), point.get('loc').get('lng'), point.get('t')), 2)
        # point['t'] = str(point['t'])
        point['intensity'] = intensity
        point['t'] = time.mktime(point['t'].timetuple())
        # intensity_list.append(dict(lat=point.get('latlon')[0], lon=point.get('latlon')[1], intensity=intensity))
    return out_route

test_list = route('kampala, uganda', 'Kisangani, Democratic Republic of the Congo', 1000, datetime.datetime(2016, 6, 21, 6, 0, 0))
with open("data.json", 'w') as f:
    json.dump(test_list, f)

def integrate(intensity_list):
    integral = 0
    for index, item in enumerate(intensity_list):
        if index < (len(intensity_list) - 1):
            delta_t = float((intensity_list[index + 1].get('t') - intensity_list[index].get('t')) / 3600.0)
            # print delta_t
            avg_intensity = float(intensity_list[index + 1].get('intensity') + intensity_list[index].get('intensity')) / 2.0
            integral += delta_t * avg_intensity
    return integral / 1000.0

print "{} kWh/m^2".format(round(integrate(test_list), 4))

# @app.route("/route", methods=["POST", "GET"])
# # @crossdomain(origin='*')
# def router ():
#     form_origin = request.form.get("str1")
#     form_dest = request.form.get("str2")
#     form_time = request.form.get("str3")
#     intensity_data = route(form_origin, form_dest, form_time)
#     return jsonify(intensity_data)

# @app.route("/")
# def serve_html():
#      return send_from_directory('static', 'mapper.html')

# @app.template_filter('date_to_millis')
# def date_to_millis(d):
#     """Converts a datetime object to the number of milliseconds since the unix epoch."""
#     return int(time.mktime(d.timetuple())) * 1000

#
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8080))
#     app.debug = True
#     app.run(host='localhost', port=port)


# counter = 0
# with open('e_w_ints.txt', 'w') as outfile:
#   outfile.write("['Index', 'Intensity'], ")
#   for line in test_list:
#       counter = counter + 1
#       outfile.write("['" + str(counter) + "', " + str(line.get('intensity')) + '], ')

# with open('n_s_data.json', 'w') as outfile:
#     json.dump(test_list, outfile)

# for item in test_list:
#   print item
# print test_list