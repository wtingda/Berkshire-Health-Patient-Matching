import googlemaps

from map import gmaps

# # example
# origin_latitude = 12.9551779
# origin_longitude = 77.6910334
# destination_latitude = 28.505278
# destination_longitude = 77.327774
# distance = gmaps.distance_matrix([str(origin_latitude) + " " + str(origin_longitude)], [str(destination_latitude) + " " + str(destination_longitude)], mode='walking')['rows'][0]['elements'][0]
# print(distance)

# # geopy example
from geopy.distance import geodesic
# newport_ri = (41.49008, -71.312796)
# cleveland_oh = (41.499498, -81.695391)
# print(geodesic(newport_ri, cleveland_oh).miles)

from map import patients_latitude, patients_longtitude, clinics_latitude, clinics_longtitude
patients_coord = zip(patients_latitude, patients_longtitude)
clinics_coord = zip(clinics_latitude, clinics_longtitude)

# todo: could calculate once a 2d table/dict of distance btw each patient and each clinic

def find_nearest(patient_coord, topk=1):
    # todo: use googlemaps.distance_matrix instead!
    dist = [geodesic(patient_coord, clinic).miles for clinic in clinics_coord]
    return sorted(dist)[:topk]

sample_patient = (42.073423320147626, -72.9493080716857)
print( find_nearest(sample_patient, 3) )
# for tup in patients_coord:
#     print(tup)
