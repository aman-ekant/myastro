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

def solar(year, month, day, time_zone, location_latitude, location_longitude):
    solaar = {}
    now = swe.julday(year, month, day)
    for i in range(1):
        res_global = swe.sol_eclipse_when_glob(now)
        #print 'global', res_global
        t_start = res_global[1][0]
        lat_long = swe.sol_eclipse_where(t_start)
        #print 'where', lat_long
        longitude = lat_long[1][0]
        latitude = lat_long[1][1]
        res_how = swe.sol_eclipse_how(res_global[1][0], longitude, latitude)
        #print 'how', res_how
        ecl_central = True
        ecl_central_mask = int('00000001', 2)
        ecl_type = res_how[0][0] & ecl_central_mask
        if ecl_type == 1:
            ecl_central = True
            ecl_central_or_not = 'Eclipse Central'
        ecl_noncentral_mask = int('00000010', 2)
        ecl_type = res_how[0][0] & ecl_noncentral_mask
        if ecl_type == 2:
            ecl_central = False
            ecl_central_or_not = 'Eclipse Non Central'
        eclipse_total_mask = int('00000100', 2)
        ecl_type = res_how[0][0] & eclipse_total_mask
        if ecl_type == 4:
            Type ='Eclipse Total'
            start = (date_convert(res_global[1][2]) + datetime.timedelta(hours=time_zone))
            start_totality = (date_convert(res_global[1][4]) + datetime.timedelta(hours=time_zone))
            if ecl_central:
                centerline_start = (date_convert(res_global[1][6]) + datetime.timedelta(hours=time_zone))
            maxi = (date_convert(res_global[1][0]) + datetime.timedelta(hours=time_zone))
            if ecl_central:
                centerline_end = (date_convert(res_global[1][7]) + datetime.timedelta(hours=time_zone))
            end_totality = (date_convert(res_global[1][5]) + datetime.timedelta(hours=time_zone))
            end = (date_convert(res_global[1][3]) + datetime.timedelta(hours=time_zone))
            duration = (date_convert(res_global[1][3]) - date_convert(res_global[1][2]))
            #print 'Type:          ', res_global[0][0], bin(res_global[0][0])
            #print 'Type: Max place', res_how[0][0], bin(res_how[0][0])
        eclipse_annualar = int('00001000', 2)
        ecl_type = res_how[0][0] & eclipse_annualar
        if ecl_type == 8:
            Type = 'Eclipse Annular'
            ecl_start = res_global[1][0]  # res_global[1][0]
            ecl_end = res_global[1][0]
            if res_global[1][2] > 0:
                ecl_start = res_global[1][2]
                start = (date_convert(res_global[1][2]) + datetime.timedelta(hours=time_zone))
            if res_global[1][4] > 0:
                start_totality = (date_convert(res_global[1][4]) + datetime.timedelta(hours=time_zone))
                if ecl_start >= res_global[1][4]:
                    ecl_start = res_global[1][4]
            if res_global[1][6] > 0:
                centerline_start = (date_convert(res_global[1][6]) + datetime.timedelta(hours=time_zone))
                if ecl_start > res_global[1][6]:
                    ecl_start = res_global[1][6]
            maxi = (date_convert(res_global[1][0]) + datetime.timedelta(hours=time_zone))
            if res_global[1][7] > 0:
                centerline_end = (date_convert(res_global[1][7]) + datetime.timedelta(hours=time_zone))
                ecl_end = res_global[1][7]
            if res_global[1][5] > 0:
                end_totality = (date_convert(res_global[1][5]) + datetime.timedelta(hours=time_zone))
                if ecl_end < res_global[1][5]:
                    ecl_end = res_global[1][5]
            if res_global[1][3] > 0:
                end = (date_convert(res_global[1][3]) + datetime.timedelta(hours=time_zone))
                if ecl_end < res_global[1][3]:
                    ecl_end = res_global[1][3]
            #print ecl_end, ecl_start
            duration = (date_convert(ecl_end) - date_convert(ecl_start))
            #print 'Type:          ', res_global[0][0], bin(res_global[0][0])
            #print 'Type: Max place', res_how[0][0], bin(res_how[0][0])
        eclipse_partial = int('0010000', 2)
        ecl_type = res_how[0][0] & eclipse_partial
        if ecl_type == 16:
            Type = 'Eclipse Partial'
            ecl_start = res_global[1][0]  # res_global[1][0]
            ecl_end = res_global[1][0]
            if res_global[1][2] > 0:
                ecl_start = res_global[1][2]
                start = (date_convert(res_global[1][2]) + datetime.timedelta(hours=time_zone))
            if res_global[1][4] > 0:
                start_totality = (date_convert(res_global[1][4]) + datetime.timedelta(hours=time_zone))
                if ecl_start >= res_global[1][4]:
                    ecl_start = res_global[1][4]
            if res_global[1][6] > 0:
                centerline_start = (date_convert(res_global[1][6]) + datetime.timedelta(hours=time_zone))
                if ecl_start > res_global[1][6]:
                    ecl_start = res_global[1][6]
            maxi = (date_convert(res_global[1][0]) + datetime.timedelta(hours=time_zone))
            if res_global[1][7] > 0:
                centerline_end = (date_convert(res_global[1][7]) + datetime.timedelta(hours=time_zone))
                ecl_end = res_global[1][7]
            if res_global[1][5] > 0:
                end_totality = (date_convert(res_global[1][5]) + datetime.timedelta(hours=time_zone))
                if ecl_end < res_global[1][5]:
                    ecl_end = res_global[1][5]
            if res_global[1][3] > 0:
                end = (date_convert(res_global[1][3]) + datetime.timedelta(hours=time_zone))
                if ecl_end < res_global[1][3]:
                    ecl_end = res_global[1][3]
            #print ecl_end, ecl_start
            duration = (date_convert(ecl_end) - date_convert(ecl_start))
            #print 'Type:          ', res_global[0][0], bin(res_global[0][0])
            #print 'Type: Max place', res_how[0][0], bin(res_how[0][0])
        eclipse_ann_total = int('0100000', 2)
        ecl_type = res_how[0][0] & eclipse_ann_total
        if ecl_type == 32:
            Type = 'Eclipse Annular-Total'

        soros_cycle = int(lat_long[2][9])
        soros_number = int(lat_long[2][10])
        max_covered = int(lat_long[2][2] * 100)
        sun_alt = lat_long[2][5]
        sun_azm = ((lat_long[2][4] + 180) % 360)
        pos_p = swe.calc_ut(res_global[1][0], 0)
        signs = birthchart.natal_planet_signs(pos_p)
        sun_pos =  pos_p[0]
        sun_zodiac =  constants.SIGN_ZODIAC[signs[0]]
        pos_p = swe.calc_ut(res_global[1][0], 1)
        signs = birthchart.natal_planet_signs(pos_p)
        moon_pos = pos_p[0]
        moon_zodiac = constants.SIGN_ZODIAC[signs[0]]
        #print 'Where -Latitue  :', latitude
        #print 'Where -Longitude:', longitude
        magnii = lat_long[2][1]
        now = res_global[1][0] + 30  
    solar_eclipse = {'ecl_central_or_not' : ecl_central_or_not, 'soros_cycle' : soros_cycle,
                            'soros_number' : soros_number, 'max_covered' : max_covered, 'sun_alt' : sun_alt, 'sun_azm' : sun_azm,
                            'sun_pos' : sun_pos, 'sun_zodiac' : sun_zodiac, 'moon_pos' : moon_pos, 'moon_zodiac' : moon_zodiac,
                            'latii' : latitude, 'longii' : longitude, 'magnii' : magnii, 'start' : start, 'start_totality' : start_totality,
                            'centerline_start' : centerline_start, 'max' : maxi, 'centerline_end' : centerline_end,
                            'end_totality' : end_totality, 'end' : end, 'duration' : duration, 'Type' : Type}

    return solar_eclipse

    
def solarbypos(year, month, day, time_zone, location_latitude, location_longitude):    # print i
    now = swe.julday(year, month, day)
    res_global = swe.sol_eclipse_when_glob(now)
    now = res_global[1][0] - 1
    res = swe.sol_eclipse_when_loc(now, location_longitude, location_latitude)
    res_how = swe.sol_eclipse_how(res[1][0], location_longitude, location_latitude)
    #print res
    #print res_how
    ecl_central = int('00000001', 2)
    ecl_type = res_how[0][0] & ecl_central
    if ecl_type == 1:
        ecl_central_or_not = 'Eclipse Central'
    ecl_noncentral = int('00000010', 2)
    ecl_type = res_how[0][0] & ecl_noncentral
    if ecl_type == 2:
        ecl_central_or_not = 'Eclipse Non Central'
    eclipse_total = int('00000100', 2)
    ecl_type = res_how[0][0] & eclipse_total
    if ecl_type == 4:
        Type = 'Eclipse Total'
        start = date_convert(res[1][1]) + datetime.timedelta(hours=time_zone)
        print '1    ', date_convert(res[1][2]) + datetime.timedelta(hours=time_zone)
        maxi = date_convert(res[1][0]) + datetime.timedelta(hours=time_zone)
        print '2    ', date_convert(res[1][3]) + datetime.timedelta(hours=time_zone)
        end = date_convert(res[1][4]) + datetime.timedelta(hours=time_zone)
        print 'Duration', date_convert(res[1][4]) - date_convert(res[1][1])
        print 'Duration', date_convert(res[1][3]) - date_convert(res[1][2])
        print 'Type:               ', res[0][0], bin(res[0][0])
        print 'Type: in Los Angeles', res_how[0][0], bin(res_how[0][0])
    eclipse_annual = int('00001000', 2)
    ecl_type = res_how[0][0] & eclipse_annual
    if ecl_type == 8:
        Type = 'Eclipse Annual'
        start = date_convert(res[1][1]) + datetime.timedelta(hours=time_zone)
        print '1    ', date_convert(res[1][2]) + datetime.timedelta(hours=time_zone)
        maxi = date_convert(res[1][0]) + datetime.timedelta(hours=time_zone)
        print '2    ', date_convert(res[1][3]) + datetime.timedelta(hours=time_zone)
        end = date_convert(res[1][4]) + datetime.timedelta(hours=time_zone)
        print 'Duration', date_convert(res[1][4]) - date_convert(res[1][1])
        print 'Duration', date_convert(res[1][3]) - date_convert(res[1][2])
        print 'Type:   ', res[0][0], bin(res[0][0])
        print 'Type: in Los Angeles', res_how[0][0], bin(res_how[0][0])
    eclipse_partial = int('0010000', 2)
    ecl_type = res_how[0][0] & eclipse_partial
    if ecl_type == 16:
        Type = 'Eclipse Partial'
        start = date_convert(res[1][1]) + datetime.timedelta(hours=time_zone)
        # print '1    ', date_convert(res[1][2]) + datetime.timedelta(hours=time_zone)
        maxi = date_convert(res[1][0]) + datetime.timedelta(hours=time_zone)
        # print '2    ', date_convert(res[1][3]) + datetime.timedelta(hours=time_zone)
        end = date_convert(res[1][4]) + datetime.timedelta(hours=time_zone)
        print 'Duration', date_convert(res[1][4]) - date_convert(res[1][1])
        #print 'Duration', date_convert(res[1][3]) - date_convert(res[1][2])
        print 'Type:               ', res[0][0], bin(res[0][0])
    print 'Type: in Los Angeles', res_how[0][0], bin(res_how[0][0])
    eclipse_ann_total = int('0100000', 2)
    ecl_type = res_how[0][0] & eclipse_ann_total
    if ecl_type == 32:
        Type = 'Eclipse Annular-Total'
        start = date_convert(res[1][1]) + datetime.timedelta(hours=time_zone)
        print '1    ', date_convert(res[1][2]) + datetime.timedelta(hours=time_zone)
        maxi = date_convert(res[1][0]) + datetime.timedelta(hours=time_zone)
        print '2    ', date_convert(res[1][3]) + datetime.timedelta(hours=time_zone)
        end = date_convert(res[1][4]) + datetime.timedelta(hours=time_zone)
        print 'Duration', date_convert(res[1][4]) - date_convert(res[1][1])
        print 'Duration', date_convert(res[1][3]) - date_convert(res[1][2])
        print 'Type:               ', res[0][0], bin(res[0][0])
        print 'Type: in Los Angeles', res_how[0][0], bin(res_how[0][0])
    soros_cycle = int(res[2][9])
    soros_number = int(res[2][10])
    max_covered = int(res[2][2] * 100)
    sun_alt = res[2][5]
    sun_azm = ((res[2][4] + 180) % 360)
    pos_p = swe.calc_ut(res[1][0], 0)
    signs = birthchart.natal_planet_signs(pos_p)
    sun_pos = pos_p[0]
    sun_zodiac = constants.SIGN_ZODIAC[signs[0]]
    pos_p = swe.calc_ut(res[1][0], 1)
    signs = birthchart.natal_planet_signs(pos_p)
    moon_pos = pos_p[0]
    moon_zodiac = constants.SIGN_ZODIAC[signs[0]]

    pos_p = swe.calc_ut(res[1][0], 0)
    #print 'Sun  position', pos_p[0]
    pos_p = swe.calc_ut(res[1][0], 1)
    #print 'Moon position', pos_p[0]
    
 
       
    solar_eclipse_bypos = {'ecl_central_or_not' : ecl_central_or_not, 'soros_cycle' : soros_cycle,
                            'soros_number' : soros_number, 'max_covered' : max_covered, 'sun_alt' : sun_alt, 'sun_azm' : sun_azm,
                            'sun_pos' : sun_pos, 'sun_zodiac' : sun_zodiac, 'moon_pos' : moon_pos, 'moon_zodiac' : moon_zodiac, 
                            'start' : start, 'max' : maxi, 'end' : end, 'Type' : Type}

    return solar_eclipse_bypos