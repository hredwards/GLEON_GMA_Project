"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from navbar import NavBar
import dash_bootstrap_components as dbc
import os

external_stylesheets = ['/assets/main.css']
app = dash.Dash(__name__, external_stylesheets= external_stylesheets)
server = app.server
app.server.secret_key = os.getenv("Flask_SK")
#app.server.secret_key = "6d8528c3750143f18s62e871"


app.layout = html.Div([
    html.Div(id='blank-output'),
    dcc.Location(id = 'url', refresh = True),
    NavBar(),
    html.Div(id = 'page-content')
],
)

app.config['suppress_callback_exceptions'] = True
"""