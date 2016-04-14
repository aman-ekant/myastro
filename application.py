#!/usr/bin/env python
__author__ = 'naren'
########################################################################################################################
################################################imports#################################################################
import numpy as np
import birthchart
import datetime
import math
import pandas as pd
import swisseph as swe
from astro import constants
import time
import re
from flask import Flask, render_template, request, jsonify, url_for
from flask_restful import Resource, Api
from sqlalchemy import create_engine, MetaData
from sqlalchemy import *
from json import dumps
import urllib2, json
import sqlite3
from flask import g
import planet_rise_times
import ip2location_lookup
import ephemeris_today
import moon_phases
import eclipse_solar
import eclipses_lunar

#########################################################################################################################
################################################Common###################################################################

con = sqlite3.connect('city', check_same_thread=False)
curr = con.cursor()
application = Flask(__name__, static_url_path='/astro/static')
api = Api(application)

swe.set_ephe_path('astro/data/ephemeris/')  # path to ephemeris files
f = urllib2.urlopen('http://jsonip.com/')
json_string = f.read()
f.close()
ip_add = json.loads(json_string)
ip_addrs = ip_add['ip']#'2607:f1c0:83c:7000:0:0:43:963d'
tt = ''
if (re.match('^[0-9]{0,3}.[0-9]{0,3}.[0-9]{0,3}.[0-9]{0,3}$', ip_addrs)):
    tt = 1
    location_latitude, location_longitude, TimezoneID, region  = ip2location_lookup.ipv42loc(ip_addrs)
    
else:
    tt = 0
    location_latitude, location_longitude, TimezoneID, region  = ip2location_lookup.ipv62loc(ip_addrs)
#print 'latitude is', location_latitude
#print 'Longitude is', location_longitude
#print 'region is', region
#location_longitude = 77.2167
#location_latitude = 28.6667
nows = datetime.datetime.now()
year = nows.year
month = nows.month
day = nows.day
start_time = datetime.datetime.utcnow()
time_zone = TimezoneID
#print nows

##########################################################################################################################
###############################################moon phases API############################################################
rezultsz = moon_phases.phases(year)
@application.route('/moonphases_api/', methods=['GET'])
def get_moonphasesx():
    #return jsonify({'moonphases': rezultsz})
    return jsonify({'moonphases': 'No Data Found',
                    'error': 'missing parameter'})




@application.route('/moonphases_api/<int:year>', methods=['GET'])
def moonphasessx(year):
    rezultszz = moon_phases.phases(year)
    return jsonify({'moonphases': rezultszz})


##########################################################################################################################
#################################################planet hours API#########################################################
rezults, rezultss = ephemeris_today.plan_hours(TimezoneID, location_longitude, location_latitude)
@application.route('/hours_api/')
def hoursx():
    #return jsonify({'Sunset Planetary Hours' : rezults,'Sunrise Planetary Hours' : rezultss})
    return jsonify({'Planetary Hours': 'No Data Found',
                    'error': 'missing parameters'})

@application.route('/hours_api/<Timezonez>/<lon>/<lat>', methods=['GET'])
def hoursz(Timezonez, lon, lat):
    rezults, rezultss = ephemeris_today.plan_hours(float(Timezonez), float(lon), float(lat)) 
    return jsonify({'Sunset Planetary Hours' : rezults,'Sunrise Planetary Hours' : rezultss})
    
        

@application.route('/hours_api/<Timezonez>/<lon>/')
def hourrs(Timezonez, lon):
    return jsonify({'Planetary Hours': 'No Data Found',
                'error': '1 missing parameter'})


@application.route('/hours_api/<Timezonez>/')
def housrs(Timezonez):
    return jsonify({'Planetary Hours': 'No Data Found',
                'error': '2 missing parameters'})



##########################################################################################################################
#################################################ephemeris_today API######################################################

@application.route('/home_api/')
def get_homez():
    #return jsonify({'ephemeris': rezult})
    return jsonify({'Ephemeris Today': 'No Data Found',
                    'error': 'missing parameters'})

@application.route('/home_api/<Timezonezs>/')
def get_homex(Timezonezs):
    rezult  = ephemeris_today.ephe_today(float(Timezonezs), start_time)
    return jsonify({'ephemeris': rezult})
throwaway = datetime.datetime.strptime('20110101','%Y%m%d')
@application.route('/home_api/<Timezonezs>/<time>/')
def get_homec(Timezonezs, time):
    
    try:
        datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        rezult  = ephemeris_today.ephe_today(float(Timezonezs), datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f"))
        return jsonify({'ephemeris': rezult})
    
    except ValueError:
        return jsonify({'Ephemeris Today': 'No Data Found',
                    'error': 'Parameter value doesn\'t match the prescribed format'})


##########################################################################################################################
###################################################Today's Ephemeris######################################################

@application.route('/')
def home():
    rezult  = ephemeris_today.ephe_today(TimezoneID, start_time)
#ephemeris_today
    return render_template('home.html', rez=rezult)

##########################################################################################################################
###################################################Planet Risetimes#######################################################

@application.route('/risetimes/')
def risetimes():
    x = planet_rise_times.planet_rise()
    return render_template('planet_rise_times.html', x=x)

###########################################################################################################################
###################################################Planetary Hours#########################################################

@application.route('/hours/')
def hours():
    rezults, rezultss = ephemeris_today.plan_hours(TimezoneID, location_longitude, location_latitude)
    return render_template('planetary_hours.html', res=rezults, ress=rezultss)


############################################################################################################################
###################################################Moon Phases##############################################################

@application.route('/moonphases/<int:year>')
def moonphasess(year):
    rezults = moon_phases.phases(year)
    return render_template('moon_phases.html', rez=rezults)

@application.route('/moonphases/')
def moonphases():
    rezults = moon_phases.phases(year)
    return render_template('moon_phases.html', rez=rezults)

##############################################################################################################################
####################################################Solar Eclipse##############################################################

@application.route('/eclipse/')
def eclipse():
    result = eclipse_solar.solar(year, month, day, time_zone, location_latitude, location_longitude)
    return render_template('solareclipse.html', rez=result) 
       
    

@application.route('/eclipses/')
def eclipses():
    result = eclipse_solar.solarbypos(year, month, day, time_zone, location_latitude, location_longitude)
    return render_template('solareclipsebyposition.html', rez=result) 

##############################################################################################################################
#######################################################Lunar Eclipse##############################################################

@application.route('/leclipse/')
def leclipse():
    result = eclipses_lunar.lunar(year, month, day, time_zone, location_latitude, location_longitude)
    return render_template('lunareclipse.html', rez=result) 
    
    

@application.route('/leclipses/')
def leclipses():
    result = eclipses_lunar.lunarbypos(year, month, day, time_zone, location_latitude, location_longitude)
    return render_template('lunareclipsebyposition.html', rez=result) 

##############################################################################################################################

@application.route('/content/')
def content():
    return render_template('content.html')

if __name__ == '__main__':
     application.run(debug=True)

