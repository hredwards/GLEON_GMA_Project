import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from app import app
from freshGraphs import tn_tp_scatter_all, choose2All, mapPlot, convert_to_json, overTimeAll, dfMasterData

app.config['suppress_callback_exceptions'] = True

body = html.Div(
    [
        dbc.Col([dbc.Row(html.H3("Welcome to the Global Microcystin Aggregation Project!", style={'textAlign':'center', 'float':'left'}),),
        dbc.Row(html.P(
                    """This is the homepage, this would have graphs and stuff; realistically
                    long term this needs to become Oldapp.py but for now we'll use this for testing"""),),
        dbc.Row(dbc.Button("Learn More About the Project", href="/PageAbout", color="secondary", size="lg"),),], className="pretty_container"),
        html.Div(
            [
                dbc.Col([mapPlot, tn_tp_scatter_all], className="six columns"),
                dbc.Col([overTimeAll, choose2All], className="five columns"),
            ], className="twelve columns"),
        html.Div(id='intermediate-value', style={'display': 'none'}, children=convert_to_json(dfMasterData)),
    ], className="twelve columns"
)




def Homepage():
    layout = body
    return layout

HomeLayout = html.Div([
        body
    ],
    style={
        "display": "flex",
        "flex-direction": "column"
    }
    )