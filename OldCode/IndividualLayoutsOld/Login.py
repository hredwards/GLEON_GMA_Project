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
        return flask.redirect('/Login')
    else:

        # Return a redirect with
        rep = flask.redirect(_app_route)
        rep.set_cookie('custom-auth-session', username)
        return rep



login_form = dbc.Row([
    html.Form([
        dcc.Input(placeholder='username', name='username', type='text'),
        dcc.Input(placeholder='password', name='password', type='password'),
        html.Button('Login', type='submit')
    ], action='/login', method='post')
], justify="center", form=True,   className="twelve columns",
)



body = html.Div([
    dbc.Row(html.H3("Welcome to the Login Page!"), justify="center", form=True, className="twelve columns"),
    html.Div(id='custom-auth-frame'),
    html.Div(id='custom-auth-frame-1', style={'textAlign': 'right', "background": "black"}),
    login_form,
    dbc.Row(dbc.Button("Want a login?", href="/Contact", color="secondary", style={"margin":"2rem"}), justify="center", form=True),
], className="pretty_container four columns offset-by-four columns",
)




def Login():
    layout = body
    return layout

