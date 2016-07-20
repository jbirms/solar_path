import sys
# import numpy as np 
# import pandas as pd 
import datetime as datetime
import math
from interpolate import *

# parameters: lat(default = 40.713, lng(default = -74.006), datetime(default = now), elevation(calculated from lat, lng), tilt_angle(default = 0deg), 
# .strftime("%m/%d/%Y"), time = datetime.datetime.now().strftime("%H:%M")
# formulae from pveducation.org
def solar_intensity(lat = 40.713, lng = -74.006, date_time = datetime.datetime.now()):
	# day_of_year = datetime.datetime.strptime(date_time, '%m/%d/%Y').timetuple().tm_yday
	day_of_year = date_time.timetuple().tm_yday
	declination_angle = math.degrees(math.asin(math.sin(math.radians(23.45)) * math.sin(2 * math.pi/365 * (day_of_year - 81))))
	# print 'declination_angle = ' + str(declination_angle)
	# ~~~equation of time~~~ to account for orbital eccentricity and axial wobble
	e_o_t = 9.87 * math.sin(2.0 * 2 * math.pi / 365 * (day_of_year - 81)) - 7.53 * math.cos(2 * math.pi / 365 * (day_of_year - 81)) - 1.5 * math.sin(2 * math.pi / 365 * (day_of_year - 81))
	gmt_diff = math.floor(lng / 15) # hour difference from GMT (+5 for EST)
	lstm = 15.0 * gmt_diff # local standard time meridian (edge of time zone)
	tc = 4.0 * (lng - lstm) + e_o_t # time correction factor
	local_solar_time = date_time + datetime.timedelta(0, tc/60.0)
	lst_dec = local_solar_time.hour + local_solar_time.minute / 60.0 + local_solar_time.second / 3600.0
	hour_angle = 15.0 * (lst_dec - 12.0)
	# print 'hour angle past solar noon = ' + str(hour_angle)
	# with a flat panel, the elevation angle is the incident angle
	elevation_angle = math.degrees(math.asin(math.sin(math.radians(declination_angle)) * math.sin(math.radians(lat)) + math.cos(math.radians(declination_angle)) * math.cos(math.radians(lat)) * math.cos(math.radians(hour_angle))))
	# print elevation_angle
	rad_from_vert = math.pi / 2 - math.radians(elevation_angle) # zenith angle in radians for airmass formula
	if rad_from_vert < math.pi / 2:
		air_mass = 1 / (math.cos(rad_from_vert) + 0.50572 * (96.07995 - math.degrees(rad_from_vert)) ** (-1.6364))
	else:
		air_mass = None
	e_0 = 1367 * (1 + 0.033 * math.cos(2 * math.pi * (day_of_year - 3) / 365))
	if air_mass:
		intensity = math.cos(rad_from_vert) * e_0 * 0.7 ** (air_mass ** 0.678)
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
		# intensity_list.append(dict(lat=point.get('latlon')[0], lon=point.get('latlon')[1], intensity=intensity))
	return out_route

test_list = route('moab, ut', 'reno, nv', 3600, datetime.datetime(2016, 7, 7, 9, 0, 0))
print test_list

def integrate(intensity_list):
	integral = 0
	for index, item in enumerate(intensity_list):
		if index < (len(intensity_list) - 1):
			delta_t = float((intensity_list[index + 1].get('t') - intensity_list[index].get('t')).total_seconds()) / 3600.0
			# print delta_t
			avg_intensity = float(intensity_list[index + 1].get('intensity') + intensity_list[index].get('intensity')) / 2.0
			integral += delta_t * avg_intensity
	return integral / 1000.0

print "{} kWh/m^2".format(round(integrate(test_list), 4))

# counter = 0
# with open('e_w_ints.txt', 'w') as outfile:
# 	outfile.write("['Index', 'Intensity'], ")
# 	for line in test_list:
# 		counter = counter + 1
# 		outfile.write("['" + str(counter) + "', " + str(line.get('intensity')) + '], ')

# with open('n_s_data.json', 'w') as outfile:
#     json.dump(test_list, outfile)

# for item in test_list:
# 	print item
# print test_list