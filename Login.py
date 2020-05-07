import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask
from s3References import creds, usersNames
from app import app
from dash.dependencies import Input, Output


# Create a login route
_app_route = '/PageUpload'

@app.server.route('/login', methods=['POST'])
def route_login():
    data = flask.request.form
    username = data.get('username')
    password = data.get('password')

    if username not in creds.keys() or  creds[username] != password:
        return flask.redirect('/PageLogin')
    else:

        # Return a redirect with
        rep = flask.redirect(_app_route)
        rep.set_cookie('custom-auth-session', username)
        return rep



login_form = html.Div([
    html.Form([
        dcc.Input(placeholder='username', name='username', type='text'),
        dcc.Input(placeholder='password', name='password', type='password'),
        html.Button('Login', type='submit')
    ], action='/login', method='post')
])



body = dbc.Container(
    [
       dbc.Row(html.H3("Welcome to the Login Page!")),
        html.Div(id='custom-auth-frame'),
        html.Div(id='custom-auth-frame-1',
           style={
                  'textAlign': 'right',
                  "background": "black",
           }
           ),
        login_form,
        dbc.Button("Want a login?", href="/PageContact", color="secondary"),
    ],
    className="mt-4 pretty_container twelve columns",
)




def Login():
    layout = html.Div([
        body
    ])
    return layout

