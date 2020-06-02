import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from uploadDownload import dataPageTable




body = html.Div(
    [
       dbc.Row(html.H3("Welcome to the Data Page!"), justify="center", form=True),
        dbc.Row(html.P("Here you can download any file that's been uploaded to our collection. Select as many as you'd like, the one file you download will contain all entries from selected sets.", style={"padding":"2rem"}), justify="center", form=True),
        dbc.Row(dataPageTable, justify="center", form=True)
    ],
    className="pretty_container twelve columns",
)


def Data():
    layout =body
    return layout

