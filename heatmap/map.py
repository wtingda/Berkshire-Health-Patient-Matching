import random

import googlemaps

from gmplot import gmplot

# we haven't found a way to automatically locate berkshire county on goolge map using gmplot, so we got the rough coordinates of the four corners on map
tl = (42.745941, -73.264959)
tr = (42.738711, -72.948854)
bl = (42.051087, -73.493993)
br = (42.041317, -73.056959)

# lat1 = tl[0] - tr[0]
# lat2 = bl[0] - br[0]
# long1 = tl[1] - tr[1]
# long2 = bl[1] - br[1]
#
# # choose the shorter longitude and latitude for sampling
# lat = min(lat1, lat2)
# long = min(long1, long2)
gmaps = googlemaps.Client(key="AIzaSyDE_MLUeIdpPgnCWEV-ZgscLCO1734Ax3w")
gcoderesult = gmaps.geocode("Berkshire County")
print(gcoderesult)

# generating coordinates of patients and clinics
# todo: integrate with patient & clinic info with real / tingda & tongyu
num_patients = 294
num_clinics = 30

def random_float(lower, upper):
    diff = upper - lower
    val = random.random()*diff + lower
    while val > upper:
        val = random.random()*diff + lower
    return val

patients_latitude = [random_float(br[0], tl[0]) for _ in range(num_patients)]
patients_longtitude = [random_float(bl[1], tr[1]) for _ in range(num_patients)]
clinics_latitude = [random_float(br[0], tl[0]) for _ in range(num_clinics)]
clinics_longtitude = [random_float(bl[1], tr[1]) for _ in range(num_clinics)]
# patients_latitude = np.random.uniform(br[0], tl[0], num_patients)
# # print(patients_latitude)
# patients_longtitude = np.random.uniform(bl[1], tr[1], num_patients)
# # print(patients_longtitude)
# patients_coord = zip(patients_latitude, patients_longtitude)
# # for tup in patients_coord:
# #     print(tup)
# clinics_latitude = np.random.uniform(br[0], tl[0], num_clinics)
# # print(patients_latitude)
# clinics_longtitude = np.random.uniform(bl[1], tr[1], num_clinics)


####################################################################################
# berkshire_coord = (42.3118, 73.1822)
gmap = gmplot.GoogleMapPlotter(42.446, -73.192, 10.5)

gmap.heatmap(patients_latitude, patients_longtitude)

for x,y in zip(clinics_latitude, clinics_longtitude):
    gmap.marker(x,y, "darkred")

# todo: add outline on map

gmap.apikey = "AIzaSyDE_MLUeIdpPgnCWEV-ZgscLCO1734Ax3w"

gmap.draw("my_map.html")
