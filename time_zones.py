#!/usr/bin/env python
import pytz
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from pandas.tseries.offsets import *
import time

from dateutil import relativedelta

path = 'astro/data//atlas/'


def get_time_zone_1970(city_id, birth_date):
	pd.set_option('use_inf_as_null', True)
	time_tabs = pd.read_csv(path + 'time_tabs.csv', header=None, index_col=0,
	                        names=('table_number', 'date_start', 'zone_type'))
	city_np = np.load('astro/data/atlas/city_table_np.npy')
	latitude = city_np[city_id][0]  # ['new_lat']
	longitude = city_np[city_id][1]  # ['new_long']
	zone_type_field6 = int(city_np[city_id][2])  # ['time_zone']
	time_type_field7 = int(city_np[city_id][3])  # ['zone_type']
	py_tz_name = int(city_np[city_id][4])  # ['tz_name']
	stored_time_zone = city_np[city_id][5]  # ['n_time_zone']
	stored_dst = city_np[city_id][6]  # ['dst']
	time_deconstruct = birth_date.timetuple()
	date_year = time_deconstruct[0]
	date_month = time_deconstruct[1]
	date_day = time_deconstruct[2]
	date_hour = time_deconstruct[3]
	date_min = time_deconstruct[4]
	dst = 0.
	final_zone = 0.0
	date_change = date_year * 624000 + date_month * 48000 + date_day * 1500 + date_hour * 60 + date_min
	# date_change = 1239496620
	# print date_change, zone_type_field6, time_type_field7
	message = 0
	if zone_type_field6 < 12000:
		final_zone = zone_type_field6
		# print "Starting Time Zone: ", time_type_field7
	else:
		while zone_type_field6 > 12000:
			zone_type_field6 = zone_type_field6 - 12000
			# print 'Initial zone: ', zone_type_field6
			z = time_tabs.loc[zone_type_field6:zone_type_field6].copy()
			len_table = len(z.index)
			i = 1
			starting_date = z['date_start'].iloc[0]
			# print z['date_start'].iloc[i]
			while i < len_table:
				if date_change < starting_date:
					final_zone = longitude * 60
					dst = 0.
					message = 30
					break
				else:
					if starting_date <= date_change < z['date_start'].iloc[i]:
						final_zone = z['zone_type'].iloc[i - 1]
						zone_type_field6 = z['zone_type'].iloc[i - 1]
						break
				i += 1
	# print "Find out DST",time_type_field7,dst
	if time_type_field7 > 30001:
		if time_type_field7 == 30002:
			if zone_type_field6 == 4500:
				dst = 0.
			else:
				dst = 1.
		if time_type_field7 == 30003:
			if zone_type_field6 == 4500:
				dst = 0.
			else:
				time_type_field7 = 30001

	if time_type_field7 < 50:
		if time_type_field7 == 2:
			dst = 1.
		if time_type_field7 == 3:
			dst = 2.
		if time_type_field7 == 4:
			dst = .5
		if time_type_field7 == 6:
			dst = 20. / 60
		if time_type_field7 == 7:
			dst = 40. / 60
	if 50 < time_type_field7 < 30000:
		while 50 < time_type_field7 < 30000:
			time_type_field7 = time_type_field7 - 50
			# print time_type_field7, 'First Pass'
			z = time_tabs.loc[time_type_field7:time_type_field7].copy()
			# print z, date_change
			if z.iloc[0]['zone_type'] == 30004 and date_change < 1222753500:
				message = 10  # illinois
			if z.iloc[0]['zone_type'] == 30005 and date_change < 1222753500:
				message = 20  # Pennyslvania
			len_table = len(z.index)
			i = 1
			starting_date = z['date_start'].iloc[0]
			# print starting_date
			# print z['date_start'].iloc[i]
			while i < len_table:
				if date_change < starting_date:
					dst = 0.
					final_zone = longitude * 60
					message = 30
					break
				else:
					# print 'i am here'
					if starting_date <= date_change < z['date_start'].iloc[i]:
						# print 'zone_type', z['zone_type'].iloc[i - 1]
						time_type_field7 = z['zone_type'].iloc[i - 1]
						dst = z['zone_type'].iloc[i - 1]
						# print 'DST',z['zone_type'].iloc[i - 1]
						if dst == 2:
							dst = 1.
						if dst == 3:
							dst = 2.
						if dst == 4:
							dst = .5
						if dst == 6:
							dst = 20. / 60
						if dst == 7:
							dst = 40. / 60
						break
				i += 1
	if message == 10 and dst == 1:
		message = 10
	elif message == 20 and dst == 1:
		message = 20
	elif message == 30 and dst == 0:
		message = 30
	else:
		message = 0
	# print time_type_field7,dst,message
	if time_type_field7 == 30001:
		# cutoff date is 1987 4 26 2 am
		# next cut off is 2007 3 11 2 am  1252528620
		# After 2007
		if date_change > 1252528620:
			date_dst_last = datetime(date_year, 3, date_day, 2, 0) + relativedelta.relativedelta \
				(day=1, weekday=relativedelta.SU(2))
			date_change_dst = date_dst_last.year * 624000 + date_dst_last.month * 48000 + date_dst_last.day * 1500 + 120  # + date_min
			# print 'post 2007-3-11-2am', date_change_dst
			date_std_last = datetime(date_year, 10, date_day, 2, 0) + relativedelta.relativedelta \
				(day=31, weekday=relativedelta.SU(1))
			date_change_std = date_std_last.year * 624000 + date_std_last.month * 48000 + date_std_last.day * 1500 + 120  # + date_min
			# print 'date of change post 2007', date_year, 'dst: ', date_dst_last, 'std: ', date_std_last, 'dst', dst
			# print date_change, date_change_dst, date_change_std
			if date_change < date_change_dst:
				dst = 0.
				# print 'i am here - std time pre dst(2007) '
			else:
				if date_change < (date_change_dst + 24 * 60):
					# print "Message: Please make sure you have correct time as we are switching"
					dst = 1.
				elif date_change < date_change_std:
					dst = 1.
					# print ' i am now dst post(2007)'
				if date_change_std <= date_change <= (date_change_std + 24 * 60):
					# print "Message: Please make sure you have correct time as we are switching back to std"
					dst = 0.
				elif date_change > date_change_std:
					# print 'back to std time post 2007'
					dst = 0.
		# first sunday of april to last sunday in october up to 2007
		if date_change >= 1240087620 and date_change < 1252528620:
			date_dst_last = datetime(date_year, 3, date_day, 0, 0) + relativedelta.relativedelta \
				(day=30, weekday=relativedelta.SU(1))
			date_change_dst = date_dst_last.year * 624000 + date_dst_last.month * 48000 + date_dst_last.day * 1500 + 120  # + date_min
			date_std_last = datetime(date_year, 10, date_day, 0, 0) + relativedelta.relativedelta \
				(day=31, weekday=relativedelta.SU(-1))
			date_change_std = date_std_last.year * 624000 + date_std_last.month * 48000 + date_std_last.day * 1500 + 120  # + date_min
			# print 'date of change pre 1987-NAREN', date_year, 'dst: ', date_dst_last, 'std: ', date_std_last, 'dst', dst
			# print date_change, date_change_dst
			if date_change < date_change_dst:
				dst = 0.
				# print 'i am here - std time pre dst(2007) '
			else:
				if date_change < (date_change_dst + 24 * 60):
					# print "Message: Please make sure you have correct time as we are switching"
					dst = 1.
				elif date_change < date_change_std:
					dst = 1.
					# print ' i am now dst post(2007)'
				if date_change_std <= date_change <= (date_change_std + 24 * 60):
					# print "Message: Please make sure you have correct time as we are switching back to std"
					dst = 0.
				elif date_change > date_change_std:
					# print 'back to std time post 2007'
					dst = 0.
		# last sunday of april to last sunday in october up to 1987 april 5 2 am
		if date_change < 1240087620:
			date_dst_last = datetime(date_year, 4, date_day, 2, 0) + relativedelta.relativedelta \
				(day=30, weekday=relativedelta.SU(-1))
			date_change_dst = date_dst_last.year * 624000 + date_dst_last.month * 48000 + date_dst_last.day * 1500 + 120
			date_std_last = datetime(date_year, 10, date_day, 2, 0) + relativedelta.relativedelta \
				(day=31, weekday=relativedelta.SU(-1))
			date_change_std = date_std_last.year * 624000 + date_std_last.month * 48000 + date_std_last.day * 1500 + 120
			# print 'date of change pre 1987-naren', date_year, 'dst: ', date_dst_last, 'std: ', date_std_last, 'dst', dst
			# print date_change, date_change_dst, date_change_std
			if date_change < date_change_dst:
				dst = 0.
				# print 'i am here - std time pre dst(2007) '
			else:
				if date_change < (date_change_dst + 24 * 60):
					# print "Message: Please make sure you have correct time as we are switching"
					dst = 1.
				elif date_change < date_change_std:
					dst = 1.
					# print ' i am now dst post(2007)'
				if date_change_std <= date_change <= (date_change_std + 24 * 60):
					# print "Message: Please make sure you have correct time as we are switching back to std"
					dst = 0.
				elif date_change > date_change_std:
					# print 'back to std time post 2007'
					dst = 0.
	final_zone = - final_zone / 900.
	return latitude, longitude, final_zone, float(dst), py_tz_name, stored_time_zone, stored_dst, message, 0


def get_time_zone_1971(city_id, birth_date):
	city_np = np.load('astro/data/atlas/city_table_np.npy')
	latitude = city_np[city_id][0]  # ['new_lat']
	longitude = city_np[city_id][1]  # ['new_long']
	py_tz_name = int(city_np[city_id][4])  # ['tz_name']
	stored_time_zone = city_np[city_id][5]  # ['n_time_zone']
	stored_dst = city_np[city_id][6]  # ['dst']
	time_zone = pytz_timezone(py_tz_name)
	date_of_birth_utc = time_zone.localize(birth_date).astimezone(pytz.utc)
	is_dst_y_n = is_dst(time_zone, date_of_birth_utc)
	dst_y_n = dst_change_today(time_zone, date_of_birth_utc)
	# print is_dst_y_n, dst_y_n
	message1 = 0
	message2 = 0
	if dst_y_n:
		message1 = 50#'Time changing on date entered.'
	try:
		utc_dt = time_zone.localize(birth_date, is_dst=None)
		# print utc_dt
	except:
		if pytz.exceptions.AmbiguousTimeError:
			message2 = 60#'Time is between time change, please verify time.'
			# print ('Time is between Time change, Please verify time')
	dst = 0
	if is_dst_y_n:
		dst = stored_dst
	final_zone = stored_time_zone
	print 'A',latitude
	print 'B', longitude
	print 'C', final_zone
	print 'D', dst
	print 'E', py_tz_name
	print 'F', stored_time_zone
	print 'G', stored_dst
	print 'H', message1
	
	return latitude, longitude, final_zone, dst, py_tz_name, stored_time_zone, stored_dst, message1, message2


def pytz_timezone(timezone):
	geo_tz_db = pd.read_csv(path + 'geonamestimezone.csv', index_col=4,
	                        names=(['geo_pytz', 'geo_tz', 'geo_dst', 'geo_country', 'index', 'abv_st', 'abv_dst']))
	database_time_zone = geo_tz_db.ix[int(timezone)]['geo_pytz']
	return pytz.timezone(database_time_zone)


def is_dst(zonename, utc_dt):
	# tz = pytz.timezone(zonename)
	return utc_dt.astimezone(zonename).dst() != timedelta(0)


def dst_change_today(zonename, utc_dt):
	tz = zonename  # pytz.timezone(zonename)
	dst_today = utc_dt.astimezone(tz).dst() != timedelta(0)
	utc_date_yesterday = utc_dt - timedelta(hours=23)
	dst_yesterday = utc_date_yesterday.astimezone(tz).dst() != timedelta(0)
	if dst_today != dst_yesterday:
		return True
	else:
		return False


def get_dst(py_tz, birth_date):
	time_zone = pytz_timezone(py_tz)
	date_of_birth_utc = time_zone.localize(birth_date).astimezone(pytz.utc)
	is_dst_y_n = is_dst(time_zone, date_of_birth_utc)
	return is_dst_y_n


# This gets the lat/long, time zone, daylight saving information for birth date/city
# used for calculating birth chart
# chatsworth=12496, new delhi=207243
# prior to 1970
birth_date = datetime(1950, 6, 1, 1, 0, 0)
city = 115525#207243#67812  # 115525#32604#11493  # 64760#32604#12496

# print birth_date

lat_, long_, birth_zone, birth_dst, py_tz, new_zone, new_dst, message1, message2 = get_time_zone_1970(city, birth_date)
print 'Pre  1970', lat_, long_, birth_zone, birth_dst, py_tz, new_zone, new_dst, message1, message2

# Post 1970
# birth_date = datetime(1959, 7, 2, 12, 0, 0)
lat_, long_, birth_zone, birth_dst, py_tz, new_zone, new_dst, message1, message2 = get_time_zone_1971(city, birth_date)
print 'Post 1970', lat_, long_, birth_zone, birth_dst, py_tz, new_zone, new_dst, message1, message2


# Other use for time zone is to see if DST is in effect today
# birth_date = datetime(1992, 2, 29, 18, 20, 0)
# dst_info = get_dst(132, birth_date)
# print dst_info

def convert_timedelta(x):
	seconds = x.total_seconds()
	if seconds < 0:
		return '-ve', str(timedelta(seconds=-seconds))
	else:
		return '+ve', str(timedelta(seconds=seconds))


# tt = pytz.timezone("Europe/Istanbul")
# tt = pytz.timezone("Asia/Singapore")
# tt= pytz.timezone("America/New_York")
# tt = pytz.timezone("Asia/Kolkata")
tt = pytz.timezone('America/Los_Angeles')
y = tt._transition_info
print y[0]
today = datetime(2015, 11, 8)
x = tt._utc_transition_times
print x[0]
old_tz = timedelta(0)
old_dst = timedelta(0)
pos_neg, second1 = convert_timedelta(y[0][0])
# print pos_neg,second1
# print x,y
old_dst = timedelta(0)
date1900 = datetime(1883, 1, 1)
print date1900
# lmt_tz = timedelta(-1,58022)
lmt_tz = timedelta(0, 24924 - 24)

final_history = {}

for xx in range(1, len(x)):
	if xx == 1 and y[xx - 1][2] == 'LMT':
		print 'i am here', lmt_tz
		final_history[date1900] = y[xx - 1][2], y[xx][2], convert_timedelta(
			y[xx][0] - y[xx][1] - lmt_tz), convert_timedelta(y[xx][0]), convert_timedelta(y[xx][1])
		prev_tz = y[xx][0]
		prev_dst = y[xx][1]
		print final_history
	if xx > 1:
		print x[xx], y[xx][0], y[xx][1], y[xx][2], 'tz', y[xx][0] - y[xx][1]
		date_change = x[xx] + y[xx][0] - y[xx][1] + prev_dst
		current_dst = y[xx][1]
		if y[xx][0] - y[xx][1] - prev_tz == timedelta(0):
			if prev_dst != timedelta(0):
				if y[xx][0] == prev_raw_tz:
					print 'am here', prev_raw_tz, y[xx][1]
					current_dst = timedelta(0)
				else:
					current_dst = -prev_dst
			else:
				current_dst = y[xx][1]
		final_history[date_change] = y[xx - 1][2], y[xx][2], convert_timedelta(
			y[xx][0] - y[xx][1] - prev_tz), convert_timedelta(y[xx][0]), convert_timedelta(current_dst)
		prev_tz = y[xx][0] - y[xx][1]
		prev_dst = y[xx][1]
		prev_raw_tz = y[xx][0]
		# print final_history
	# print x[xx], y[xx][0], y[xx][1], y[xx][2],'tz',y[xx][0]- y[xx][1]

	# now_dst = y[xx][1]
	# old_dst = now_dst
	# print 'start', now_dst
	# if now_dst == timedelta(0):
	#    print 'naren',old_dst
	#    if y[xx][0] > timedelta(0):
	if xx > 1:
		old_dst = y[xx - 1][1]
		old_tz = y[xx - 1][0]
	xy = old_dst + old_tz
	timezone_change = y[xx][0] - xy - y[xx][1]
	# print 'time zone change',timezone_change,xy,y[xx][1]
	# if xx == 1:
	#    print xx,' ', (x[xx]+y[xx][0]-y[xx][1]).strftime('%A %d, %B %Y %H:%M'),'DST', y[xx][1].seconds/60,y[xx][2],convert_timedelta(y[xx][0]),'Change',timezone_change
	# else:
	#    print xx,' ', (x[xx]+y[xx][0]-y[xx][1]).strftime('%A %d, %B %Y %H:%M'),'DST' ,y[xx][1].seconds/60,y[xx][2],convert_timedelta(y[xx][0]),'Change',timezone_change
	# else:
	#    old_dst = now_dst
	#    #print 'not equal'
	#    print (x[xx]+y[xx][0]-y[xx][1]).strftime('%A %d, %B %Y %H:%M'),y[xx][1].seconds/3600,y[xx][2],convert_timedelta(y[xx][0])
	# print '------------------------------------'
	# if x[xx] > today:
	# print x[xx],x[xx-1],y[xx],y[xx-1]

	# print 'Previous',x[xx-1]+y[xx-1][0]-y[xx-1][1], 'Forward', y[xx-1][1], 'TimeZone',y[xx-1][2]
	# print 'Next',x[xx]+y[xx][0]+y[xx-1][1], 'Backward', y[xx-1][1], 'TimeZone',y[xx][2]
	# print x[xx-1]+y[xx-1][0],y[xx-1][2],y[xx-1][1]
	# break
tzchanges = pd.DataFrame(final_history, index=['z1', 'z2', 'tz_change', 't_zone', 'dst'])
tzchanges = tzchanges.T
print tzchanges['2015']

tzchanges.to_csv('astro/data/planet_stations/tzchanges.csv')

# for xx in range(1,len(x)):
#    print x[xx] ,x[xx]+y[xx][0],'gmt offset:',y[xx][0],'DST',y[xx][1],'timezone',y[xx][2],y[xx][0] - y[xx-1][0]


# weekday calculator
birth_date = datetime(1957, 1, 8, 10, 58, 0)
week_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# print week_day[birth_date.weekday()]  # monday=0, sunday =6

# week number in year, day of weekI
# print birth_date.isocalendar()


# convert date to another timezome
time_z = pytz.timezone('Pacific/Easter')
# print time_z.zone
# date_convert = datetime(2015, 10, 28, 0, 36,0)
date_convert = datetime.now()
time_in_tz = time_z.localize(date_convert)
# print time_in_tz
new_time_zone = pytz.timezone('Asia/Tokyo')
# print time_in_tz.astimezone(new_time_zone)

# days duration between two dates with time and taking time zone into account
tz_start = pytz.timezone('America/Los_Angeles')
tz_end = pytz.timezone('Asia/Kolkata')
day1 = datetime(2015, 10, 28, 2, 1, 1)
day1_tz_start = tz_start.localize(day1)
day2 = datetime(2020, 2, 25, 0, 0, 0)
day2_tz_end = tz_end.localize(day2)

day_diff_in_days = day2_tz_end - day1_tz_start
day_diff_in_weeks = day_diff_in_days.days // 7
day_diff_in_hours = day_diff_in_days.seconds // 3600 + day_diff_in_days.days * 24
day_diff_in_minuntes = day_diff_in_days.seconds // 60 + day_diff_in_hours * 60
day_diff_in_secs = day_diff_in_days.seconds + day_diff_in_minuntes * 60

days = day_diff_in_days.days
hours = day_diff_in_days.seconds // 3600
minutes = (day_diff_in_days.seconds % 3600) / 60
seconds = (day_diff_in_days.seconds % 3600) % 60
# print 'days:',days, ' hours:',hours,' minutes:',minutes, ' seconds:' ,seconds

# print day_diff_in_days.days
# print day_diff_in_weeks
# print day_diff_in_hours
# print day_diff_in_minuntes
# print day_diff_in_secs

# to_day=datetime.now()
# print to_day
# print 'Next Business day',to_day + BDay()
# print 'Next Month Business begin',to_day +BMonthBegin()
# print 'Next Business month close', to_day +BMonthEnd()
# print 'Next Qtr Business',to_day + BQuarterBegin()

# show next x week monday dates/weekdays
# print pd.date_range(to_day,periods=10,freq='W-MON')



# show next x business month dates/weekdays
# print pd.date_range(to_day,periods=10,freq=BMonthBegin())
# show next x business month end dates/weekdays
# print pd.date_range(to_day,periods=10,freq=BMonthEnd())

# show next x Q  end dates/weekdays [ bug fo rnext quarter]
# print pd.date_range(to_day,periods=10,freq=BQuarterBegin())
# print pd.date_range(to_day,periods=10,freq=BQuarterEnd())







y = tt._transition_info
# print y[0]
today = datetime(2015, 11, 8)
x = tt._utc_transition_times
# print x
pos_neg, second1 = convert_timedelta(y[0][0])
# print pos_neg,second1
# print x,y
old_dst = timedelta(0)
for xx in range(2, 5):  # len(x)):
	print x[xx], y[xx], y[xx][1]
	now_dst = y[xx][1]
	# old_dst = now_dst
	# print 'start', now_dst
	if now_dst == timedelta(0):
		print 'naren', old_dst
		if y[xx][0] > timedelta(0):
			print '1', (x[xx] + y[xx][0] + old_dst).strftime('%A %d, %B %Y %H:%M'), y[xx][1].seconds / 3600, y[xx][
				2], convert_timedelta(y[xx][0])

	else:
		old_dst = now_dst
		# print 'not equal'
		print (x[xx] + y[xx][0] - y[xx][1]).strftime('%A %d, %B %Y %H:%M'), y[xx][1].seconds / 3600, y[xx][
			2], convert_timedelta(y[xx][0])
	print '------------------------------------'
