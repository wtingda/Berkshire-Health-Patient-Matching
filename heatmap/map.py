import random

import googlemaps

gmaps = googlemaps.Client(key="AIzaSyDE_MLUeIdpPgnCWEV-ZgscLCO1734Ax3w")
gcoderesult = gmaps.geocode("Berkshire County")
print(gcoderesult)

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
#print(gcoderesult[0]['geometry']['location']['lat'])


clinics_lat = []
clinics_long = []

# imports list of churches and finds their coordinates via geocode
with open("churches.txt",'r') as f:
    lines = f.readlines()
    for i in range(len(lines)):
        if i % 2 == 1:
            address = lines[i].strip()
            coords = gmaps.geocode(address)
            clinics_lat.append(coords[0]['geometry']['location']['lat'])
            clinics_long.append(coords[0]['geometry']['location']['lng'])


num_patients = 300
num_clinics = 30

patients_lat = []
patients_long = []

# samples randomly from list of Berkshire addresses
with open("berkshire.csv", 'r') as f:

    data = f.readlines()
    dataLen = len(data)
    for i in range(num_patients):
        index = random.randint(0,dataLen-1)
        patients_long.append(float(data[index].split(',')[0]))
        patients_lat.append(float(data[index].split(',')[1]))

# todo: search if there's 2d random generating coordinates
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
#
# def random_float(lower, upper):
#     diff = upper - lower
#     val = random.random()*diff + lower
#     while val > upper:
#         val = random.random()*diff + lower
#     return val
#
# patients_latitude = [random_float(br[0], tl[0]) for _ in range(num_patients)]
# patients_longtitude = [random_float(bl[1], tr[1]) for _ in range(num_patients)]
# clinics_latitude = [random_float(br[0], tl[0]) for _ in range(num_clinics)]
# clinics_longtitude = [random_float(bl[1], tr[1]) for _ in range(num_clinics)]
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
# berkshire_coord = (42.3118, -73.1822)
gmap = gmplot.GoogleMapPlotter(gcoderesult[0]['geometry']['location']['lat'], gcoderesult[0]['geometry']['location']['lng'], 10.5)

gmap.heatmap(patients_lat, patients_long)

for x,y in zip(clinics_lat, clinics_long):
    gmap.marker(x,y, "darkred")

def calc_dist(start, end): # start and end are each a coordiate of (lat, long)
    d = gmaps.distance_matrix([str(start[0]) + " " + str(start[1])], [str(end[0]) + " " + str(end[1])], mode='driving')['rows'][0]['elements'][0]
    dist =  d['distance']['value']
    return {end: dist}

def find_nearest(patient_coord, topk=1):
    # dist = [geodesic(patient_coord, clinic).miles for clinic in clinics_coord]
    # dist = [calc_dist(patient_coord, clinic) for clinic in clinics_coord]
    dist = [calc_dist(patient_coord, clinic) for clinic in zip(clinics_lat, clinics_long)] # list of dicts
    # return sorted(dist)[:topk]
    return sorted(dist, key=lambda x: list(x.values())[0])[:topk]

# patients_coord = zip(patients_lat, patients_long)
print("\n\n")
p1 = (42.0434466, -73.1208865) # some patient from berkshires.csv
gmap.marker(p1[0], p1[1], "blue")
p1_nearest = [list(d.keys())[0] for d in find_nearest(p1, 3)]
print(p1_nearest)
for x, y in p1_nearest:
    gmap.marker(x,y, "green")

gmap.apikey = "AIzaSyDE_MLUeIdpPgnCWEV-ZgscLCO1734Ax3w"

gmap.draw("my_map.html")
