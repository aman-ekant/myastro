#!/usr/bin/env python
__author__ = 'naren'
import swisseph as swe
import datetime
import math
import birthchart
from astro import constants

swe.set_ephe_path('../ephemeris/')


def date_convert(jul_number):
    temp = swe.revjul(jul_number)
    year = temp[0]
    month = temp[1]
    day = temp[2]
    min_temp, hour = math.modf(temp[3])
    sec_temp, min = math.modf(min_temp * 60)
    sub_sec, sec = math.modf(sec_temp * 60)
    return datetime.datetime(year, month, day, int(hour), int(min), int(sec))


# ###lunar eclipses
print 'When next Lunar Eclipse'
print '------------------------'
now = swe.julday(2016, 3, 23)
time_zone = 0  # we have to look up time zone from lat/long
res = swe.lun_eclipse_when(now)
res_how = swe.lun_eclipse_how(res[1][0], 139.7, 35.68)
print res
print res_how
eclip_time = swe.revjul(res[1][0])  # utc
# print len(res[1]),res[0],res[1],eclip_time,bin(res[0][0])
ecl_central = int('00000001', 2)
central = res[0][0] & ecl_central
if central == 1:
    print 'Eclipse Central'
ecl_noncentral = int('00000010', 2)
central = res[0][0] & ecl_noncentral
if central == 2:
    print 'Eclipse Non Central'
eclipse_total = int('00000100', 2)
central = res[0][0] & eclipse_total
if central == 4:
    print 'Eclipse Total'
    print 'Start        ', date_convert(res[1][6]) + datetime.timedelta(hours=time_zone)
    print 'Start partial', date_convert(res[1][2]) + datetime.timedelta(hours=time_zone)
    print 'Start Total  ', date_convert(res[1][4]) + datetime.timedelta(hours=time_zone)
    print 'Max          ', date_convert(res[1][0]) + datetime.timedelta(hours=time_zone)
    print 'End Total    ', date_convert(res[1][5]) + datetime.timedelta(hours=time_zone)
    print 'End partial  ', date_convert(res[1][3]) + datetime.timedelta(hours=time_zone)
    print 'End          ', date_convert(res[1][7]) + datetime.timedelta(hours=time_zone)
    print 'Duration Penumbral', date_convert(res[1][7]) - date_convert(res[1][6])
    print 'Duration Umbral   ', date_convert(res[1][3]) - date_convert(res[1][2])
    print 'Total             ', date_convert(res[1][5]) - date_convert(res[1][4])

eclipse_annualar = int('00001000', 2)
central = res[0][0] & eclipse_annualar
if central == 8:
    print 'Eclipse Annular'
eclipse_partial = int('0010000', 2)
central = res[0][0] & eclipse_partial
if central == 16:
    print 'Eclipse Partial'
    print 'Start        ', date_convert(res[1][6]) + datetime.timedelta(hours=time_zone)
    print 'Start partial', date_convert(res[1][2]) + datetime.timedelta(hours=time_zone)
    print 'Max          ', date_convert(res[1][0]) + datetime.timedelta(hours=time_zone)
    print 'End partial  ', date_convert(res[1][3]) + datetime.timedelta(hours=time_zone)
    print 'End          ', date_convert(res[1][7]) + datetime.timedelta(hours=time_zone)
    print 'Duration Penumbral', date_convert(res[1][7]) - date_convert(res[1][6])
    print 'Duration Umbral   ', date_convert(res[1][3]) - date_convert(res[1][2])
eclipse_ann_total = int('0100000', 2)
central = res[0][0] & eclipse_ann_total
if central == 32:
    print 'Eclipse Penumbral'
eclipse_ann_total = int('1000000', 2)
central = res[0][0] & eclipse_ann_total
if central == 64:
    print 'Eclipse Penumbral'
    print 'Start', date_convert(res[1][6]) + datetime.timedelta(hours=time_zone)
    print 'Max  ', date_convert(res[1][0]) + datetime.timedelta(hours=time_zone)
    print 'End  ', date_convert(res[1][7]) + datetime.timedelta(hours=time_zone)
    print 'Duration Penumbral', date_convert(res[1][7]) - date_convert(res[1][6])
print 'Soros Cycle        :', int(res_how[1][9])
print 'Soros number       :', int(res_how[1][10])
print 'Magnitude Umbral   :', res_how[1][0]
print 'Magnitude PreUmbral:', res_how[1][1]

pos_p = swe.calc_ut(res[1][0], 0)
signs = birthchart.natal_planet_signs(pos_p)
print 'Sun  position', pos_p[0], constants.SIGN_ZODIAC[signs[0]]
pos_p = swe.calc_ut(res[1][0], 1)
signs = birthchart.natal_planet_signs(pos_p)
print 'Moon position', pos_p[0], constants.SIGN_ZODIAC[signs[0]]
lat = 34.03
longitude = -118.25
res_how = swe.lun_eclipse_how(res[1][0], longitude, lat)
print res_how
now = res[1][0] - 1
# now = swe.julday(2014, 4, 1)
time_zone = -8
print '------------------------'
print 'Next Eclipse for a given geographical position: Los Angeles'###############################################
res = swe.lun_eclipse_when_loc(now, longitude, lat)
res_how = swe.lun_eclipse_how(res[1][0], longitude, lat)
if res[1][8] > 0:
    moon_rise = res[1][8]
else:
    now1 = res[1][0] - 1  # swe.julday(2016, 3, 23)
    # rsmi=1 rise,2 set
    rise = swe.rise_trans(now1, 1, longitude, lat, rsmi=1)
    moon_rise = rise[1][0]
if res[1][9] > 0:
    moon_set = res[1][9]
else:
    now1 = res[1][0]  # swe.julday(2016, 3, 23)
    rise = swe.rise_trans(now1, 1, longitude, lat, rsmi=2)
    moon_set = rise[1][0]
print res
print res_how
eclipse_total = int('00000100', 2)
central = res[0][0] & eclipse_total
if central == 4:
    print 'Eclipse Total'
    print 'Moon Rise    ', date_convert(moon_rise) + datetime.timedelta(hours=time_zone)
    if moon_rise < res[1][6]:
        print 'Start        ', date_convert(res[1][6]) + datetime.timedelta(hours=time_zone)
        duration_start = res[1][6]
    else:
        duration_start = moon_rise
    if moon_rise < res[1][2]:
        print 'Start partial', date_convert(res[1][2]) + datetime.timedelta(hours=time_zone)
        duration_start_partial = res[1][2]
    else:
        duration_start_partial = moon_rise
    if moon_rise < res[1][4]:
        print 'Start Total  ', date_convert(res[1][4]) + datetime.timedelta(hours=time_zone)
        duration_start_total = res[1][4]
    else:
        duration_start_total = moon_rise
    print 'Max          ', date_convert(res[1][0]) + datetime.timedelta(hours=time_zone)
    if res[1][5] > 0 and moon_set > res[1][5]:
        print 'End Total    ', date_convert(res[1][5]) + datetime.timedelta(hours=time_zone)
        duration_end_total = res[1][5]
    else:
        duration_end_total = moon_set
    if res[1][3] > 0 and moon_set > res[1][3]:
        print 'End partial  ', date_convert(res[1][3]) + datetime.timedelta(hours=time_zone)
        duration_end_partial = res[1][3]
    else:
        duration_end_partial = moon_set
    if moon_set > res[1][7] and res[1][7] > 0:
        print 'End          ', date_convert(res[1][7]) + datetime.timedelta(hours=time_zone)
        duration_end = res[1][7]
    else:
        duration_end = moon_set
    print 'Moon Set     ', date_convert(moon_set) + datetime.timedelta(hours=time_zone)
    print 'Duration Penumbral', date_convert(duration_end) - date_convert(duration_start)
    print 'Duration Umbral   ', date_convert(duration_end_partial) - date_convert(duration_start_partial)
    print 'Duration Total    ', date_convert(duration_end_total) - date_convert(duration_start_total)

eclipse_annualar = int('00001000', 2)
central = res[0][0] & eclipse_annualar
if central == 8:
    print 'Eclipse Annular'
eclipse_partial = int('0010000', 2)
central = res[0][0] & eclipse_partial
if central == 16:
    print 'Eclipse Partial'
    print 'Moon Rise    ', date_convert(moon_rise) + datetime.timedelta(hours=time_zone)
    if moon_rise < res[1][6]:
        print 'Start        ', date_convert(res[1][6]) + datetime.timedelta(hours=time_zone)
        duration_start = res[1][6]
    else:
        duration_start = moon_rise
    if moon_rise < res[1][2]:
        print 'Start partial', date_convert(res[1][2]) + datetime.timedelta(hours=time_zone)
        duration_start_partial = res[1][2]
    else:
        duration_start_partial = moon_rise
    print 'Max          ', date_convert(res[1][0]) + datetime.timedelta(hours=time_zone)
    if res[1][3] > 0 and moon_set > res[1][3]:
        print 'End partial  ', date_convert(res[1][9]) + datetime.timedelta(hours=time_zone)
        duration_end_partial = res[1][3]
    else:
        duration_end_partial = moon_set
    if moon_set > res[1][7] and res[1][7] > 0:
        print 'End          ', date_convert(res[1][7]) + datetime.timedelta(hours=time_zone)
        duration_end = res[1][7]
    else:
        duration_end = moon_set
    print 'Moon Set     ', date_convert(moon_set) + datetime.timedelta(hours=time_zone)
    print 'Duration Penumbral', date_convert(duration_end) - date_convert(duration_start)
    print 'Duration Umbral   ', date_convert(duration_end_partial) - date_convert(duration_start_partial)
eclipse_ann_total = int('0100000', 2)
central = res[0][0] & eclipse_ann_total
if central == 32:
    print 'Eclipse Penumbral'
eclipse_ann_total = int('1000000', 2)
central = res[0][0] & eclipse_ann_total
if central == 64:
    print 'Eclipse Penumbral'
    print 'Moon Rise    ', date_convert(moon_rise) + datetime.timedelta(hours=time_zone)
    if moon_rise < res[1][6]:
        print 'Start        ', date_convert(res[1][6]) + datetime.timedelta(hours=time_zone)
        duration_start = res[1][6]
    else:
        duration_start = moon_rise
    if moon_rise < res[1][2]:
        print 'Start partial', date_convert(res[1][2]) + datetime.timedelta(hours=time_zone)
        duration_start_partial = res[1][2]
    else:
        duration_start_partial = moon_rise
    print 'Max          ', date_convert(res[1][0]) + datetime.timedelta(hours=time_zone)
    if res[1][3] > 0 and moon_set > res[1][3]:
        print 'End partial  ', date_convert(res[1][9]) + datetime.timedelta(hours=time_zone)
        duration_end_partial = res[1][3]
    else:
        duration_end_partial = moon_set
    if moon_set > res[1][7] and res[1][7] > 0:
        print 'End          ', date_convert(res[1][7]) + datetime.timedelta(hours=time_zone)
        duration_end = res[1][7]
    else:
        duration_end = moon_set
    print 'Moon Set     ', date_convert(moon_set) + datetime.timedelta(hours=time_zone)
    print 'Duration Penumbral', date_convert(duration_end) - date_convert(duration_start)
    #print 'Duration Umbral   ', date_convert(duration_end_partial) - date_convert(duration_start_partial)

print 'Moon Az', (res[2][4] + 180) % 360
print 'Moon Alt', res[2][5]
pos_p = swe.calc_ut(res[1][0], 0)
signs = birthchart.natal_planet_signs(pos_p)
print 'Sun  position', pos_p[0], constants.SIGN_ZODIAC[signs[0]]
pos_p = swe.calc_ut(res[1][0], 1)
signs = birthchart.natal_planet_signs(pos_p)
print 'Moon position', pos_p[0], constants.SIGN_ZODIAC[signs[0]]
print 'Soros Cycle: ', int(res_how[1][9])
print 'Soros number:', int(res_how[1][10])
print 'Magnitude Umbral   ', res_how[1][0]
print 'Magnitude PreUmbral   ', res_how[1][1]

print '------------------------'