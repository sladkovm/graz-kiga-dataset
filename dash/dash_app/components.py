import os
import json
import pandas as pd
import plotly.graph_objs as go
from geopy import Nominatim
from geopy.distance import geodesic
import dash_table
import numpy as np
import dash_html_components as html
import dash_core_components as dcc


geocoder = Nominatim(user_agent='Kiga Graz')

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


def make_address(address='Hasnerplatz 1, 8010 Graz'):
    rv =  html.Div(className='input-group mb3',
        children=[
            html.Div(className='input-group-prepend',
            children=[
                html.Span(className='input-group-text', children=['Address']),
                dcc.Input(id='address-input',
                    className='form-control',
                    style={'width': 475},
                    value=address,
                    type='text'),
                html.Button('Submit', id='submit', className='btn btn-primary')
            ])
        ])

    return rv


def make_table(address="Hasnerplatz 1, 8010 Graz"):
    home = geocoder.geocode(address)
    if home is None:
        return None
    df = pd.concat([df_stad, df_privat], sort=False)
    df = df[['name', 'address', 'lat', 'lon']].dropna()
    df['km'] = df.apply(lambda x: np.round(geodesic((x.lat, x.lon), (home.latitude, home.longitude)).km, 2), axis=1)
    df.sort_values(by='km', inplace=True)
    df = df[['name', 'address', 'km']]
    
    rv = dash_table.DataTable(
        id='table',
        row_selectable="single",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
        style_table={
            'textAlign': 'left',
            'maxHeight': '600px',
            'overflowY': 'scroll'
        },  
        style_cell_conditional=[
            {'if': {'column_id': 'name'},
            'maxWidth': '150px', 'textAlign': 'left',},
            {'if': {'column_id': 'address'},
            'maxWidth': '150px', 'textAlign': 'right',},
            {'if': {'column_id': 'km'},
            'maxWidth': '25px', 'textAlign': 'right',}
        ]   ,
        style_as_list_view=True,
        style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold'
    },
    )
    return rv


def make_plot(address="Hasnerplatz 1, 8010 Graz"):
    home = geocoder.geocode(address)

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
        ),

        go.Scattermapbox(
            name='Home',
            lat=[home.latitude],
            lon=[home.longitude],
            mode='markers+text',
            textposition="bottom center",
            marker=go.scattermapbox.Marker(
                size=10,
                color='orange'
            ),
            text=['Home'],
            textfont=dict(color='orange')
        )

    ]

    layout = go.Layout(
        autosize=True,
        width=600,
        height=650,
        margin=go.layout.Margin(
            l=50,
            r=0,
            b=0,
            t=0,
            pad=4
        ),
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

    return dict(data=data, layout=layout)
