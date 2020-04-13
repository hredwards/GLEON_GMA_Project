import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from navbar import NavBar
import dash_bootstrap_components as dbc




external_stylesheets = ['/assets/main.css']
app = dash.Dash(__name__, external_stylesheets= external_stylesheets)
server = app.server


app.layout = html.Div([
    dcc.Location(id = 'url', refresh = True),
    NavBar(),
    html.Div(id = 'page-content')
],
)

