import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
#from tempgraphs import tnTPPlotAll
from app import app
import data_analysis as da
from freshGraphs import tn_tp_scatter_all, choose2All

app.config['suppress_callback_exceptions'] = True

body = dbc.Container(
    [
        dbc.Row(
            [
                html.H3("Welcome to the Global Microcystin Aggregation Project!", style={'textAlign':'center', 'float':'left'}),
            ],
            #form=True
        ),
        dbc.Row(
                html.P(
                    """This is the homepage, this would have graphs and stuff; realistically
                    long term this needs to become Oldapp.py but for now we'll use this for testing"""
                ),
            justify="left"
        ),
        dbc.Row(
            dbc.Button("Learn More About the Project", href="/PageAbout", color="secondary", size="lg"),
        ),
        #tn_tp_scatter_all,
        #choose2All,

        html.Div([
            dbc.Row([
                tn_tp_scatter_all,
                choose2All
            ]),]),





       ],
#className="body mt-4",
)




def Homepage():
    layout = html.Div([body])
    return layout

HomeLayout = html.Div([
        body
    ],
    )