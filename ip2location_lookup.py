#!/usr/bin/env python
import pandas as pd
import IP2Location
import time

starttime = time.clock()
#IP4
regions_good = pd.read_csv('ip2_location/geonames_regions.csv', delimiter=',', index_col=None, header=0,
                           keep_default_na=False,
                           na_values="NaN", names=(
		['region', 'country', 'lat', 'long', 'pytzname', 'timezone', 'dst', 'std_abv', 'dst_abv']))
IP2LocObj = IP2Location.IP2Location()
# open the bin file
def ipv42loc(ip_addrs):
	IP2LocObj.open('ip2_location/IP2LOCATION-LITE-DB11.BIN')

	rec = IP2LocObj.get_all(ip_addrs)
	#print rec.country_short
	country = rec.country_long
	region = rec.region
	city = rec.city
	latitude = rec.latitude
	longitude = rec.longitude
	#print rec.zipcode
	#print rec.timezone
	if rec.city == "-" and rec.region == "-" and rec.country_short == "-":
		region_override = "XX"#rec.country_short
		country_overide = "XX"#rec.country_short
	elif rec.city == "-" or rec.region == "-":
		region_override = rec.country_short
		country_overide = rec.country_short
	else:
		region_override = rec.region
		country_overide = rec.country_short
	timezone = (regions_good.ix[region_override + country_overide]['pytzname'])
	timezoneid = (regions_good.ix[region_override + country_overide]['timezone'])
	#print regions_good.ix[region_override + country_overide]['dst']
	#print regions_good.ix[region_override + country_overide]['std_abv']
	#print regions_good.ix[region_override + country_overide]['dst_abv']

	return latitude, longitude, timezoneid, region, city, country, timezone


#print 'BIN transit time: ', time.clock() - starttime

# _______________
# IPV6
# _________________

def ipv62loc(ip_addrs):
	IP2LocObj.open('ip2_location/IP2LOCATION-LITE-DB11.IPV6.BIN')
	#ip_add = "2607:f1c0:83c:7000:0:0:43:963d"

	rec = IP2LocObj.get_all(ip_addrs)

	#print ip_add
	#print rec.country_short
	country = rec.country_long
	region = rec.region
	city = rec.city
	latitude = rec.latitude
	longitude = rec.longitude
	#print rec.zipcode
	#print rec.timezone
	if rec.city == "-" and rec.region == "-" and rec.country_short == "-":
		region_override = "XX"#rec.country_short
		country_overide = "XX"#rec.country_short
	elif rec.city == "-" or rec.region == "-":
		region_override = rec.country_short
		country_overide = rec.country_short
	else:
		region_override = rec.region
		country_overide = rec.country_short
	timezone = (regions_good.ix[region_override + country_overide]['pytzname'])
	timezoneid = (regions_good.ix[region_override + country_overide]['timezone'])
	#print regions_good.ix[region_override + country_overide]['dst']
	#print regions_good.ix[region_override + country_overide]['std_abv']
	#print regions_good.ix[region_override + country_overide]['dst_abv']

	return latitude, longitude, timezoneid, region, city, country, timezone