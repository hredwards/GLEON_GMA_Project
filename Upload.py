import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from uploadDownload import uploadBar





def Upload():
    layout = html.Div([
        uploadBar
    ], className="page-content")
    return layout

