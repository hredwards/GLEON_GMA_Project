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


session_cookie = flask.request.cookies.get('custom-auth-session')

def logInOut():
    session_cookie = flask.request.cookies.get('custom-auth-session')

    if not session_cookie:
        # If there's no cookie we need to login.
        return [html.Div(html.H2("Charts will be displayed here after user's authentication."),
                         style={'textAlign': 'center',
                                'color': 'red'}), '', login_form]
    else:
        logout_output = html.Div(children=[html.Div(html.H3('Hello {} !'.format(usersNames[session_cookie])),
                                                    style={'display': 'inline-block'}),
                                           html.Div(dcc.LogoutButton(logout_url='/logout'),
                                                    style={'display': 'inline-block'})],
                                 style={
                                     'color': 'green',
                                     'height': '50px'
                                 }
                                 )
        return [logout_output]



body = dbc.Container(
    [
       dbc.Row(html.H3("Welcome to the Login Page!")),
        dbc.Row(html.P("""This is the Login page, this would have a login box ofr registered users and a redirect to
                         the contact page""")),
        logInOut(),
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
    className="mt-4",
)



@app.callback(Output('custom-auth-frame-1', 'children'))
def render_content():
    session_cookie = flask.request.cookies.get('custom-auth-session')

    if not session_cookie:
        # If there's no cookie we need to login.
        return [html.Div(html.H2("Charts will be displayed here after user's authentication."),
                         style={'textAlign': 'center',
                                'color': 'red'}), '', login_form]
    else:
        logout_output = html.Div(children=[html.Div(html.H3('Hello {} !'.format(usersNames[session_cookie])),
                                                    style={'display': 'inline-block'}),
                                           html.Div(dcc.LogoutButton(logout_url='/logout'),
                                                    style={'display': 'inline-block'})],
                                 style={
                                     'color': 'green',
                                     'height': '50px'
                                 }
                                 )
        return [logout_output]




def Login():
    layout = html.Div([
        body
    ])
    return layout

