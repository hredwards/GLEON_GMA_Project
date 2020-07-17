"""""
This will host the app itself

"""""

"""""
Notes from last session/ things Hallie would otherwise forget

This is a github linked project so commit changes once you're ready to test deployment
shortcuts/notes are in the notes/txt file in this project
"""""



"""""
Import required libraries
"""""
import os
import pickle
import copy
import datetime as dt
import math

import requests
import pandas as pd
from flask import Flask
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html



"""""
Initial Set Up options - server, other file/function imports
"""""
# pulls Multi-dropdown options for filters from controls.py; initialized in persistent variable definitions section
from controls import DB_Info, Reporting_Measures, Microcystin_Method, Field_Methods, Sample_Types, Substrate_Status, COUNTRIES, LAKES

# Initialize Dash App server; uses file called Oldapp.py as thing to host
app = dash.Dash(__name__)
server = app.server



"""""
Persistent Variable Definitions
"""""
# Year range definition -- change to be min/max of year from DATETIME in df??
Year_Range = [2000, 2020]


# Create controls - these reference definitions in controls.py
Substrate_Status_options = [{'label': str(Substrate_Status[substrate_status]),
                      'value': str(substrate_status)}
                     for substrate_status in Substrate_Status]

Sample_Types_options = [{'label': str(Sample_Types[sample_types]),
                      'value': str(sample_types)}
                     for sample_types in Sample_Types]

Field_Methods_options = [{'label': str(Field_Methods[field_methods]),
                      'value': str(field_methods)}
                     for field_methods in Field_Methods]

Microcystin_Method_options = [{'label': str(Microcystin_Method[microcystin_method]),
                      'value': str(microcystin_method)}
                     for microcystin_method in Microcystin_Method]

Reporting_Measures_options = [{'label': str(Reporting_Measures[reporting_measures]),
                      'value': str(reporting_measures)}
                     for reporting_measures in Reporting_Measures]

DB_Info_options = [{'label': str(DB_Info[db_info]),
                      'value': str(db_info)}
                     for db_info in DB_Info]



"""""
Satellite Overview/Mapbox Config
"""""
# Create global chart template from mapbox public API token
mapbox_access_token = 'pk.eyJ1IjoiZ2xlb25nbWEiLCJhIjoiY2s3NGJ6amdiMDZ6NDNsczk1cjQwZHMxeiJ9.d9oeGzHUbPW0FRTOm6gUPA'

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(
        l=30,
        r=30,
        b=20,
        t=40
    ),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation='h'),
    title='Satellite Overview',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(
            lon=-38.14,
            lat=-41.29
        ),
        zoom=3,
    )
)

"""""
App layout Begins. This uses Dash HTML components to layout different sections of the site. Mostly aesthetics; data is pulled later
"""""
app.layout = html.Div(
    [
        dcc.Store(id='aggregate_data'),
        html.Div(
            [
                html.Div( ## this is for the header; title, subtitle, and learn more link--eventually replace with links to other pages on dash
                    [html.Img(src="https://gleon.org/sites/default/files/images/Logo1.JPG", className='three columns'),
                     html.H2('GLEON GMA',),
                     html.H5('Global Microsytin Aggregation Project',)], className='five columns'),

                html.Div( ## this is for the header; title, subtitle, and learn more link--eventually replace with links to other pages on dash
                    [html.A(html.Button("Home", id="homePage"), href="http://127.0.0.1:8050/", className="five columns"),
                     html.A(html.Button("About", id="aboutPage"), href="https://gleon.org/research/projects/global-microcystin-aggregation-gma", className="five columns"),
                     html.A(html.Button("Data", id="dataPage"), href="https://gleon.org/research/projects/global-microcystin-aggregation-gma", className="five columns"),
                     html.A(html.Button("Contact", id="contactPage"), href="https://gleon.org/research/projects/global-microcystin-aggregation-gma", className="five columns"),
                     html.A(html.Button("Login", id="loginPage"), href="http://127.0.0.1:8050/login", className="five columns"),
                     ],
            id="header",
            className='row',
        )])])





"""""
App Callbacks start - these take input and return outputs
"""""


"""""
App callbacks for table with summary variables -- UPDATE ONCE WE HAVE DATASET FIGURED OUT--POSTGRE EQUIVALENT?
"""""







"""""
Initialize the actual server from this file
"""""
# Main
if __name__ == '__main__':
    app.run_server(debug=True)
