from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from s3References import dfCreds
from app import app
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from Layouts import Upload
from navbar import NavBar


class User:
    def __init__(self, id, username, password, fullName):
        self.id = id
        self.username = username
        self.password = password
        self.fullName = fullName

    def __repr__(self):
        return f'<User: {self.username}>'


users = []

for index, row in dfCreds.iterrows():
    users.append(User(id=row["id"], username=row["user"], password=row["pass"], fullName=row["name"]))


@app.server.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user



@app.server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect('/successLogin')

        return redirect('/Login')

    return redirect('/Login')


@app.server.route('/successLogin')
def profile():
    if not g.user:
        return redirect('/Login')

    return redirect('/Upload')


login_form = dbc.Row([
    html.Form([
        dcc.Input(placeholder='username', name='username', type='text'),
        dcc.Input(placeholder='password', name='password', type='password'),
        html.Button('Login', type='submit')
    ], action='/login', method='post')
], justify="center", form=True,   className="twelve columns",
)

login = html.Div([
    dbc.Row(html.H3("Welcome to the Login Page!"), justify="center", form=True, className="twelve columns"),
    html.Div(id='custom-auth-frame'),
    html.Div(id='custom-auth-frame-1', style={'textAlign': 'right', "background": "black"}),
    login_form,
    dbc.Row(dbc.Button("Want a login?", href="/Contact", color="secondary", style={"margin":"2rem"}), justify="center", form=True),
], className="pretty_container four columns offset-by-four columns",
)


def Login():
    layout = login
    return layout