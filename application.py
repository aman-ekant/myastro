#!/usr/bin/env python
__author__ = 'naren'
########################################################################################################################
################################################ imports ###############################################################
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

#############################################################################################################################
############################################### Common ######################################################################

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
    location_latitude, location_longitude, TimezoneID, region, city, country, timezone  = ip2location_lookup.ipv42loc(ip_addrs)
    
else:
    tt = 0
    location_latitude, location_longitude, TimezoneID, region, city, country, timezone  = ip2location_lookup.ipv62loc(ip_addrs)
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
#print TimezoneID
#print timezone

##########################################################################################################################
############################################## moon phases API ###########################################################
rezultsz = moon_phases.phases(year)
@application.route('/moonphases_api/', methods=['GET'])
def get_moonphasesx():
    return jsonify({'moonphases': 'No Data Found',
                    'error': 'missing parameter'})




@application.route('/moonphases_api/<int:year>', methods=['GET'])
def moonphasessx(year):
    rezultszz = moon_phases.phases(year)
    return jsonify({'moonphases': rezultszz})


##########################################################################################################################
################################################ planet hours API ########################################################

@application.route('/hours_api/')
def hoursx():
    return jsonify({'Planetary Hours': 'No Data Found',
                    'error': 'missing parameters'})

@application.route('/hours_api/<Timezonez1>/<Timezonez2>/<lon>/<lat>', methods=['GET'])
def hoursz(Timezonez1, Timezonez2, lon, lat):
    Timezonez = Timezonez1+'/'+Timezonez2
    rezults, rezultss = ephemeris_today.plan_hours(Timezonez, float(lon), float(lat)) 
    return jsonify({'Sunset Planetary Hours' : rezults,'Sunrise Planetary Hours' : rezultss})
    

@application.route('/hours_api/<Timezonez1>/<lon>/')
def hourra(Timezonez1, lon):
    return jsonify({'Planetary Hours': 'No Data Found',
                'error': '2 missing parameter'})       

@application.route('/hours_api/<Timezonez1>/<Timezonez2><lon>/')
def hourrs(Timezonez1, Timezonez2, lon):
    return jsonify({'Planetary Hours': 'No Data Found',
                'error': '1 missing parameter'})


@application.route('/hours_api/<Timezonez1>/')
def housrs(Timezonez1):
    return jsonify({'Planetary Hours': 'No Data Found',
                'error': '3 missing parameters'})



##########################################################################################################################
################################################ ephemeris_today API #####################################################

@application.route('/home_api/')
def get_homez():
    return jsonify({'Ephemeris Today': 'No Data Found',
                    'error': 'missing parameters'})
@application.route('/home_api/<Timezonez1>/')
def get_homeqq(Timezonez1):
    return jsonify({'Ephemeris Today': 'No Data Found',
                    'error': 'missing parameters'})

@application.route('/home_api/<Timezonez1>/<Timezonez2>/')
def get_homex(Timezonez1, Timezonez2):
    Timezonezs = Timezonez1+'/'+Timezonez2
    rezult  = ephemeris_today.ephe_today(Timezonezs, start_time)
    return jsonify({'ephemeris': rezult})
throwaway = datetime.datetime.strptime('20110101','%Y%m%d')
@application.route('/home_api/<Timezonez1>/<Timezonez2>/<time>/')
def get_homec(Timezonezs, time):
    
    try:
        Timezonezs = Timezonez1+'/'+Timezonez2
        datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        rezult  = ephemeris_today.ephe_today(Timezonezs, datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f"))
        return jsonify({'ephemeris': rezult})
    
    except ValueError:
        return jsonify({'Ephemeris Today': 'No Data Found',
                    'error': 'Parameter value doesn\'t match the prescribed format'})


##########################################################################################################################
################################################ solar_eclipse API #######################################################

@application.route('/solareclipse_api/')
def get_solarz():
    return jsonify({'Solar Eclipse': 'No Data Found',
                    'error': 'missing parameters'})

@application.route('/solareclipse_api/<Timezonezs>/')
def get_solarx(Timezonezs):
    result = eclipse_solar.solar(float(Timezonezs), year, month, day, location_latitude, location_longitude)
    return jsonify({'Solar Eclipse': result})

@application.route('/solareclipse_api/<Timezonezs>/<years>/')
def get_solarc(Timezonezs, years):
    result = eclipse_solar.solar(float(Timezonezs), int(years), month, day, location_latitude, location_longitude)
    return jsonify({'Solar Eclipse': result})
    
@application.route('/solareclipse_api/<Timezonezs>/<years>/<months>/')
def get_solarv(Timezonezs, years, months):
    result = eclipse_solar.solar(float(Timezonezs), int(years), int(months), day, location_latitude, location_longitude)
    return jsonify({'Solar Eclipse': result})

@application.route('/solareclipse_api/<Timezonezs>/<years>/<months>/<days>/')
def get_solarb(Timezonezs, years, months, days):
    result = eclipse_solar.solar(float(Timezonezs), int(years), int(months), int(days), location_latitude, location_longitude)
    return jsonify({'Solar Eclipse': result})

@application.route('/solareclipse_api/<Timezonezs>/<years>/<months>/<days>/<latt>/')
def get_solarn(Timezonezs, years, months, days, latt):
    return jsonify({'Solar Eclipse': 'No Data Found',
                    'error': '1 missing parameter'})

@application.route('/solareclipse_api/<Timezonezs>/<years>/<months>/<days>/<latt>/<longg>/')
def get_solarm(Timezonezs, years, months, days, latt, longg):
    result = eclipse_solar.solarbypos(float(Timezonezs), int(years), int(months), int(days), float(latt), float(longg))
    return jsonify({'Solar Eclipse': result})

##########################################################################################################################
################################################ lunar_eclipse API #######################################################

@application.route('/lunareclipse_api/')
def get_lunarz():

    return jsonify({'Lunar Eclipse': 'No Data Found',
                    'error': 'missing parameters'})

@application.route('/lunareclipse_api/<Timezonezs>/')
def get_lunarx(Timezonezs):
    result = eclipses_lunar.lunar(float(Timezonezs), year, month, day, location_latitude, location_longitude)
    return jsonify({'Lunar Eclipse': result})

@application.route('/lunareclipse_api/<Timezonezs>/<years>/')
def get_lunarc(Timezonezs, years):
    result = eclipses_lunar.lunar(float(Timezonezs), int(years), month, day, location_latitude, location_longitude)
    return jsonify({'Lunar Eclipse': result})
    
@application.route('/lunareclipse_api/<Timezonezs>/<years>/<months>/')
def get_lunarv(Timezonezs, years, months):
    result = eclipses_lunar.lunar(float(Timezonezs), int(years), int(months), day, location_latitude, location_longitude)
    return jsonify({'Lunar Eclipse': result})

@application.route('/lunareclipse_api/<Timezonezs>/<years>/<months>/<days>/')
def get_lunarb(Timezonezs, years, months, days):
    result = eclipses_lunar.lunar(float(Timezonezs), int(years), int(months), int(days), location_latitude, location_longitude)
    return jsonify({'Lunar Eclipse': result})

@application.route('/lunareclipse_api/<Timezonezs>/<years>/<months>/<days>/<latt>/')
def get_lunarn(Timezonezs, years, months, days, latt):
    return jsonify({'Lunar Eclipse': 'No Data Found',
                    'error': '1 missing parameter'})

@application.route('/lunareclipse_api/<Timezonezs>/<years>/<months>/<days>/<latt>/<longg>/')
def get_lunarm(Timezonezs, years, months, days, latt, longg):
    result = eclipses_lunar.lunarbypos(float(Timezonezs), int(years), int(months), int(days), float(latt), float(longg))
    return jsonify({'Lunar Eclipse': result})



##########################################################################################################################
################################################## Today's Ephemeris #####################################################

@application.route('/home/')
def home():
    rezult  = ephemeris_today.ephe_today(timezone, start_time)
    return render_template('home.html', rez=rezult, region=region, city=city, country=country)

##########################################################################################################################
################################################## Transits #####################################################

@application.route('/transit/')
def transit():
    rezult  = ephemeris_today.ephe_trans(timezone, start_time)
    return render_template('transits.html', rez=rezult)

##########################################################################################################################
################################################## Planet Risetimes ######################################################

@application.route('/risetimes/')
def risetimes():
    x = planet_rise_times.planet_rise()
    return render_template('planet_rise_times.html', x=x)

###########################################################################################################################
################################################## Planetary Hours ########################################################

@application.route('/hours/')
def hours():
    rezults, rezultss = ephemeris_today.plan_hours(timezone, location_longitude, location_latitude)
    return render_template('planetary_hours.html', res=rezults, ress=rezultss)


############################################################################################################################
################################################## Moon Phases #############################################################

@application.route('/moonphases/<int:year>')
def moonphasess(year):
    rezults = moon_phases.phases(year)
    return render_template('moon_phases.html', rez=rezults)

@application.route('/moonphases/')
def moonphases():
    rezults = moon_phases.phases(year)
    return render_template('moon_phases.html', rez=rezults)

##############################################################################################################################
################################################### Solar Eclipse ############################################################

@application.route('/eclipse/')
def eclipse():
    result = eclipse_solar.solar(time_zone, year, month, day, location_latitude, location_longitude)
    return render_template('solareclipse.html', rez=result) 
       
    

@application.route('/eclipses/')
def eclipses():
    result = eclipse_solar.solarbypos(time_zone, year, month, day, location_latitude, location_longitude)
    return render_template('solareclipsebyposition.html', rez=result) 

###############################################################################################################################
###################################################### Lunar Eclipse ##########################################################

@application.route('/leclipse/')
def leclipse():
    result = eclipses_lunar.lunar(time_zone, year, month, day, location_latitude, location_longitude)
    return render_template('lunareclipse.html', rez=result) 
    
    

@application.route('/leclipses/')
def leclipses():
    result = eclipses_lunar.lunarbypos(time_zone, year, month, day, location_latitude, location_longitude)
    return render_template('lunareclipsebyposition.html', rez=result) 

##############################################################################################################################
###################################################### Index Page ############################################################

@application.route('/')
def content():
    return render_template('content.html')

##############################################################################################################################
########################################################## Mains #############################################################

if __name__ == '__main__':
     application.run(debug=True)

###############################################################################################################################