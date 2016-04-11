import array
import datetime
import numpy as np

EPH_ARRAY = np.load('astro/data/ephemeris/eph-ns.npy')
EPH_DATE_START = datetime.datetime(1915, 1, 1)  # YYYY, MM, DD
#EPH_PLANETS = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9,15,19])  # NATAL PLANETS FOR ephemeris CALCULATION ONLY

# SUN=0, MOON=1, MERCURY=2, VENUS=3, MARS=4, JUPITER=5, SATURN=6, URANUS=7, NEPTUNE=8, PLUTO=9,
# CHIRON=15, JUNO=19 --- These are as defined in Swiss ephemeris -- following two are our definition ASC=10, MC=11
EPHEMERIS_PLANETS = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9,15,19], dtype=np.int16)  # NATAL PLANETS+ASC+MC

NATAL_PLANETS = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], dtype=np.int16)  # NATAL PLANETS+ASC+MC
LEN_NATAL_PLANETS = 12  # len(NATAL_PLANETS)
TRANSIT_PLANETS = np.array([5, 6, 7, 8, 9], dtype=np.int16)  # transit planets MAJOR EVENTS

TRANSIT_ASPECTS = np.array([0, 60, 90, 120, 180], dtype=np.int16)
TRANSIT_ASPECTS_EXT = np.array([0, 60, 60, 90, 90, 120, 120, 180], dtype=np.int16)
L_TRANSIT_ASPECTS = len(TRANSIT_ASPECTS)
L_TRANSIT_ASPECTS_EXT = len(TRANSIT_ASPECTS_EXT)

NATAL_PLANETS_TIMING = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])  # NATAL PLANETS+ASC+MC
TRANSIT_PLANETS_TIMING = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])  # transit planets all
TRANSIT_ASPECTS_TIMING = np.array([0, 30, 45, 60, 90, 120, 135, 150, 180])  # aspects used in timing
TRANSIT_ASPECTS2_TIMING = np.array([0, 30, 30, 45, 45, 60, 60, 90, 90, 120, 120, 135, 135, 150, 150, 180])
PLANET_CHARS_TIMING = ('Su', 'Mo', 'Me', 'Ve', 'Ma', 'Ju', 'Sa', 'Ur', 'Ne', 'Pl', 'As', 'Mc')

PLANET_CHARS = ('Su', 'Mo', 'Me', 'Ve', 'Ma', 'Ju', 'Sa', 'Ur', 'Ne', 'Pl', 'As', 'Mc')
PLANET_CHARS_NBT = ('Su', 'Me', 'Ve', 'Ma', 'Ju', 'Sa', 'Ur', 'Ne', 'Pl')

BIRTH_PLANETS = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])  # NATAL PLANETS FOR BIRTH CHART CALCULATION ONLY
NATAL_ASPECTS = np.array([0, 30, 45, 60, 90, 120, 135, 150, 180])
NATAL_ASPECTS_EXT = np.array([0, 30, 30, 45, 45, 60, 60, 90, 90, 120, 120, 135, 135, 150, 150, 180])
LEN_NATAL_ASPECTS = len(NATAL_ASPECTS)
LEN_NATAL_ASPECTS_EXT = len(NATAL_ASPECTS_EXT)
NATAL_ORBS_APPLYING = np.array([8, 5, 6, 5, 8, 5, 6, 5, 8])
NATAL_ORBS_SEPARATING = np.array([8, 5, 6, 5, 8, 5, 6, 5, 8])

ASTEROIDS_PLANETS = array.array('i', [47])

# TRANSIT ASPECTS
ASPECTS = np.array([0, 30, 45, 60, 90, 120, 135, 150, 180])
LEN_TRANIT_ASPECTS = len(ASPECTS)
ORBSAPPLYING = np.array([10, 3, 3, 6, 10, 10, 5, 3, 10])
ORBSSEPARATING = np.array([10, 3, 3, 6, 10, 10, 5, 3, 10])
SIGN_ZODIAC = (
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sag', 'Capricorn', 'Aquarius', 'Pisces')