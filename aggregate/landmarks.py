import json
from geopy.geocoders import Nominatim


lm = [
    {
        "name": "Hauptplatz",
        "address": "Hauptplatz 1, 8010 Graz"
    },
    {
        "name": "HBHF",
        "address": 'hauptbahnhof, Graz'
    },
    {
        "name": "Uni Graz",
        "address": "Universitätsplatz 3, 8010 Graz"
    },
    {
        "name": "TU Graz",
        "address": "Rechbauerstraße 12, 8010 Graz"
    }, 
    {
        "name": "TU Know Center",
        "address": "Inffeldgasse 13, 8010 Graz"
    },
    {
        "name": "LKH Graz",
        'address': "Auenbruggerplatz 1, 8036 Graz"
    }
]   


if __name__ == "__main__":

    geolocator = Nominatim(user_agent="Kiga Graz")
    ouput = []
    for _ in lm:
        loc = geolocator.geocode(_["address"])
        _.update({"location": loc.raw})
        _.update({'lat': loc.latitude})
        _.update({'lon': loc.longitude})
        ouput.append(_)


    with open('data/landmarks.json', 'w') as f:
        json.dump(ouput, f)