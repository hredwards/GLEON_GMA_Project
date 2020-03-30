import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from tempgraphs import tnTPPlot, tn_tp
from app import app
import data_analysis as da


app.config['suppress_callback_exceptions'] = True

body = dbc.Container(
    [
        dbc.Row(
            [
                html.H3("Welcome to the Global Microcystin Aggregation Project!", style={'textAlign':'center'}),
            ],
            form=True
        ),
        dbc.Row(
            [
                html.P(
                    """This is the homepage, this would have graphs and stuff; realistically
                    long term this needs to become Oldapp.py but for now we'll use this for testing"""
                ),
                dbc.Button("Learn More About the Project", href="/PageAbout", color="secondary", size="lg", className="mr-1", style={'textAlign':'center'}),
            ],
            justify="center", form=True
        ),
       dbc.Row(
           [

               dbc.Col(
                   [
                       tnTPPlot,
                   ]
               ),
              dbc.Col(
                 [
                     html.H2("Graph"),
                     dcc.Graph(
                         figure={"data": [{"x": [1, 2, 3], "y": [1, 4, 9]}]}
                            ),
                        ]
                     ),
                ]
            ),
        dbc.Row(
                html.P("This is a bunch of filler text"),
        )
       ],
className="body mt-4",
)

html.A(html.Button("About", id="aboutPage"),
       href="https://gleon.org/research/projects/global-microcystin-aggregation-gma", className="five columns"),





def Homepage():
    layout = html.Div([
        body
    ],
    )
    return layout

HomeLayout = html.Div([
        body
    ],
    )