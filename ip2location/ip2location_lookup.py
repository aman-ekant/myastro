import pandas as pd
import IP2Location
import time

starttime = time.clock()
#IP4
n1 = 216
n2 = 250
n3 = 125
n4 = 0
regions_good = pd.read_csv('../data/ip2_location/geonames_regions.csv', delimiter=',', index_col=None, header=0,
                           keep_default_na=False,
                           na_values="NaN", names=(
		['region', 'country', 'lat', 'long', 'pytzname', 'timezone', 'dst', 'std_abv', 'dst_abv']))
IP2LocObj = IP2Location.IP2Location()
# open the bin file
IP2LocObj.open('../data/ip2_location/IP2LOCATION-LITE-DB11.BIN')
ip_add = str(n1) + '.' + str(n2) + '.' + str(n3) + '.' + str(n4)
rec = IP2LocObj.get_all(ip_add)
#ipnumber = 16777216 * n1 + 65536 * n2 + 256 * n3 + n4
#print ipnumber
print ip_add
print rec.country_short
print rec.country_long
print rec.region
print rec.city
print rec.latitude
print rec.longitude
print rec.zipcode
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
print regions_good.ix[region_override + country_overide]['pytzname']
print regions_good.ix[region_override + country_overide]['timezone']
print regions_good.ix[region_override + country_overide]['dst']
print regions_good.ix[region_override + country_overide]['std_abv']
print regions_good.ix[region_override + country_overide]['dst_abv']


print 'BIN transit time: ', time.clock() - starttime

# _______________
# IPV6
# _________________
print "---------------"
print "IPV6"
IP2LocObj.open('../data/ip2_location/IP2LOCATION-LITE-DB11.IPV6.BIN')
ip_add = "2607:f1c0:83c:7000:0:0:43:963d"

rec = IP2LocObj.get_all(ip_add)

print ip_add
print rec.country_short
print rec.country_long
print rec.region
print rec.city
print rec.latitude
print rec.longitude
print rec.zipcode
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
print regions_good.ix[region_override + country_overide]['pytzname']
print regions_good.ix[region_override + country_overide]['timezone']
print regions_good.ix[region_override + country_overide]['dst']
print regions_good.ix[region_override + country_overide]['std_abv']
print regions_good.ix[region_override + country_overide]['dst_abv']


