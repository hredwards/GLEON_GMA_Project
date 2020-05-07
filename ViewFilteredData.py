import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
#from tempgraphs import tnTPPlotAll
from dash.dependencies import Input, Output, State
from app import app
import data_analysis as da
from freshGraphs import tn_tp_scatter_filter, choose2Filtered, mapPlot, convert_to_json
from s3References import dfMasterData
from controls import month_Controls, LAKES, lake_status_options, Substrate_Status, Substrate_Status_options, Sample_Types_options, Field_Methods_options, Microcystin_Method_options, data_Review_options

app.config['suppress_callback_exceptions'] = False
df = dfMasterData



filtersAvailable = html.Div(
                    [
                        html.P(
                            'Filter by reported date:',
                            className="control_label"
                        ),
                        dcc.RangeSlider(
                            id='filter-year-slider',
                            min=df['Year'].min(),
                            max=df['Year'].max(),
                            value=[df['Year'].min(), df['Year'].max()],
                            marks={str(year): str(year) for year in df['Year'].unique()},
                            step=None,
                            className="dcc_control"
                        ),
                        html.P(
                            'Filter by lake name:',
                            className="control_label"
                        ),
                        dcc.RadioItems(
                            id='lake_selector',
                            options=[
                                {'label': 'All ', 'value': 'all'},
                                {'label': 'Customize ', 'value': 'custom'}
                            ],
                            value='all',
                            labelStyle={"display": "inline-block",
                                        "margin-right": "1rem",
                                        "font-weight": "300"},
                            className="dcc_control"
                        ),
                        dcc.Dropdown(
                            id='lake_statuses',
                            options=lake_status_options,
                            multi=True,
                            value=list(LAKES.values()),
                            className="dcc_control",
                            style={'display': 'none'}
                        ),
                        html.P(
                            'Filter by substrate:',
                            className="control_label"
                        ),
                        dcc.RadioItems(
                            id='substrate_selector',
                            options=[
                                {'label': 'All ', 'value': 'all'},
                                {'label': 'Customize ', 'value': 'custom'}
                            ],
                            value='all',
                            labelStyle={"display": "inline-block",
                                        "margin-right": "1rem",
                                        "font-weight": "300"},
                            className="dcc_control"
                        ),
                        dcc.Dropdown(
                            id='substrate_types',
                            options=Substrate_Status_options,
                            multi=True,
                            value=list(Substrate_Status.keys()),
                            className="dcc_control",
                            style={'display': 'none'}
                        ),
                    ], className="pretty_container"
                )

@app.callback(
    Output('lake_statuses', 'style'),
    [Input('lake_selector', 'value')]
)
def show_full_lake_list(lake_selection):
    if lake_selection == 'custom':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    Output('substrate_types', 'style'),
    [Input('substrate_selector', 'value')]
)
def show_full_lake_list(substrate_selection):
    if substrate_selection == 'custom':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output('lake_statuses', 'value'),
              [Input('lake_selector', 'value')])
def display_type(selector):
    if selector == 'all':
        return list(LAKES.values())
    else:
        return []



summaryboxes = html.Div(
                    [
                                        html.P("No. of Lakes"),
                                        html.H6(
                                            id="lake_text",
                                            className="info_text"
                                        )
                                    ],
                                    id="lakes",
                                    className="pretty_container"
                                )

"""
summaryboxes = html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P("No. of Lakes"),
                                        html.H6(
                                            id="lake_text",
                                            className="info_text"
                                        )
                                    ],
                                    id="lakes",
                                    className="pretty_container"
                                ),

                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.P("No. of Datasets"),
                                                html.H6(
                                                    id="datasetText",
                                                    className="info_text"
                                                )
                                            ],
                                            id="datasetNum",
                                            className="pretty_container"
                                        ),
                                        html.Div(
                                            [
                                                html.P("No. of Datapoints"),
                                                html.H6(
                                                    id="dataPointsText",
                                                    className="info_text"
                                                )
                                            ],
                                            id="datapoints",
                                            className="pretty_container"
                                        ),
                                    ],
                                    id="tripleContainer",
                                )

                            ],
                            id="infoContainer",
                            className="row"
                        ),
                    ],
                    id="rightCol",
                    className="eight columns"
                )

"""










body = html.Div(
    [
        dbc.Row(
            [
                html.H3("Welcome to the Global Microcystin Aggregation Project!", style={'textAlign':'center', 'float':'left'}),
            ],
            #form=True
        ),
        dbc.Row(
                html.P(
                    """This page contains the same graphs as the homepage but can be filtered by various identifiers."""
                ),
            justify="left"
        ),
        #summaryboxes,
        #dbc.Col(filtersAvailable, className="pretty_container four columns"),

        html.Div(
            [
                dbc.Col([filtersAvailable, choose2Filtered], className="four columns"),
                dbc.Col([mapPlot, tn_tp_scatter_filter], className="pretty_container eight columns"),
            ], className="twelve columns"),
        html.Div(id='intermediate-value', style={'display': 'none'}, children=convert_to_json(df)),
    ], className="twelve columns",
)




def FilteredView():
    layout = body
    return layout
