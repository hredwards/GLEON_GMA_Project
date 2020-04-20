import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from uploadDownload import uploadBar



body = dbc.Container(
    [
       dbc.Row(html.H3("Welcome to the Upload Page!")),
    ],
    className="mt-4",
)


def Upload():
    layout = html.Div([
        body,
        uploadBar
    ])
    return layout

