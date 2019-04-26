import os
import json
import pandas as pd
import plotly.graph_objs as go


mapbox_access_token = os.getenv('MAPBOX', None)
if mapbox_access_token is None:
    raise ValueError('Mapbox access token is None')

with open('data/krippe_stad.json') as f:
    krippe_stad = json.load(f)
with open('data/krippe_privat.json') as f:
    krippe_privat = json.load(f)
with open('data/landmarks.json') as f:
    landmarks = json.load(f)


df_stad = pd.DataFrame(krippe_stad)
df_privat = pd.DataFrame(krippe_privat)
df_landmarks = pd.DataFrame(landmarks)


data = [
    go.Scattermapbox(
        name='Stadt',
        lat=df_stad.lat,
        lon=df_stad.lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=df_stad.GT*5,
            color='green'
        ),
        text=df_stad.name,
    ), 
    
    go.Scattermapbox(
        name='Privat',
        lat=df_privat.lat,
        lon=df_privat.lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=10,
            color='blue'
        ),
        text=df_privat.name,
    ),
    
    go.Scattermapbox(
        name='Landmarks',
        lat=df_landmarks.lat,
        lon=df_landmarks.lon,
        mode='markers+text',
        textposition="bottom center",
        marker=go.scattermapbox.Marker(
            size=10,
            color='red'
        ),
        text=df_landmarks.name,
        textfont=dict(color='red')
    )
]



layout = go.Layout(
    title='Kinderkrippe Graz 2019',
    autosize=True,
    width=1024,
    height=1024,
    legend=dict(orientation="h", x=0, y=0),
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=df_landmarks.loc[0].lat,
            lon=df_landmarks.loc[0].lon
        ),
        pitch=0,
        zoom=12
    )
)

map_plot = dict(data=data, layout=layout)
# iplot(fig, filename='Kiderkrippe Graz')