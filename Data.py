import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from forDataTab import get_metadata_table_content, dataPageTable, refreshButton, Bucket





body = dbc.Container(
    [
       dbc.Row(html.H3("Welcome to the Data Page!")),
        dbc.Row(html.P("""This is the Data page, this would have downloads for all data""")),
        dataPageTable,
    ],
    className="mt-4",
)


def Data():
    layout = html.Div([
        body,
    ])
    return layout

