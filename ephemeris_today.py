#!/usr/bin/env python
__author__ = 'naren'
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



def ephe_today(TimezoneID, start_time):
    birth_date = start_time
    time_birth_hour = start_time.hour  # 24 hour format
    time_birth_min = start_time.minute  # 24 hour format
    print TimezoneID
    is_birth_time = False
    x, y = np.array(birthchart.ephemeris_calc(float(TimezoneID),birth_date, time_birth_hour, time_birth_min))

    signs = birthchart.natal_planet_signs(x)
    #print signs
    rezult = []
    for i in range(len(x)):
        planet_deg = int(x[i])
        p_min = x[i] - planet_deg
        planet_min = int(p_min * 60)
        p_sec = p_min - (planet_min / 60.)
        planet_sec = int(p_sec * 3500)
        speed = ''
        if y[i] < 0:
            speed = 'R'
        rezult += constants.PLANET_CHARS[i], str(planet_deg) , str(planet_min) , str(planet_sec) , str(speed) , constants.SIGN_ZODIAC[signs[i]]

    return rezult


    xx = birthchart.natal_aspects(x, .1)
    aspect_natal_master = pd.read_csv('astro/data/natal_aspect_master/' + 'natal_aspects_master.csv', index_col=0,
                                      names=(['planet_a', 'aspect', 'planet_b']))
#Planetary hours

def plan_hours(time_zone, location_longitude, location_latitude):
    is_birth_time = True
    #lt_zone = -7
    date_start = datetime.datetime.today()  # today's date
    planetary_hour_sequence = ('saturn', 'jupiter', 'mars', 'sun', 'venus', 'mercury', 'moon')
    day_sequence = ('moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'sun')
    day_sequence_p = (6, 2, 5, 1, 4, 0, 3)
    #search this date's noon [12 PM]
    now_julian = swe.julday(date_start.year, date_start.month, date_start.day, 12)
    planet_rise_jul = swe.rise_trans(now_julian, 0, location_longitude, location_latitude, 0.0, 0.0, 0.0, 1)
    planet_set_jul = swe.rise_trans(now_julian, 0, location_longitude, location_latitude, 0.0, 0.0, 0.0, 2)
    sun_rise_tuple = swe.jdut1_to_utc(planet_rise_jul[1][0],1)
    sun_rise_list = list(sun_rise_tuple)
    sun_rise_list[5] = int(sun_rise_list[5])
    sun_rise = datetime.datetime(*sun_rise_list[0:6]) + datetime.timedelta(hours=time_zone)
    sun_rise_question = sun_rise
    sun_set_tuple = swe.jdut1_to_utc(planet_set_jul[1][0], 1)
    sun_set_list = list(sun_set_tuple)
    sun_set_list[5] = int(sun_set_list[5])
    sun_set = datetime.datetime(*sun_set_list[0:6]) + datetime.timedelta(hours=time_zone)
    sun_set_question = sun_set
    # next day sun rise
    now_julian = swe.julday(date_start.year, date_start.month, date_start.day + 1, 12)
    planet_rise_jul_next_day = swe.rise_trans(now_julian, 0, location_longitude, location_latitude, 0.0, 0.0, 0.0, 1)
    sun_rise_tuple_n = swe.jdut1_to_utc(planet_rise_jul_next_day[1][0], 1)
    sun_rise_list_n = list(sun_rise_tuple_n)
    sun_rise_list_n[5] = int(sun_rise_list_n[5])
    sun_rise_n = datetime.datetime(*sun_rise_list_n[0:6]) + datetime.timedelta(hours=time_zone)
    print 'sun rise:', sun_rise.strftime('%m-%d-%Y: %H:%M')
    print 'sun set:', sun_set.strftime('%m-%d-%Y: %H:%M')
    print 'sun rise next', sun_rise_n.strftime('%m-%d-%Y: %H:%M')
    day_diff = (sun_set - sun_rise)
    day_diff_skip = day_diff.total_seconds() / 12
    night_diff = (sun_rise_n - sun_set)
    night_diff_skip = night_diff.total_seconds() / 12
    #print day_diff_skip, night_diff_skip
    day_of_week = sun_rise.weekday()
    start_sequence = day_sequence[day_of_week]  #starting planet
    print 'Day:',start_sequence#, planetary_hour_sequence[day_sequence_p[day_of_week]]
    j = day_sequence_p[day_of_week]
    #print 'Sunrise: Planetary hours'
    rezultss = []
    for i in range(12):
        if j > 6:
            j = 0
        rezultss+= sun_rise.strftime('%m-%d-%Y: %H:%M'), (sun_rise + day_diff / 12).strftime('%m-%d-%Y: %H:%M'), planetary_hour_sequence[j]
        sun_rise += day_diff / 12
        j += 1
    #print 'Sunset : Planetary hours'
    rezults = []
    for i in range(12):
        if j > 6:
            j = 0
        rezults+= sun_set.strftime('%m-%d-%Y: %H:%M'), (sun_set + night_diff / 12).strftime('%m-%d-%Y: %H:%M'), planetary_hour_sequence[j]
        sun_set += night_diff / 12
        j += 1
    return rezults, rezultss