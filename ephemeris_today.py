#!/usr/bin/env python
__author__ = 'naren'
###########################################################################################################################################################################################
################################################imports####################################################################################################################################
import numpy as np
import birthchart
import datetime
import pandas as pd
import swisseph as swe
from astro import constants
import time
from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine, MetaData
from sqlalchemy import *
from json import dumps
import urllib2, json
import sqlite3
from flask import g
import pytz, datetime

##############################################################################################################################################################################################
############################################### Default Inputs ###############################################################################################################################

city_latitude = float(34.05)  # Positive for north of Equator
city_longitude = float(-118.25)  # positive for East of Londo
date_passed = datetime.datetime(2016, 3, 28, 8, 53, 0)
time_zone = "Asia/Kolkata"

###############################################################################################################################################################################################
############################################## Today's Ephemeris Function #####################################################################################################################

def ephe_today(time_zone, date_passed):
    local_timezone = pytz.timezone(time_zone)
    local_date = local_timezone.localize(date_passed, is_dst=None)
    start_time = local_date.astimezone(pytz.utc)

    birth_date = start_time
    time_birth_hour = start_time.hour  # 24 hour format
    time_birth_min = start_time.minute  # 24 hour format
    #print TimezoneID
    is_birth_time = False
    x, y = np.array(birthchart.ephemeris_calc(0,birth_date, time_birth_hour, time_birth_min))

    signs = birthchart.natal_planet_signs(x)
    #print signs
    rezult = {}
    for i in range(len(x)):
        planet_deg = int(x[i])
        p_min = x[i] - planet_deg
        planet_min = int(p_min * 60)
        p_sec = p_min - (planet_min / 60.)
        planet_sec = int(p_sec * 3500)
        speed = ''
        planet = constants.PLANET_CHARS[i]
        if y[i] < 0:
            speed = 'R'
        rezult[planet] = {'planet' : planet, 'planet_deg' : str(planet_deg) +' '+ str(planet_min) +' '+ str(planet_sec) +' '+ str(speed) , 'sign' : constants.SIGN_ZODIAC[signs[i]]}
    return (rezult)

##############################################################################################################################################################################################
################################################ Transit Function ############################################################################################################################

def ephe_trans(time_zone, date_passed):
    local_timezone = pytz.timezone(time_zone)
    local_date = local_timezone.localize(date_passed, is_dst=None)
    start_date = local_date.astimezone(pytz.utc)
    print 'Local date is: ', local_date
    x, y = np.array(birthchart.ephemeris_calc(0., start_date, start_date.hour, start_date.minute))
    xx = birthchart.natal_aspects(x, 1)
    aspect_natal_master = pd.read_csv('astro/data/natal_aspect_master/' + 'natal_aspects_master.csv', index_col=0,
                                      names=(['planet_a', 'aspect', 'planet_b']))
    trans_result = {}
    i = 0
    for n in xx[0]:
        trans_result[i] = {'planet_a' : constants.PLANET_CHARS[aspect_natal_master.loc[n]['planet_a']], 'planet_aspects' : constants.ASPECTS[aspect_natal_master.loc[n]['aspect']], 
        'plant_b' : constants.PLANET_CHARS[aspect_natal_master.loc[n]['planet_b']]}
        i += 1
    return( trans_result)

##################################################################################################################################################################################################
################################################ Planetary hours Function ########################################################################################################################

def plan_hours(time_zone, city_longitude, city_latitude):
    local_timezone = pytz.timezone(time_zone)
    local_date = local_timezone.localize(date_passed, is_dst=None)
    
    date_start = datetime.datetime.today()  # today's date

    planetary_hour_sequence = ('Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon')
    day_sequence = ('Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Sun')
    day_sequence_p = (6, 2, 5, 1, 4, 0, 3)
    # search this date's noon [12 PM]
    now_julian = swe.julday(date_start.year, date_start.month, date_start.day, 12)
    planet_rise_jul = swe.rise_trans(now_julian, 0, city_longitude, city_latitude, 0.0, 0.0, 0.0, 1)
    planet_set_jul = swe.rise_trans(now_julian, 0, city_longitude, city_latitude, 0.0, 0.0, 0.0, 2)
    sun_rise_tuple = swe.jdut1_to_utc(planet_rise_jul[1][0], 1)
    sun_rise_list = list(sun_rise_tuple)
    sun_rise1 = datetime.datetime(*sun_rise_list[0:5], tzinfo=pytz.utc)
    sun_rise = sun_rise1.astimezone(local_timezone)
    # sunset
    sun_set_tuple = swe.jdut1_to_utc(planet_set_jul[1][0], 1)
    sun_set_list = list(sun_set_tuple)
    sun_set1 = datetime.datetime(*sun_set_list[0:5], tzinfo=pytz.utc)
    sun_set = sun_set1.astimezone(local_timezone)
    # next day sun rise
    now_julian = swe.julday(date_start.year, date_start.month, date_start.day + 1, 12)
    planet_rise_jul_next_day = swe.rise_trans(now_julian, 0, city_longitude, city_latitude, 0.0, 0.0, 0.0, 1)
    sun_rise_tuple_n = swe.jdut1_to_utc(planet_rise_jul_next_day[1][0], 1)
    sun_rise_list_n = list(sun_rise_tuple_n)
    sun_rise_n1 = datetime.datetime(*sun_rise_list_n[0:5], tzinfo=pytz.utc)
    sun_rise_n = sun_rise_n1.astimezone(local_timezone)
    print 'sun rise:', sun_rise.strftime('%m-%d-%Y: %H:%M')
    print 'sun set:', sun_set.strftime('%m-%d-%Y: %H:%M')
    print 'sun rise next', sun_rise_n.strftime('%m-%d-%Y: %H:%M')
    day_diff = (sun_set - sun_rise)
    day_diff_skip = day_diff.total_seconds() / 12
    night_diff = (sun_rise_n - sun_set)
    night_diff_skip = night_diff.total_seconds() / 12
    # print day_diff_skip, night_diff_skip
    day_of_week = sun_rise.weekday()
    start_sequence = day_sequence[day_of_week]  # starting planet
    print 'Day:', start_sequence  # , planetary_hour_sequence[day_sequence_p[day_of_week]]
    j = day_sequence_p[day_of_week]
    print 'Sunrise: Planetary hours'
    rezultss = {}
    for i in range(12):
        if j > 6:
            j = 0
        rezultss[i] = {'time' : str(sun_rise.strftime('%m-%d-%Y: %H:%M')), 'time2' : str((sun_rise + day_diff / 12).strftime('%m-%d-%Y: %H:%M')), 'planet' : str(planetary_hour_sequence[j])}
        sun_rise += day_diff / 12
        j += 1
    print 'Sunset : Planetary hours'
    rezults = {}
    for i in range(12):
        if j > 6:
            j = 0
        rezults[i]= {'time' : str(sun_set.strftime('%m-%d-%Y: %H:%M')), 'time2' : str((sun_set + night_diff / 12).strftime('%m-%d-%Y: %H:%M')), 'planet' : str(planetary_hour_sequence[j])}
        sun_set += night_diff / 12
        j += 1
    return rezults, rezultss
    
###########################################################################################################################################################################################################