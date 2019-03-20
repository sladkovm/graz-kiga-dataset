# Graz kiga dataset

## Content

1. Dataset as a *json* file
2. ETL script to regenerate the dataset by parsing the appropriate pages from ABI-Service Graz

## Structure of the dataset

```
[{
 "district": "XI. Mariatrost",
 "name": "Kinderkrippe Sch\u00f6nbrunngasse", 
 "address": "Sch\u00f6nbrunngasse 30, 8043 Graz", 
 "tel": "Tel.: +43 316 872-2780", 
 "n_groups": "Anzahl der Gruppen: 5 GT", 
 "time": "\u00d6ffnungszeiten: Montag bis Freitag von 07.00 bis 17.00 Uhr", "more": "Mehr Infos", 
 "GT": 5, 
 "location": {
     "place_id": 27361661,
      "licence": "Data \u00a9 OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright", 
      "osm_type": "node", 
      "osm_id": 2601774773, 
      "boundingbox": ["47.0901141", "47.0902141", "15.4550976", "15.4551976"], 
      "lat": "47.0901641", 
      "lon": "15.4551476", 
      "display_name": "Endre Ady, 30, Sch\u00f6nbrunngasse, Geidorf, Graz, Steiermark, 8043, \u00d6sterreich", 
      "class": "historic", 
      "type": "memorial", 
      "importance": 0.6924713915777061, 
      "icon": "https://nominatim.openstreetmap.org/images/mapicons/tourist_monument.p.20.png"}
      },...
]
```

## Important dependencies

1. *bonobo* 
2. *Google API*