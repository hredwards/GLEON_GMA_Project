import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from uploadDownload import dataPageTable




body = html.Div(
    [
       dbc.Row(html.H3("Welcome to the Data Page!")),
        dbc.Row(html.P("""This is the Data page, this would have downloads for all data""")),
        dataPageTable,
    ],
    className="mt-4 twelve columns",
)


def Data():
    layout =body
    return layout

