from geopy.geocoders import Nominatim, ArcGIS
from unidecode import unidecode

geolocator = Nominatim(user_agent='test')
s = "St.-Peter-Haußtstraße 85, 8042 Graz"
print(unidecode(s))


# g = geolocator.geocode(unidecode(s))
# print(g.address)


g_arcgis = ArcGIS()
g = g_arcgis.geocode(unidecode(s))
print(g.address)
print(g.raw)
print(g.latitude)
print(g.longitude)