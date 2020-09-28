""""
This file contains all app callbacks and pathname redirects. This is the app that is ran to start the server as defined in the procfile
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from Layouts import About, Data, Contact#, Upload #, UserPage
from navbar import NavBar
import boto3
import io
from botocore.client import Config
from app import app
import os
from ViewFilteredData import filtersAvailable, FilteredView
from Homepage import Homepage
from LoginWithSessions import Login, UserPage, uploadPage
from flask import g, redirect, session


"""
from Homepage import Homepage
from About import About
from Data import Data
from ViewFilteredData import FilteredView
from Contact import Contact
from Login import Login, login_form
from Upload import Upload

"""

app.config['suppress_callback_exceptions'] = True
server = app.server


#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

""""
This defines the css file(s) to be used and defines the app and server. It also establishes an empty dataframe and the app layout.
The app layout pulls the URL/pathname and the display_page app callback below loads the page layout based on this URL
"""





""""
This returns the page layout based on pathname; these are all defined in their respective .py files
"""


@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/Homepage':
        return Homepage()
    elif pathname == '/':
        return Homepage()
    elif pathname == '/FilterData':
        return FilteredView()
    elif pathname == '/About':
        return About()
    elif pathname == '/Data':
        return Data()
    elif pathname == '/Contact':
        return Contact()
    elif pathname == '/Login' and 'user_fullName' not in session:
        return Login()
    elif pathname == '/Login' and 'user_fullName' in session:
        return UserPage()
    elif pathname == '/Logout':
        return Login()
    elif pathname == '/Upload' and 'user_fullName' in session:
        return uploadPage()
    elif pathname == '/Upload' and 'user_fullName' not in session:
        return Login()
    elif pathname == '/UserPage':
        return UserPage()
    else:
        return Homepage()


"""
Sets the tab text based on the current URL; this code is javascript, not python, which is why it looks off
"""

app.clientside_callback(
    """
    function(pathname) {
        if (pathname === '/Homepage') {
            document.title = "Homepage - GLEON GMA Project"
        } else if (pathname === '/') {
            document.title = "Homepage - GLEON GMA Project"
        } else if (pathname === '/FilterData') {
            document.title = "Filter Graphs - GLEON GMA Project"
        } else if (pathname === '/About') {
            document.title = "About - GLEON GMA Project"
        } else if (pathname === '/Data') {
            document.title = "Data - GLEON GMA Project"
        } else if (pathname === '/Contact') {
            document.title = "Contact - GLEON GMA Project"
        } else if (pathname === '/Login') {
            document.title = "Login - GLEON GMA Project"
        } else if (pathname === '/Upload') {
            document.title = "Upload - GLEON GMA Project"
        } else if (pathname === '/UserPage') {
            document.title = "User's Page - GLEON GMA Project"
        } else {
            document.title = "Homepage - GLEON GMA Project"            
        }
    }
    """,
    Output('blank-output', 'children'),
    [Input('url', 'pathname')]
)


""""
This Callback just uses the url/pathname to determine which page is active.
Right now, the only place this is used is in navbar.py to determine the active page.
The active page is then set to have a 'pill' in the nav bar. This is just the box behind the nav link indicating 
which page you are on
"""

@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 8)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/Homepage":
        return True, False, False, False, False, False, False
    elif pathname == "/":
        return True, False, False, False, False, False, False
    elif pathname == "/About":
        return False, True, False, False, False, False, False
    elif pathname == "/FilterData":
        return False, False, True, False, False, False, False
    elif pathname == "/Data":
        return False, False, False, True,  False, False, False
    elif pathname == "/Login":
        return False, False, False, False, False, True, False
    elif pathname == "/UserPage":
        return False, False, False, False, False, True, False
    elif pathname == "/Upload":
        return False, False, False, False, False, False, True
    elif pathname == "/Contact":
        return False, False, False, False, True, False, False
    else:
        return False, False, False, False, False, False, False, False




if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)

