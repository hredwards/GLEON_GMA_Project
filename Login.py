import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html



body = dbc.Container(
    [
       dbc.Row(html.H3("Welcome to the Login Page!")),
        dbc.Row(html.P("""This is the Login page, this would have a login box ofr registered users and a redirect to
                         the contact page""")),
        dbc.Button("Want a login?", href="/PageContact", color="secondary"),
    ],
    className="mt-4",
)


def Login():
    layout = html.Div([
        dcc.Location(id="url"),
        body
    ])
    return layout

