__author__ = 'naren'
import swisseph as swe
from astro import constants
import numpy as np
import time

swe.set_ephe_path('astro/data/ephemeris/')  # path to ephemeris files
# eph_array = np.load('../data/ephemeris/eph-ns.npy')

# calculates birth chart planet positions including asc and mc if time of birth is known
def natal_chart_calc(t_zone, b_offset, b_date, t_birth_hour, t_birth_min, b_latitude, b_longitude, is_time, h_type):
    date_year_birth = int(b_date.strftime("%Y"))
    date_month_birth = int(b_date.strftime("%m"))
    date_day_birth = int(b_date.strftime("%d"))
    # print 'naren', date_year_birth, date_month_birth, date_day_birth, t_birth_hour, t_birth_min, t_zone, b_offset,\
    # (t_birth_hour + (t_birth_min / 60.)) - (t_zone + b_offset)
    now_julian = swe.julday(date_year_birth, date_month_birth, date_day_birth,
                            (t_birth_hour + (t_birth_min / 60.)) - (t_zone + b_offset))
    # print now_julian
    l_birthchart = len(constants.BIRTH_PLANETS)
    bchart_pos = np.zeros(l_birthchart + 2)
    bchart_speed = np.zeros(l_birthchart)
    for i in range(l_birthchart):
        pos_p = swe.calc_ut(now_julian, constants.BIRTH_PLANETS[i])
        bchart_pos[i] = pos_p[0]
        bchart_speed[i] = pos_p[3]

    if is_time:
        house_array = (swe.houses(now_julian, b_latitude, b_longitude, h_type))
        bchart_pos[i + 1] = house_array[1][0]
        bchart_pos[i + 2] = house_array[1][1]
    else:
        bchart_pos[i + 1] = 0
        bchart_pos[i + 2] = 0
    return bchart_pos, bchart_speed

def ephemeris_calc(t_zone, b_date, t_birth_hour, t_birth_min):
    date_year_birth = int(b_date.strftime("%Y"))
    date_month_birth = int(b_date.strftime("%m"))
    date_day_birth = int(b_date.strftime("%d"))
    now_julian = swe.julday(date_year_birth, date_month_birth, date_day_birth,
                            (t_birth_hour + (t_birth_min / 60.)) - t_zone)
    len_ephemeris = len(constants.EPHEMERIS_PLANETS)
    ephemeris_pos = np.zeros(len_ephemeris)
    ephemeris_speed = np.zeros(len_ephemeris)
    for i in range(len_ephemeris):
        pos_p = swe.calc_ut(now_julian, constants.EPHEMERIS_PLANETS[i])
        ephemeris_pos[i] = pos_p[0]
        ephemeris_speed[i] = pos_p[3]

    return ephemeris_pos, ephemeris_speed

# planet in houses
def natal_planets_house(birth_chart):
    house_natal = np.empty(12, dtype=np.int8)
    house_start = birth_chart[10:11]
    house_next = (house_start + 30) % 360
    for i in range(12):
        for p in range(len(birth_chart)):
            if house_start - house_next > 40:  # house is crossing 360 to 0
                if house_start <= birth_chart[p] < 360:
                    house_natal[p] = i + 1
                elif 0 <= birth_chart[p] < house_next:
                    house_natal[p] = i + 1
            elif house_start <= birth_chart[p] < house_next:
                house_natal[p] = i + 1
        house_start = house_next
        house_next = (house_start + 30) % 360
    # print 'Houses-Planets', house_natal
    return house_natal


# planet in signs
def natal_planet_signs(birth_chart):
    len_chart = len(birth_chart)
    sign_natal_planets = np.empty(len_chart, dtype=np.int8)
    for start in range(0, 360, 30):
        for p in range(len(birth_chart)):
            if (start + 30) > birth_chart[p] >= start:
                sign_natal_planets[p] = start / 30
    # print ' Signs-Planets', sign_natal_planets
    return sign_natal_planets


def natal_planets_house_compare(birth_chart, asc):
    house_natal = np.empty(12, dtype=np.int8)
    house_start = asc
    house_next = (house_start + 30) % 360
    for i in range(12):
        for p in range(len(birth_chart)):
            if house_start - house_next > 40:  # house is crossing 360 to 0
                if house_start <= birth_chart[p] < 360:
                    house_natal[p] = i + 1
                elif 0 <= birth_chart[p] < house_next:
                    house_natal[p] = i + 1
            elif house_start <= birth_chart[p] < house_next:
                house_natal[p] = i + 1
        house_start = house_next
        house_next = (house_start + 30) % 360
    # print 'Houses-Planets', house_natal
    return house_natal


# calculate birth natal aspects
def natal_aspects(birth_chart, orb, is_birthtime=True):
    # planet_natal_char = (
    # 'sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto', 'asc', 'mc')
    # aspects_ext = np.array([0, 30, 30, 45, 45, 60, 60, 90, 90, 120, 120, 135, 135, 150, 150, 180])
    is_birthtime = is_birthtime
    if is_birthtime:
        birthchart_n = birth_chart
    else:
        birthchart_n = birth_chart[0:10]
    aspect_len = constants.LEN_NATAL_ASPECTS  # len(aspects)  #number of aspects
    aspect_len_ext = constants.LEN_NATAL_ASPECTS_EXT  # len(aspects_ext)  #number of aspects
    l_natal_planets = constants.LEN_NATAL_PLANETS  # len(birthchart_n)

    len_birth_chart = (l_natal_planets - 1) * aspect_len_ext  # comparing sun to other 11 planets
    bt_array = np.empty(len_birth_chart, dtype=np.float)  # initialize array birth time user
    aspect_degree = np.empty(150, dtype=np.float)
    aspect_number_natal = np.zeros(150, dtype=np.int)
    aspect_number = 0
    asp = 0
    orb = orb
    # Make th master array of birth planet degrees for comparing
    l = 0
    for i in range(1, l_natal_planets):
        for k in range(aspect_len):
            if constants.NATAL_ASPECTS[k] == 0 or constants.NATAL_ASPECTS[k] == 180:
                temp_pos1 = (birthchart_n[i] + constants.NATAL_ASPECTS[k]) % 360
                bt_array[l] = temp_pos1
            else:
                temp_pos1 = (birthchart_n[i] + constants.NATAL_ASPECTS[k]) % 360
                temp_pos2 = (birthchart_n[i] - constants.NATAL_ASPECTS[k]) % 360
                bt_array[l] = temp_pos1
                l += 1
                bt_array[l] = temp_pos2
            l += 1
    # print 'naren', len(bt_array)#, bt_array

    # Compare against planets

    for k in range(l_natal_planets - 1):
        natal_array_h = (birthchart_n[k] + orb) % 360
        natal_array_l = (birthchart_n[k] - orb) % 360
        if k > 0:
            bt_array = bt_array[aspect_len_ext:]
        if abs(natal_array_h - natal_array_l) < 40:
            ee = np.logical_and(natal_array_h >= bt_array, bt_array >= natal_array_l)
            aa = np.where(ee)
            aaa = np.ravel(aa)  # have all planets in aspect
            for itt in aaa:
                diff = (bt_array[itt] - birthchart_n[k])
                g = itt // aspect_len_ext
                gg = itt % aspect_len_ext
                aspect_number_natal[asp] = aspect_number + g * aspect_len + ((gg + 1) / 2)
                aspect_degree[asp] = diff
                # print 'aspect', planet_natal_char[k], ' ', aspects_ext[gg], ' ', planet_natal_char[
                # g + 1 + k], diff, k, g, gg, int((gg + 1) / 2), aspect_number_natal[asp]
                # print 'direct',asp,aspect_number
                asp += 1
        else:
            # less than 360 but greater than planet+orb
            ee1 = np.logical_and(natal_array_l <= bt_array, bt_array < 360.)
            aa1 = np.where(ee1)
            aaa = np.ravel(aa1)  # have all planets in aspect
            # print "i am here",aaa
            for ds in aaa:
                if birthchart_n[k] >= natal_array_l:
                    diff = bt_array[ds] - birthchart_n[k]
                    # print 'A1', natal_array_h, bt_array[ds], natal_array_l, birthchart_n[k]
                else:
                    diff = 360 - bt_array[ds] + birthchart_n[k]
                    # print 'A2', natal_array_h, bt_array[ds], natal_array_l, birthchart_n[k]
                g = ds // aspect_len_ext
                gg = ds % aspect_len_ext
                aspect_number_natal[asp] = aspect_number + g * aspect_len + ((gg + 1) / 2)
                aspect_degree[asp] = diff
                # print 'aspectA', planet_natal_char[k], aspects_ext[gg], ' ', planet_natal_char[
                #    g + 1 + k], diff, k, ds, gg, int((gg + 1) / 2), aspect_number_natal[asp]
                asp += 1

            # > 0 but less than planet+orb
            ee = np.logical_and(natal_array_h >= bt_array, bt_array >= 0.)
            aa = np.where(ee)
            aaa = np.ravel(aa)  # have all planets in aspect
            # print 'birthchart',aaa
            for ds in aaa:
                if birthchart_n[k] >= natal_array_l:
                    diff = 360 - birthchart_n[k] + bt_array[ds]
                    #print 'B1', natal_array_h, bt_array[ds], natal_array_l, birthchart_n[k]
                else:
                    diff = bt_array[ds] - birthchart_n[k]
                    #print 'B2', natal_array_h, bt_array[ds], natal_array_l, birthchart_n[k]
                #print natal_array_h[i],bt_array[i],natal_array_l[i]
                g = ds // aspect_len_ext
                gg = ds % aspect_len_ext
                aspect_number_natal[asp] = aspect_number + g * aspect_len + ((gg + 1) / 2)
                aspect_degree[asp] = diff
                #print 'aspectB', planet_natal_char[k], aspects_ext[gg], ' ', planet_natal_char[
                #    g + 1 + k], diff, k, ds, int((gg + 1) / 2),aspect_number, aspect_number_natal[asp]
                asp += 1
        aspect_number += (l_natal_planets - 1 - k) * aspect_len

    aspect_number_natal = aspect_number_natal[:asp]
    aspect_degree = aspect_degree[:asp]
    return aspect_number_natal, aspect_degree


def local_asc_mc(sun_rise1, sun_set1, sun_rise_n1, b_latitude, b_longitude, h_type, t_zone, b_offset):
    date_year_birth = sun_rise1.year
    date_month_birth = sun_rise1.month
    date_day_birth = sun_rise1.day
    date_hour_birth = sun_rise1.hour
    date_min_birth = sun_rise1.minute
    day_diff = (sun_set1 - sun_rise1) / 12
    day_diff1 = (sun_rise_n1 - sun_set1) / 12
    day_divided = 24 + 1  # 60 * 24 /20 extra for storing start of next day, 24 planetary hours in a day
    l_asc_mc = np.zeros(day_divided * 2)
    j = -1
    # print sun_rise1,sun_set1, sun_rise_n1
    for i in range(day_divided):
        # print i, date_year_birth, date_month_birth, date_day_birth, date_hour_birth, date_min_birth, day_diff
        now_julian = swe.julday(date_year_birth, date_month_birth, date_day_birth,
                                (date_hour_birth + date_min_birth / 60.) - (t_zone - b_offset))
        house_array = (swe.houses(now_julian, b_latitude, b_longitude, h_type))
        j += 1
        l_asc_mc[j] = house_array[1][0]
        j += 1
        l_asc_mc[j] = house_array[1][1]
        if i < 12:
            sun_rise1 += day_diff
            date_year_birth = sun_rise1.year
            date_month_birth = sun_rise1.month
            date_day_birth = sun_rise1.day
            date_hour_birth = sun_rise1.hour
            date_min_birth = sun_rise1.minute
        else:
            sun_set1 += day_diff1
            date_year_birth = sun_set1.year
            date_month_birth = sun_set1.month
            date_day_birth = sun_set1.day
            date_hour_birth = sun_set1.hour
            date_min_birth = sun_set1.minute
            day_diff = day_diff1
    return l_asc_mc


def planetary_hours():
    print 'to do'


def synastry(birthchart1, birthchart2, max_orb=8):
    planet = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    # asc/mc will be added when saved, same array used for no birth time.Moon stored do not use
    planet_nbt = np.array([0, 2, 3, 4, 5, 6, 7, 8, 9])  # no moon
    planet_char = (
        'sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto', 'asc', 'mc')
    planet_char_nbt = ('sun', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto')
    aspects = np.array([0, 30, 45, 60, 90, 120, 135, 150, 180])
    aspects1 = np.array([0, 30, 30, 45, 45, 60, 60, 90, 90, 120, 120, 135, 135, 150, 150, 180])
    # orbs_applying = np.array([8, 5, 6, 5, 8, 5, 6, 5, 8])
    # orbsseparating = np.array([8, 5, 6, 5, 8, 5, 6, 5, 8])

    aspect_degree = np.empty(160)
    aspect_number_natal = np.empty(160, dtype='i')
    #max_orb = 8

    # birthchart1 = np.load('../data/naren.npy')
    # birthchart2 = np.load('../data/anita.npy')
    starttime = time.clock()
    is_birthtime = True
    if is_birthtime:
        planet_natal = planet
        planet_natal_char = planet_char
        synastry_bc_a = birthchart1
        synastry_bc_b = birthchart2
        # print 'birthtime ', synastry_bc_a, synastry_bc_b
    else:
        planet_natal = planet_nbt
        planet_natal_char = planet_char_nbt
        synastry_bc_a = birthchart1[0:10]
        synastry_bc_b = birthchart2[0:10]
        # print 'nbt',synastry1,synastry2

    aspect_len = len(aspects)  # number of aspects
    aspect_len_ext = len(aspects1)
    syn_asp_planets_a = len(synastry_bc_a)
    syn_asp_planets_b = len(synastry_bc_b)

    # calculate array of birth planets based on aspects
    lenarray = syn_asp_planets_a * aspect_len_ext
    bt_array = np.empty(lenarray)  # initialize array birth time user
    # print len(bt_array),sy1_asp_planets,aspect_len1
    # Person B birth chart is in bt array
    l = 0
    temp_pos1 = np.empty(syn_asp_planets_b)
    temp_pos2 = np.empty(syn_asp_planets_b)
    for k in range(aspect_len):
        if aspects[k] == 0 or aspects[k] == 180:
            temp_pos1 = (synastry_bc_b + aspects[k]) % 360
            bt_array[l:syn_asp_planets_b + l] = temp_pos1
        else:
            temp_pos1 = (synastry_bc_b + aspects[k]) % 360
            temp_pos2 = (synastry_bc_b - aspects[k]) % 360
            bt_array[l:syn_asp_planets_b + l] = temp_pos1
            l += syn_asp_planets_b
            bt_array[l:syn_asp_planets_b + l] = temp_pos2
        l += syn_asp_planets_b
    # print len(bt_array)  # ,bt_array

    asp = 0  # counter for number of aspects
    for k in range(syn_asp_planets_a):
        natal_array_h = (synastry_bc_a[k] + max_orb) % 360
        natal_array_l = (synastry_bc_a[k] - max_orb) % 360
        #print k, birthchart2[k]
        #print 'natalarray:',k, planet_char[k],birthchart2[k],orbsapplying[j],j,aspects[j]
        if abs(natal_array_h - natal_array_l) < 40:
            ee = np.logical_and(natal_array_h > bt_array, bt_array > natal_array_l)
            aa = np.where(ee)
            aaa = np.ravel(aa)  # have all planets in aspect
            #print aaa
            for itt in aaa:
                diff = (bt_array[itt] - synastry_bc_a[k])
                g = itt // syn_asp_planets_b  # gives aspect
                gg = itt % syn_asp_planets_b  # gives planet person B
                gt = k * aspect_len * syn_asp_planets_a + ((g + 1) / 2 * syn_asp_planets_a) + gg
                aspect_number_natal[asp] = gt
                aspect_degree[asp] = diff
                # print itt,g,gg,gt,sy2_asp_planets,aspect_len,((g+1)/2)
                # print 'aspect Person A', planet_natal_char[k], ' person B ', aspects1[g], ' ', planet_char[gg], diff, gt
                asp += 1
        else:
            #checking if planets are little over 0/360 axis
            ee = np.logical_and(natal_array_h > bt_array, bt_array >= 0.)
            aa = np.where(ee)
            aaa = np.ravel(aa)  # have all planets in aspect
            #print '>0', aaa, natal_array_h, natal_array_l, bt_array[aaa]
            for ds in aaa:
                if synastry_bc_a[k] >= natal_array_l:
                    diff = 360 - synastry_bc_a[k] + bt_array[ds]
                    #print 'B1', natal_array_h, bt_array[ds], natal_array_l, synastry1[k]
                else:
                    diff = bt_array[ds] - synastry_bc_a[k]
                    #print 'B2', natal_array_h, bt_array[ds], natal_array_l, synastry1[k]
                g = ds // syn_asp_planets_b
                gg = ds % syn_asp_planets_b
                gt = k * aspect_len * syn_asp_planets_a + ((g + 1) / 2 * syn_asp_planets_a) + gg
                aspect_number_natal[asp] = gt
                aspect_degree[asp] = diff
                # print 'aspectC: Persona A', planet_natal_char[k], aspects1[g], ' Person B ', planet_natal_char[gg], diff,gt
                asp += 1
            # checking if any planets are less than 360
            ee1 = np.logical_and(natal_array_l <= bt_array, bt_array < 360.)
            aa1 = np.where(ee1)
            aaa1 = np.ravel(aa1)  # have all planets in aspect
            #print '<3600', aaa1, natal_array_h, natal_array_l, bt_array[aaa1]
            for ds in aaa1:
                if synastry_bc_a[k] >= natal_array_l:
                    diff = bt_array[ds] - synastry_bc_a[k]
                    #print 'A1', natal_array_h, bt_array[ds], natal_array_l,synastry1[k]
                else:
                    diff = 360 - bt_array[ds] + synastry_bc_a[k]
                    #print 'A2', natal_array_h, bt_array[ds], natal_array_l,synastry1[k]
                g = ds // syn_asp_planets_b
                gg = ds % syn_asp_planets_b
                gt = k * aspect_len * syn_asp_planets_a + ((g + 1) / 2 * syn_asp_planets_a) + gg
                aspect_number_natal[asp] = gt
                aspect_degree[asp] = diff
                # print 'aspectA: Person A', planet_natal_char[k], aspects1[g], 'Person B ', planet_natal_char[
                #    gg], diff,gt
                asp += 1

    aspect_number_natal = aspect_number_natal[:asp]
    aspect_degree = aspect_degree[:asp]
    return aspect_number_natal, aspect_degree


def composite_chart(birthchirt_a, birthchart_b):
    composite = np.empty(len(birthchirt_a))
    tempdeg = abs(birthchirt_a - birthchart_b)
    tempdeg2 = (birthchirt_a + birthchart_b) / 2
    for bc in range(len(tempdeg)):
        if tempdeg[bc] < 180:
            composite[bc] = tempdeg2[bc]
        else:
            temp = (tempdeg2[bc] + 180) % 360
            composite[bc] = temp
    return composite


def midpoints_calc(birthchirt_mp):
    mm = len(birthchirt_mp)
    max_midpoints = mm * (mm - 1) / 2
    # print mm, max_midpoints,midpoints_b
    midpoints = np.empty(mm * (mm - 1) / 2)
    # midpoints_name = array('c')
    for m in range(mm):
        for mk in range(m + 1, mm):
            tempdeg = abs(birthchirt_mp[m] - birthchirt_mp[mk])
            tempdeg2 = (birthchirt_mp[m] + birthchirt_mp[mk]) / 2
            midpoint_index = max_midpoints - ((mm - m) * (mm - m - 1) / 2) + mk - m - 1
            if tempdeg < 180:
                midpoints[midpoint_index] = tempdeg2
                # print 'new -midpoint of:', planet_natal_char[m], 'planet:', planet_natal_char[mk], 'deg: ', tempdeg2,midpoint_index
            else:
                temp = (tempdeg2 + 180) % 360
                midpoints[midpoint_index] = temp
                # print 'new midpoint of:', planet_natal_char[m], 'planet:', planet_natal_char[mk], 'deg: ', temp,midpoint_index
    return midpoints


def midpoint_aspects(birthchart_m, midpoints):
    midpoint_index_master = np.load('../data/midpoints/midpoint_index.npy')
    birthchart_n = np.load('../data/naren.npy')
    aspects = np.array([0, 45, 90, 135, 180])
    aspects_ext = np.array([0, 45, 45, 90, 90, 135, 135, 180])
    aspect_degree = np.empty(200)
    aspect_number_midpoint = np.empty(200, dtype='i')
    orb_mp = 2
    len_midpoints = len(midpoints)
    len_birth_planets = len(birthchart_m)
    aspect_len = len(aspects)  # number of aspects
    aspect_len_ext = len(aspects_ext)
    lenarray = len_midpoints * aspect_len_ext
    bt_array = np.empty(lenarray)  # initialize array birth time user
    l = 0
    asp_len_midpoints = len(midpoints)
    temp_pos1 = np.empty(asp_len_midpoints)
    temp_pos2 = np.empty(asp_len_midpoints)
    # print midpoints
    for k in range(aspect_len):
        if aspects[k] == 0 or aspects[k] == 180:
            temp_pos1 = (midpoints + aspects[k]) % 360
            bt_array[l:asp_len_midpoints + l] = temp_pos1
        else:
            temp_pos1 = (midpoints + aspects[k]) % 360
            temp_pos2 = (midpoints - aspects[k]) % 360
            bt_array[l:asp_len_midpoints + l] = temp_pos1
            l += asp_len_midpoints
            bt_array[l:asp_len_midpoints + l] = temp_pos2
        l += asp_len_midpoints
    asp = 0
    for k in range(len_birth_planets):
        natal_array_h = (birthchart_m[k] + orb_mp) % 360
        natal_array_l = (birthchart_m[k] - orb_mp) % 360
        # print natal_array_h,natal_array_l
        if abs(natal_array_h - natal_array_l) < 40:
            ee = np.logical_and(natal_array_h > bt_array, bt_array > natal_array_l)
            aa = np.where(ee)
            aaa = np.ravel(aa)  # have all planets in aspect
            # print 'Direct',aaa,asp_len_midpoints
            for itt in aaa:
                diff = (bt_array[itt] - birthchart_m[k])
                g = itt // asp_len_midpoints  # aspect
                gg = itt % asp_len_midpoints  # midpoint
                gt = k * 66 + gg  # + 594
                aspect_number_midpoint[asp] = gt
                aspect_degree[asp] = diff
                # print diff,aaa[itt],g,gg,aspect_len1
                #print 'Midpoint aspect-normal', gt, gg, g, planet_natal_char[k], ' ', aspects_ext[g], ' ', diff, \
                midpoint_index_master[gg]
                asp += 1
        else:
            # print 'i am here',len(bt_array)
            ee = np.logical_and(natal_array_h > bt_array, bt_array >= 0.)
            aa = np.where(ee)
            aaa = (np.ravel(aa))  # have all planets in aspect
            # print aaa
            for ds in aaa:
                # print bt_array[aaa[ds]],ds
                if birthchart_m[k] >= natal_array_l:
                    diff = 360 - birthchart_m[k] + bt_array[ds]
                    # print 'B1', natal_array_h, bt_array[aaa[ds]], natal_array_l, birthchart2[k]
                else:
                    diff = bt_array[ds] - birthchart_m[k]
                    # print 'B2', natal_array_h, bt_array[aaa[ds]], natal_array_l, birthchart2[k]
                # diff=bt_array[i]-birthchart2[k]
                #print natal_array_h[i],bt_array[i],natal_array_l[i]
                g = ds // asp_len_midpoints  #aspect
                gg = ds % asp_len_midpoints  #midpoint
                gt = k * 66 + gg  #+ 594
                aspect_number_midpoint[asp] = gt
                aspect_degree[asp] = diff
                # print 'aspectB', gt, gg, g, planet_natal_char[k], ' ', aspects_ext[g], ' ', diff, midpoint_index_master[gg]
                asp += 1
            ee1 = np.logical_and(natal_array_l <= bt_array, bt_array < 360.)
            aa1 = np.where(ee1)
            aaa = np.ravel(aa1)  # have all planets in aspect
            # print 'naren',aaa
            for ds in aaa:
                # print bt_array[aaa[ds]],ds
                if birthchart_m[k] >= natal_array_l:
                    diff = bt_array[ds] - birthchart_m[k]
                    #print 'A1', natal_array_h, bt_array[ds], natal_array_l, birthchart2[k]
                else:
                    diff = 360 - bt_array[ds] + birthchart_m[k]
                    #print 'A2', natal_array_h, bt_array[ds], natal_array_l, birthchart2[k]
                #print natal_array_h[i],bt_array[i],natal_array_l[i]
                #diff=bt_array[i]-birthchart2[k]
                g = ds // asp_len_midpoints  #aspect
                gg = ds % asp_len_midpoints  #aspect
                gt = k * 66 + gg  #+ 594
                aspect_number_midpoint[asp] = gt
                aspect_degree[asp] = diff
                # print 'aspectA', gt, gg, g, planet_natal_char[k], ' ', aspects_ext[g], ' ', diff, midpoint_index_master[gg]
                asp += 1

    aspect_number_midpoint = aspect_number_midpoint[:asp]
    aspect_degree = aspect_degree[:asp]
    return aspect_number_midpoint, aspect_degree