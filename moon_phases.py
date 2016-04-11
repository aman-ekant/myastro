#!/usr/bin/env python
__author__ = 'naren'
import ephem
import swisseph as swe
import datetime
import pandas as pd
import time
from flask import Flask, render_template, request, jsonify, url_for

time_zone = 5.5
def phases(start):
    j = ephem.Moon()
    #start = '2015-10-1'
    moon_phases = {}
    for x in range(20):
        if x > 0:
            new_moon = ephem.next_new_moon(third_quarter)
            j.compute(new_moon)
            print j.earth_distance * ephem.meters_per_au / 1000, j.phase
        else:
            year_c = str(start)
            new_moon = ephem.next_new_moon(year_c)
        first_quarter = ephem.next_first_quarter_moon(new_moon)
        full_moon = ephem.next_full_moon(first_quarter)
        # j = ephem.Moon()
        j.compute(full_moon)
        print j.earth_distance * ephem.meters_per_au / 1000, j.phase
        third_quarter = ephem.next_last_quarter_moon(full_moon)
        moon_phases[x] = new_moon, first_quarter, full_moon, third_quarter
        print 'New Moon     :', new_moon
        # print 'First Quarter:', first_quarter
        print 'Full Moon    :', full_moon
        # print 'Third Quarter:', third_quarter
        #print '------------------------'
    #print moon_phases
    moon_phase_pd = pd.DataFrame(moon_phases)#, index=['new_moon', 'first_quarter', 'full_moon', 'third_quarter'])
    moon_phase_pd = moon_phase_pd.T
    print moon_phase_pd
    
    moon_phase_pd.to_csv('astro/data/planet_stations/moon_phases.csv')

    return (moon_phases)