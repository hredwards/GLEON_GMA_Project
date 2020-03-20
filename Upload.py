import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html



body = dbc.Container(
    [
       dbc.Row(html.H3("Welcome to the Upload Page!")),
        dbc.Row(html.P("""This is the upload page, this would be where users upload to after logging in. This won't be a link on the final version, it will only appear once logged in""")),
    ],
    className="mt-4",
)


def Upload():
    layout = html.Div([
        body
    ])
    return layout

