#!/usr/bin/env python
__author__ = 'naren'
import swisseph as swe
import datetime
import math
import birthchart
from astro import constants

swe.set_ephe_path('astro/data/ephemeris/')


def date_convert(jul_number):
    temp = swe.revjul(jul_number)
    year = temp[0]
    month = temp[1]
    day = temp[2]
    min_temp, hour = math.modf(temp[3])
    sec_temp, min = math.modf(min_temp * 60)
    sub_sec, sec = math.modf(sec_temp * 60)
    return datetime.datetime(year, month, day, int(hour), int(min), int(sec))


print 'Next Solar Eclipse global'
print '------------------------'
now = swe.julday(2017, 8, 1)
time_zone = -0  # we have to look up time zone from lat/long

for i in range(1):
    res_global = swe.sol_eclipse_when_glob(now)
    print 'global', res_global
    t_start = res_global[1][0]
    lat_long = swe.sol_eclipse_where(t_start)
    print 'where', lat_long
    longitude = lat_long[1][0]
    latitude = lat_long[1][1]
    res_how = swe.sol_eclipse_how(res_global[1][0], longitude, latitude)
    print 'how', res_how
    ecl_central = True
    ecl_central_mask = int('00000001', 2)
    ecl_type = res_how[0][0] & ecl_central_mask
    if ecl_type == 1:
        ecl_central = True
        print 'Eclipse Central'
    ecl_noncentral_mask = int('00000010', 2)
    ecl_type = res_how[0][0] & ecl_noncentral_mask
    if ecl_type == 2:
        ecl_central = False
        print 'Eclipse Non Central'
    eclipse_total_mask = int('00000100', 2)
    ecl_type = res_how[0][0] & eclipse_total_mask
    if ecl_type == 4:
        print 'Eclipse Total'
        print 'Start         :', date_convert(res_global[1][2]) + datetime.timedelta(hours=time_zone)
        print 'Start Totality:', date_convert(res_global[1][4]) + datetime.timedelta(hours=time_zone)
        if ecl_central:
            print 'Centerline S  :', date_convert(res_global[1][6]) + datetime.timedelta(hours=time_zone)
        print 'Max           :', date_convert(res_global[1][0]) + datetime.timedelta(hours=time_zone)
        if ecl_central:
            print 'Centerline End:', date_convert(res_global[1][7]) + datetime.timedelta(hours=time_zone)
        print 'End Totality  :', date_convert(res_global[1][5]) + datetime.timedelta(hours=time_zone)
        print 'End           :', date_convert(res_global[1][3]) + datetime.timedelta(hours=time_zone)
        print 'Duration      :', date_convert(res_global[1][3]) - date_convert(res_global[1][2])
        print 'Type:          ', res_global[0][0], bin(res_global[0][0])
        print 'Type: Max place', res_how[0][0], bin(res_how[0][0])
    eclipse_annualar = int('00001000', 2)
    ecl_type = res_how[0][0] & eclipse_annualar
    if ecl_type == 8:
        print 'Eclipse Annular'
        ecl_start = res_global[1][0]  # res_global[1][0]
        ecl_end = res_global[1][0]
        if res_global[1][2] > 0:
            ecl_start = res_global[1][2]
            print 'Start         :', date_convert(res_global[1][2]) + datetime.timedelta(hours=time_zone)
        if res_global[1][4] > 0:
            print 'Start Totality:', date_convert(res_global[1][4]) + datetime.timedelta(hours=time_zone)
            if ecl_start >= res_global[1][4]:
                ecl_start = res_global[1][4]
        if res_global[1][6] > 0:
            print 'Centerline S  :', date_convert(res_global[1][6]) + datetime.timedelta(hours=time_zone)
            if ecl_start > res_global[1][6]:
                ecl_start = res_global[1][6]
        print 'Max           :', date_convert(res_global[1][0]) + datetime.timedelta(hours=time_zone)
        if res_global[1][7] > 0:
            print 'Centerline End:', date_convert(res_global[1][7]) + datetime.timedelta(hours=time_zone)
            ecl_end = res_global[1][7]
        if res_global[1][5] > 0:
            print 'End Totality  :', date_convert(res_global[1][5]) + datetime.timedelta(hours=time_zone)
            if ecl_end < res_global[1][5]:
                ecl_end = res_global[1][5]
        if res_global[1][3] > 0:
            print 'End           :', date_convert(res_global[1][3]) + datetime.timedelta(hours=time_zone)
            if ecl_end < res_global[1][3]:
                ecl_end = res_global[1][3]
        print ecl_end, ecl_start
        print 'Duration      :', date_convert(ecl_end) - date_convert(ecl_start)
        print 'Type:          ', res_global[0][0], bin(res_global[0][0])
        print 'Type: Max place', res_how[0][0], bin(res_how[0][0])
    eclipse_partial = int('0010000', 2)
    ecl_type = res_how[0][0] & eclipse_partial
    if ecl_type == 16:
        print 'Eclipse Partial'
        ecl_start = res_global[1][0]  # res_global[1][0]
        ecl_end = res_global[1][0]
        if res_global[1][2] > 0:
            ecl_start = res_global[1][2]
            print 'Start         :', date_convert(res_global[1][2]) + datetime.timedelta(hours=time_zone)
        if res_global[1][4] > 0:
            print 'Start Totality:', date_convert(res_global[1][4]) + datetime.timedelta(hours=time_zone)
            if ecl_start >= res_global[1][4]:
                ecl_start = res_global[1][4]
        if res_global[1][6] > 0:
            print 'Centerline S  :', date_convert(res_global[1][6]) + datetime.timedelta(hours=time_zone)
            if ecl_start > res_global[1][6]:
                ecl_start = res_global[1][6]
        print 'Max           :', date_convert(res_global[1][0]) + datetime.timedelta(hours=time_zone)
        if res_global[1][7] > 0:
            print 'Centerline End:', date_convert(res_global[1][7]) + datetime.timedelta(hours=time_zone)
            ecl_end = res_global[1][7]
        if res_global[1][5] > 0:
            print 'End Totality  :', date_convert(res_global[1][5]) + datetime.timedelta(hours=time_zone)
            if ecl_end < res_global[1][5]:
                ecl_end = res_global[1][5]
        if res_global[1][3] > 0:
            print 'End           :', date_convert(res_global[1][3]) + datetime.timedelta(hours=time_zone)
            if ecl_end < res_global[1][3]:
                ecl_end = res_global[1][3]
        print ecl_end, ecl_start
        print 'Duration      :', date_convert(ecl_end) - date_convert(ecl_start)
        print 'Type:          ', res_global[0][0], bin(res_global[0][0])
        print 'Type: Max place', res_how[0][0], bin(res_how[0][0])
    eclipse_ann_total = int('0100000', 2)
    ecl_type = res_how[0][0] & eclipse_ann_total
    if ecl_type == 32:
        print 'Eclipse Annular-Total'

    print 'Soros Cycle: ', int(lat_long[2][9])
    print 'Soros number:', int(lat_long[2][10])
    print 'Max covered %', int(lat_long[2][2] * 100)
    print 'Sun Alt', lat_long[2][5]
    print 'Sun Azm', (lat_long[2][4] + 180) % 360
    pos_p = swe.calc_ut(res_global[1][0], 0)
    signs = birthchart.natal_planet_signs(pos_p)
    print 'Sun  position', pos_p[0], 'Sun is in', constants.SIGN_ZODIAC[signs[0]]
    pos_p = swe.calc_ut(res_global[1][0], 1)
    signs = birthchart.natal_planet_signs(pos_p)
    print 'Moon position', pos_p[0], 'Moon is in', constants.SIGN_ZODIAC[signs[0]]
    print 'Where -Latitue  :', latitude
    print 'Where -Longitude:', longitude
    print 'Magnitude       :', lat_long[2][1]
    now = res_global[1][0] + 30
    # print i
# LOCAL CITY INFO
# input = date, lat/long, time zone
# or City number - to look up correct time zone info
lat = 36.666  # 32.95
longitude = -87.67  # -118.1
# now = swe.julday(2017, 8, 16)
now = res_global[1][0] - 1
time_zone = -7

print '------------------------'
print 'Next Eclipse for a given geographical position: Lat/long'
res = swe.sol_eclipse_when_loc(now, longitude, lat)
res_how = swe.sol_eclipse_how(res[1][0], longitude, lat)
print res
print res_how
ecl_central = int('00000001', 2)
ecl_type = res_how[0][0] & ecl_central
if ecl_type == 1:
    print 'Eclipse Central'
ecl_noncentral = int('00000010', 2)
ecl_type = res_how[0][0] & ecl_noncentral
if ecl_type == 2:
    print 'Eclipse Non Central'
eclipse_total = int('00000100', 2)
ecl_type = res_how[0][0] & eclipse_total
if ecl_type == 4:
    print 'Eclipse Total'
    print 'Start', date_convert(res[1][1]) + datetime.timedelta(hours=time_zone)
    print '1    ', date_convert(res[1][2]) + datetime.timedelta(hours=time_zone)
    print 'Max  ', date_convert(res[1][0]) + datetime.timedelta(hours=time_zone)
    print '2    ', date_convert(res[1][3]) + datetime.timedelta(hours=time_zone)
    print 'End  ', date_convert(res[1][4]) + datetime.timedelta(hours=time_zone)
    print 'Duration', date_convert(res[1][4]) - date_convert(res[1][1])
    print 'Duration', date_convert(res[1][3]) - date_convert(res[1][2])
    print 'Type:               ', res[0][0], bin(res[0][0])
    print 'Type: in Los Angeles', res_how[0][0], bin(res_how[0][0])
eclipse_annual = int('00001000', 2)
ecl_type = res_how[0][0] & eclipse_annual
if ecl_type == 8:
    print 'Eclipse Annual'
    print 'Start', date_convert(res[1][1]) + datetime.timedelta(hours=time_zone)
    print '1    ', date_convert(res[1][2]) + datetime.timedelta(hours=time_zone)
    print 'Max  ', date_convert(res[1][0]) + datetime.timedelta(hours=time_zone)
    print '2    ', date_convert(res[1][3]) + datetime.timedelta(hours=time_zone)
    print 'End  ', date_convert(res[1][4]) + datetime.timedelta(hours=time_zone)
    print 'Duration', date_convert(res[1][4]) - date_convert(res[1][1])
    print 'Duration', date_convert(res[1][3]) - date_convert(res[1][2])
    print 'Type:               ', res[0][0], bin(res[0][0])
    print 'Type: in Los Angeles', res_how[0][0], bin(res_how[0][0])
eclipse_partial = int('0010000', 2)
ecl_type = res_how[0][0] & eclipse_partial
if ecl_type == 16:
    print 'Eclipse Partial'
    print 'Start', date_convert(res[1][1]) + datetime.timedelta(hours=time_zone)
    # print '1    ', date_convert(res[1][2]) + datetime.timedelta(hours=time_zone)
    print 'Max  ', date_convert(res[1][0]) + datetime.timedelta(hours=time_zone)
    # print '2    ', date_convert(res[1][3]) + datetime.timedelta(hours=time_zone)
    print 'End  ', date_convert(res[1][4]) + datetime.timedelta(hours=time_zone)
    print 'Duration', date_convert(res[1][4]) - date_convert(res[1][1])
    #print 'Duration', date_convert(res[1][3]) - date_convert(res[1][2])
    print 'Type:               ', res[0][0], bin(res[0][0])
print 'Type: in Los Angeles', res_how[0][0], bin(res_how[0][0])
eclipse_ann_total = int('0100000', 2)
ecl_type = res_how[0][0] & eclipse_ann_total
if ecl_type == 32:
    print 'Eclipse Annular-Total'
    print 'Start', date_convert(res[1][1]) + datetime.timedelta(hours=time_zone)
    print '1    ', date_convert(res[1][2]) + datetime.timedelta(hours=time_zone)
    print 'Max  ', date_convert(res[1][0]) + datetime.timedelta(hours=time_zone)
    print '2    ', date_convert(res[1][3]) + datetime.timedelta(hours=time_zone)
    print 'End  ', date_convert(res[1][4]) + datetime.timedelta(hours=time_zone)
    print 'Duration', date_convert(res[1][4]) - date_convert(res[1][1])
    print 'Duration', date_convert(res[1][3]) - date_convert(res[1][2])
    print 'Type:               ', res[0][0], bin(res[0][0])
    print 'Type: in Los Angeles', res_how[0][0], bin(res_how[0][0])
print 'Soros Cycle: ', int(res[2][9])
print 'Soros number:', int(res[2][10])
print 'Max covered %', int(res[2][2] * 100)
print 'Sun Alt', res[2][5]
print 'Sun Azm', (res[2][4] + 180) % 360
pos_p = swe.calc_ut(res[1][0], 0)
signs = birthchart.natal_planet_signs(pos_p)
print 'Sun  position', pos_p[0], 'Sun is in', constants.SIGN_ZODIAC[signs[0]]
pos_p = swe.calc_ut(res[1][0], 1)
signs = birthchart.natal_planet_signs(pos_p)
print 'Moon position', pos_p[0], 'Moon is in', constants.SIGN_ZODIAC[signs[0]]

pos_p = swe.calc_ut(res[1][0], 0)
print 'Sun  position', pos_p[0]
pos_p = swe.calc_ut(res[1][0], 1)
print 'Moon position', pos_p[0]
print '------------------------'