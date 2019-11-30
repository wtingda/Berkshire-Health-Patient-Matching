import numpy as np

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

num_patients = 294
num_clinics = 30
# todo: search if there's 2d random generating coordinates
patients_latitude = np.random.uniform(br[0], tl[0], num_patients)
# print(patients_latitude)
patients_longtitude = np.random.uniform(bl[1], tr[1], num_patients)
# print(patients_longtitude)
patients_coord = zip(patients_latitude, patients_longtitude)
for tup in patients_coord:
    print(tup)
