#!/usr/bin/env python
__author__ = 'naren'
import ephem
import swisseph as swe
import datetime
import pandas as pd
import time

def planet_rise():
	sitka = ephem.Observer()
	# sitka.date = '2015/6/18'
	sitka.lat = '22.5'
	sitka.long = '77.5'
	m = ephem.Sun()
	sitka.pressure = 0
	sitka.horizon = '-18'
	time_zone = 5.5
	planet = {}
	print 'Rise/ hign noon/set times for:', sitka.lat, sitka.long
	print 'Rise -Twilight ', ephem.date(sitka.next_rising(m) + time_zone * ephem.hour)
	sitka.horizon = '-12'
	print 'Rise - Nautical', ephem.date(sitka.next_rising(m) + time_zone * ephem.hour)
	sitka.horizon = '-6'
	print 'Rise - Civil   ', ephem.date(sitka.next_rising(m) + time_zone * ephem.hour)
	sitka.horizon = '-0:50'
	sun_rise = ephem.date(sitka.next_rising(m) + time_zone * ephem.hour)
	print 'Rise Regular   ', sun_rise
	sitka.date = ephem.date(sitka.next_rising(m))
	m = ephem.Sun(sitka)
	print 'azimuth        ', m.az
	noon = ephem.date(sitka.next_transit(m) + time_zone * ephem.hour)
	print 'Noon           ', noon
	sitka.date = ephem.date(sitka.next_transit(m))
	m = ephem.Sun(sitka)
	print 'azimuth        ', m.alt
	sun_set = ephem.date(sitka.next_setting(m) + time_zone * ephem.hour)
	print 'Set            ', sun_set
	sitka.date = ephem.date(sitka.next_setting(m))
	m = ephem.Sun(sitka)
	print 'azimuth        ', m.az
	print 'Day Length     ', (sun_set - sun_rise) * 24
	sitka.horizon = '-6'
	sun_set = ephem.date(sitka.next_setting(m) + time_zone * ephem.hour)
	print 'Sunset - Civil ', sun_set
	sitka.horizon = '-12'
	sun_set = ephem.date(sitka.next_setting(m) + time_zone * ephem.hour)
	print 'Sunset - Naut  ', sun_set
	sitka.horizon = '-18'
	sun_set = ephem.date(sitka.next_setting(m) + time_zone * ephem.hour)
	print 'Sunset - Astro ', sun_set
	print '--------------------------------'


	print 'Moon'
	print '--------------------------------'
	sitka = ephem.Observer()
	# sitka.date = '2015/6/22'
	sitka.lat = '34:1'
	sitka.long = '-118:15'
	m = ephem.Moon()
	print 'Rise/ hign noon/set times for:', sitka.lat, sitka.long
	print 'Rise   ', ephem.date(sitka.next_rising(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_rising(m))
	m = ephem.Moon(sitka)
	print 'azimuth', m.az

	print 'Noon   ', ephem.date(sitka.next_transit(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_transit(m))
	m = ephem.Moon(sitka)
	print 'azimuth', m.alt, m.phase, '% phase', m.earth_distance * ephem.meters_per_au / 1600

	print 'Set    ', ephem.date(sitka.next_setting(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_setting(m))
	m = ephem.Moon(sitka)
	print 'azimuth', m.az
	print '--------------------------------'
	print 'Moon - Now'
	sitka = ephem.Observer()
	# sitka.date = '2015/10/19 4:21:54'
	sitka.lat = '34:03'
	sitka.long = '-118:15'
	v = ephem.Moon(sitka)
	Altitude = v.alt
	Direction = v.az
	m = ephem.Moon()
	m.compute()
	Phase = m.phase
	Distance = (m.earth_distance * ephem.meters_per_au / 1600)
	planet['Moon'] = {'Phase':Phase, 'Distance':Distance, 'Altitude':Altitude, 'Direction':Direction}
	print '--------------------------------'
	print 'Mercury'
	print '--------------------------------'
	sitka = ephem.Observer()
	#sitka.date = '2015/10/12'
	sitka.lat = '34:03'
	sitka.long = '-118:15'
	m = ephem.Mercury()
	print 'Rise/ hign noon/set times for:', sitka.lat, sitka.long
	print 'Rise   ', ephem.date(sitka.next_rising(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_rising(m))
	m = ephem.Mercury(sitka)
	print 'azimuth', m.az

	print 'Noon   ', ephem.date(sitka.next_transit(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_transit(m))
	m = ephem.Mercury(sitka)
	print 'azimuth', m.alt, m.phase, '% phase'

	print 'Set    ', ephem.date(sitka.next_setting(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_setting(m))
	m = ephem.Mercury(sitka)
	print 'azimuth', m.az
	print '--------------------------------'
	print 'Mercury - Now'
	sitka = ephem.Observer()
	#sitka.date = '2015/10/19 4:21:54'
	sitka.lat = '34:03'
	sitka.long = '-118:15'
	v = ephem.Mercury(sitka)
	Altitude = v.alt
	Direction = v.az
	m = ephem.Mercury()
	m.compute()
	Phase = m.phase
	Distance = (m.earth_distance * ephem.meters_per_au / 1600)
	planet['Mercury'] = {'Phase':Phase, 'Distance':Distance, 'Altitude':Altitude, 'Direction':Direction}
	print '--------------------------------'
	print 'Venus'
	print '--------------------------------'
	sitka = ephem.Observer()
	# sitka.date = '2015/10/12'
	sitka.lat = '34:03'
	sitka.long = '-118:15'
	m = ephem.Venus()
	print 'Rise/ hign noon/set times for:', sitka.lat, sitka.long
	print 'Rise   ', ephem.date(sitka.next_rising(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_rising(m))
	m = ephem.Venus(sitka)
	print 'azimuth', m.az

	print 'Noon   ', ephem.date(sitka.next_transit(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_transit(m))
	m = ephem.Venus(sitka)
	print 'azimuth', m.alt, m.phase, '% phase'

	print 'Set    ', ephem.date(sitka.next_setting(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_setting(m))
	m = ephem.Venus(sitka)
	print 'azimuth', m.az
	print '--------------------------------'
	print 'Venus - Now'
	sitka = ephem.Observer()
	#sitka.date = '2015/10/19 4:21:54'
	sitka.lat = '34:03'
	sitka.long = '-118:15'
	v = ephem.Venus(sitka)
	Altitude = v.alt
	Direction = v.az
	m = ephem.Venus()
	m.compute()
	Phase = m.phase
	Distance = (m.earth_distance * ephem.meters_per_au / 1600)
	planet['Venus'] = {'Phase':Phase, 'Distance':Distance, 'Altitude':Altitude, 'Direction':Direction}
	print '--------------------------------'
	print 'Mars'
	print '--------------------------------'
	sitka = ephem.Observer()
	#sitka.date = '2015/10/12'
	sitka.lat = '34:03'
	sitka.long = '-118:15'
	m = ephem.Mars()
	print 'Rise/ hign noon/set times for:', sitka.lat, sitka.long
	print 'Rise   ', ephem.date(sitka.next_rising(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_rising(m))
	m = ephem.Mars(sitka)
	print 'azimuth', m.az

	print 'Noon   ', ephem.date(sitka.next_transit(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_transit(m))
	m = ephem.Mars(sitka)
	print 'azimuth', m.alt, m.phase, '% phase'

	print 'Set    ', ephem.date(sitka.next_setting(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_setting(m))
	m = ephem.Mars(sitka)
	print 'azimuth', m.az
	print '--------------------------------'
	print 'Mars - Now'
	sitka = ephem.Observer()
	#sitka.date = '2015/10/19 4:21:54'
	sitka.lat = '34:03'
	sitka.long = '-118:15'
	v = ephem.Mars(sitka)
	Altitude = v.alt
	Direction = v.az
	m = ephem.Mars()
	m.compute()
	Phase = m.phase
	Distance = (m.earth_distance * ephem.meters_per_au / 1600)
	planet['Mars'] = {'Phase':Phase, 'Distance':Distance, 'Altitude':Altitude, 'Direction':Direction}
	print '--------------------------------'
	print 'Jupiter'
	print '--------------------------------'
	sitka = ephem.Observer()
	#sitka.date = '2015/10/12'
	sitka.lat = '34:03'
	sitka.long = '-118:15'
	m = ephem.Jupiter()
	print 'Rise/ hign noon/set times for:', sitka.lat, sitka.long
	Rise = str(ephem.date(sitka.next_rising(m) + time_zone * ephem.hour))
	sitka.date = ephem.date(sitka.next_rising(m))
	m = ephem.Jupiter(sitka)
	print 'azimuth', m.az

	print 'Noon   ', ephem.date(sitka.next_transit(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_transit(m))
	m = ephem.Jupiter(sitka)
	print 'azimuth', m.alt, m.phase, '% phase'

	Set = str(ephem.date(sitka.next_setting(m) + time_zone * ephem.hour))
	sitka.date = ephem.date(sitka.next_setting(m))
	m = ephem.Jupiter(sitka)
	azimuth = m.az
	#print '--------------------------------'
	#print 'Jupiter - Now'
	sitka = ephem.Observer()
	#sitka.date = '2015/10/19 4:21:54'
	sitka.lat = '34:03'
	sitka.long = '-118:15'
	v = ephem.Jupiter(sitka)
	Altitude = str(v.alt)
	Direction = str(v.az)
	m = ephem.Jupiter()
	m.compute()
	Phase = str(m.phase)
	Distance = str(m.earth_distance * ephem.meters_per_au / 1600)
	planet['Jupiter'] = {'Azimuth' :azimuth, 'Rise' :Rise, 'Set' :Set, 'Phase':Phase, 'Distance':Distance, 'Altitude':Altitude, 'Direction':Direction}
	print '--------------------------------'
	print 'Saturn'
	print '--------------------------------'
	sitka = ephem.Observer()
	#sitka.date = '2015/10/12'
	sitka.lat = '34:03'
	sitka.long = '-118:15'
	m = ephem.Saturn()
	print 'Rise/ hign noon/set times for:', sitka.lat, sitka.long
	print 'Rise   ', ephem.date(sitka.next_rising(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_rising(m))
	m = ephem.Saturn(sitka)
	print 'azimuth', m.az

	print 'Noon   ', ephem.date(sitka.next_transit(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_transit(m))
	m = ephem.Saturn(sitka)
	print 'azimuth', m.alt, m.phase, '% phase'

	print 'Set    ', ephem.date(sitka.next_setting(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_setting(m))
	m = ephem.Saturn(sitka)
	print 'azimuth', m.az
	print '--------------------------------'
	print 'Saturn - Now'
	sitka = ephem.Observer()
	#sitka.date = '2015/10/19 4:21:54'
	sitka.lat = '34:03'
	sitka.long = '-118:15'
	v = ephem.Saturn(sitka)
	Altitude = v.alt
	Direction = v.az
	m = ephem.Saturn()
	m.compute()
	Phase = m.phase
	Distance = (m.earth_distance * ephem.meters_per_au / 1600)
	planet['Saturn'] = {'Phase':Phase, 'Distance':Distance, 'Altitude':Altitude, 'Direction':Direction}
	print '--------------------------------'
	print 'Uranus'
	print '--------------------------------'
	sitka = ephem.Observer()
	#sitka.date = '2015/10/12'
	sitka.lat = '34:03'
	sitka.long = '-118:15'
	m = ephem.Uranus()
	print 'Rise/ hign noon/set times for:', sitka.lat, sitka.long
	print 'Rise   ', ephem.date(sitka.next_rising(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_rising(m))
	m = ephem.Uranus(sitka)
	print 'azimuth', m.az

	print 'Noon   ', ephem.date(sitka.next_transit(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_transit(m))
	m = ephem.Uranus(sitka)
	print 'azimuth', m.alt, m.phase, '% phase'

	print 'Set    ', ephem.date(sitka.next_setting(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_setting(m))
	m = ephem.Uranus(sitka)
	print 'azimuth', m.az
	print '--------------------------------'
	print 'Uranus - Now'
	sitka = ephem.Observer()
	#sitka.date = '2015/10/19 4:21:54'
	sitka.lat = '34:03'
	sitka.long = '-118:15'
	v = ephem.Uranus(sitka)
	Altitude = v.alt
	Direction = v.az
	m = ephem.Uranus()
	m.compute()
	Phase = m.phase
	Distance = (m.earth_distance * ephem.meters_per_au / 1600)
	planet['Uranus'] = {'Phase':Phase, 'Distance':Distance, 'Altitude':Altitude, 'Direction':Direction}
	print '--------------------------------'
	print 'Neptune'
	print '--------------------------------'
	sitka = ephem.Observer()
	#sitka.date = '2015/10/12'
	sitka.lat = '34:03'
	sitka.long = '-118:15'
	m = ephem.Neptune()
	print 'Rise/ hign noon/set times for:', sitka.lat, sitka.long
	print 'Rise   ', ephem.date(sitka.next_rising(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_rising(m))
	m = ephem.Neptune(sitka)
	print 'azimuth', m.az

	print 'Noon   ', ephem.date(sitka.next_transit(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_transit(m))
	m = ephem.Neptune(sitka)
	print 'azimuth', m.alt, m.phase, '% phase'

	print 'Set    ', ephem.date(sitka.next_setting(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_setting(m))
	m = ephem.Neptune(sitka)
	print 'azimuth', m.az
	print '--------------------------------'
	print 'Neptune - Now'
	sitka = ephem.Observer()
	#sitka.date = '2015/10/19 4:21:54'
	sitka.lat = '34:03'
	sitka.long = '-118:15'
	v = ephem.Neptune(sitka)
	Altitude = v.alt
	Direction = v.az
	m = ephem.Neptune()
	m.compute()
	Phase = m.phase
	Distance = (m.earth_distance * ephem.meters_per_au / 1600)
	planet['Neptune'] = {'Phase':Phase, 'Distance':Distance, 'Altitude':Altitude, 'Direction':Direction}
	print '--------------------------------'
	print 'Pluto'
	print '--------------------------------'
	sitka = ephem.Observer()
	#sitka.date = '2015/10/12'
	sitka.lat = '34:03'
	sitka.long = '-118:15'
	m = ephem.Pluto()
	print 'Rise/ hign noon/set times for:', sitka.lat, sitka.long
	print 'Rise   ', ephem.date(sitka.next_rising(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_rising(m))
	m = ephem.Pluto(sitka)
	print 'azimuth', m.az

	print 'Noon   ', ephem.date(sitka.next_transit(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_transit(m))
	m = ephem.Pluto(sitka)
	print 'azimuth', m.alt, m.phase, '% phase'

	print 'Set    ', ephem.date(sitka.next_setting(m) + time_zone * ephem.hour)
	sitka.date = ephem.date(sitka.next_setting(m))
	m = ephem.Pluto(sitka)
	print 'azimuth', m.az
	print '--------------------------------'
	print 'Pluto - Now'
	sitka = ephem.Observer()
	#sitka.date = '2015/10/19 4:21:54'
	sitka.lat = '34:03'
	sitka.long = '-118:15'
	v = ephem.Pluto(sitka)
	Altitude = v.alt
	Direction = v.az
	m = ephem.Pluto()
	m.compute()
	Phase = m.phase
	Distance = (m.earth_distance * ephem.meters_per_au / 1600)
	planet['Pluto'] = {'Phase':Phase, 'Distance':Distance, 'Altitude':Altitude, 'Direction':Direction}
	return(planet)