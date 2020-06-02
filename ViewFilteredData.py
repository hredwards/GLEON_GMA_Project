import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
#from tempgraphs import tnTPPlotAll
from dash.dependencies import Input, Output, State
from app import app
import data_analysis as da
from freshGraphs import tn_tp_scatter_filter, choose2Filtered, mapPlotFiltered, convert_to_json, overTimeFiltered
from s3References import pullMasterdata, dfcsvOutline
from controls import month_Controls, LAKES, lake_status_options, Substrate_Status, Substrate_Status_options, \
    Sample_Types_options, Sample_Types, Field_Methods_options, Microcystin_Method, Microcystin_Method_options, data_Review_options,\
    Field_Methods, data_Review, institution_status_options, INSTITUTIONS, ynOptions, ynLabels

app.config['suppress_callback_exceptions'] = True
df = pullMasterdata()

dateFilters = html.Div([
    html.Details([
        html.Summary("Filter by Date"),
        html.Div(children=[
            html.H6(
                'Year',
                className="control_label"
            ),
            dcc.RangeSlider(
                id='filter-year-slider',
                min=df['Year'].min(),
                max=df['Year'].max(),
                value=[df['Year'].min(), df['Year'].max()],
                marks={
                    str(year): {'label': str(year), 'style': {'writing-mode': 'vertical-lr', 'text-orientation': 'upright'}}
                    for year in df['Year'].unique()
                },
                step=None,
                className="dcc_control_year"
            ),
            html.H6(
                'Month',
                className="control_label"
            ),
            dcc.RangeSlider(
                id='filter-month-slider',
                min=df['Month'].min(),
                max=df['Month'].max(),
                value=[df['Month'].min(), df['Month'].max()],
                marks={str(month): str(month) for month in df["Month"].unique()},
                step=None,
                className="dcc_control"
            ),
        ])
    ], open=True)

])


methodFilters = html.Div([
    html.Details([
        html.Summary("Filter by Methodology"),
        html.Div(children=[
            html.P(
                'Substrate:',
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


            html.P(
                'Microcystin Method:',
                className="control_label"
            ),
            dcc.RadioItems(
                id='microcystin_selector',
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
                id='microcystin_types',
                options=Microcystin_Method_options,
                multi=True,
                value=list(Microcystin_Method.keys()),
                className="dcc_control",
                style={'display': 'none'}
            ),


            html.P(
                'Sample Type:',
                className="control_label"
            ),
            dcc.RadioItems(
                id='sample_selector',
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
                id='sample_types',
                options=Sample_Types_options,
                multi=True,
                value=list(Sample_Types.keys()),
                className="dcc_control",
                style={'display': 'none'}
            ),

            html.P(
                'Field Method:',
                className="control_label"
            ),
            dcc.RadioItems(
                id='field_method_selector',
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
                id='field_method_types',
                options=Field_Methods_options,
                multi=True,
                value=list(Field_Methods.keys()),
                className="filter_box",
                style={'display': 'none', 'overflow':'show'}
            ),
            html.P(
                'Was Data Filtered?',
                className="control_label"
            ),
            dcc.RadioItems(
                id='filtered_selector',
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
                id='filt_options',
                options=ynOptions,
                multi=True,
                value=list(ynLabels.values()),
                className="dcc_control",
                style={'display': 'none'}
            ),
        ])
    ], open=True)

])

dataSourceFilters = html.Div([
    html.Details([
        html.Summary("Filter by Data Source"),
        html.Div(children=[
            html.P(
                'Institution:',
                className="control_label"
            ),
            dcc.RadioItems(
                id='institution_selector',
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
                id='institution_options',
                options=institution_status_options,
                multi=True,
                value=list(INSTITUTIONS.keys()),
                className="dcc_control",
                style={'display': 'none'}
            ),


            html.P(
                'Data Peer Reviewed or Published:',
                className="control_label"
            ),
            dcc.RadioItems(
                id='peer_review_selector',
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
                id='pr_options',
                options=ynOptions,
                multi=True,
                value=list(ynLabels.values()),
                className="dcc_control",
                style={'display': 'none'}
            ),

            html.P(
                'Field Method Reported:',
                className="control_label"
            ),
            dcc.RadioItems(
                id='field_reported_selector',
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
                id='fr_options',
                options=ynOptions,
                multi=True,
                value=list(ynLabels.values()),
                className="dcc_control",
                style={'display': 'none'}
            ),

            html.P(
                'Lab Method Reported:',
                className="control_label"
            ),
            dcc.RadioItems(
                id='lab_reported_selector',
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
                id='lm_options',
                options=ynOptions,
                multi=True,
                value=list(ynLabels.values()),
                className="dcc_control",
                style={'display': 'none'}
            ),

            html.P(
                'QA/QC Data available:',
                className="control_label"
            ),
            dcc.RadioItems(
                id='qa_qc_selector',
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
                id='qc_options',
                options=ynOptions,
                multi=True,
                value=list(ynLabels.values()),
                className="dcc_control",
                style={'display': 'none'}
            ),
        ])
    ], open=True)

])

lake_filter = html.Div([
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
])


filtersAvailable = html.Div(
                    [
                        dbc.Row(html.H6("Just select your filters below, and all graphs will update with the appropriate datasets."), justify="center", form=True, style={"text-align":"center"}),
                        lake_filter,
                        dateFilters,
                        methodFilters,
                        dataSourceFilters,
                    ], style={"margin":"1rem", "padding":"1rem"}, className="pretty_container"
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

@app.callback(Output('lake_statuses', 'value'),
              [Input('lake_selector', 'value')])
def display_type(selector):
    if selector == 'all':
        return list(LAKES.values())
    else:
        return []



@app.callback(
    Output('substrate_types', 'style'),
    [Input('substrate_selector', 'value')]
)
def show_full_lake_list(substrate_selection):
    if substrate_selection == 'custom':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output('substrate_types', 'value'),
              [Input('substrate_selector', 'value')])
def display_type(selector):
    if selector == 'all':
        return list(Substrate_Status.values())
    else:
        return []




@app.callback(
    Output('microcystin_types', 'style'),
    [Input('microcystin_selector', 'value')]
)
def show_full_lake_list(mc_selection):
    if mc_selection == 'custom':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output('microcystin_types', 'value'),
              [Input('substrate_selector', 'value')])
def display_type(selector):
    if selector == 'all':
        return list(Microcystin_Method.values())
    else:
        return []



@app.callback(
    Output('sample_types', 'style'),
    [Input('sample_selector', 'value')]
)
def show_sample_list(sample_selection):
    if sample_selection == 'custom':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output('sample_types', 'value'),
              [Input('sample_selector', 'value')])
def display_type(selector):
    if selector == 'all':
        return list(Sample_Types.values())
    else:
        return []





@app.callback(
    Output('field_method_types', 'style'),
    [Input('field_method_selector', 'value')]
)
def show_full_lake_list(field_selection):
    if field_selection == 'custom':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output('field_method_types', 'value'),
              [Input('field_method_selector', 'value')])
def display_type(selector):
    if selector == 'all':
        return list(Field_Methods.values())
    else:
        return []



@app.callback(
    Output('filt_options', 'style'),
    [Input('filtered_selector', 'value')]
)
def show_full_lake_list(field_selection):
    if field_selection == 'custom':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output('filt_options', 'value'),
              [Input('filtered_selector', 'value')])
def display_type(selector):
    if selector == 'all':
        return list(ynLabels.values())
    else:
        return []


@app.callback(
    Output('institution_options', 'style'),
    [Input('institution_selector', 'value')]
)
def show_full_list(field_selection):
    if field_selection == 'custom':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output('institution_options', 'value'),
              [Input('institution_selector', 'value')])
def display_type(selector):
    if selector == 'all':
        return list(INSTITUTIONS.keys())
    else:
        return []

@app.callback(
    Output('pr_options', 'style'),
    [Input('peer_review_selector', 'value')]
)
def show_full_list(field_selection):
    if field_selection == 'custom':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output('pr_options', 'value'),
              [Input('peer_review_selector', 'value')])
def display_type(selector):
    if selector == 'all':
        return list(ynLabels.keys())
    else:
        return []

@app.callback(
    Output('fr_options', 'style'),
    [Input('field_reported_selector', 'value')]
)
def show_full_list(field_selection):
    if field_selection == 'custom':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output('fr_options', 'value'),
              [Input('field_reported_selector', 'value')])
def display_type(selector):
    if selector == 'all':
        return list(ynLabels.keys())
    else:
        return []

@app.callback(
    Output('lm_options', 'style'),
    [Input('lab_reported_selector', 'value')]
)
def show_full_list(field_selection):
    if field_selection == 'custom':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output('lm_options', 'value'),
              [Input('lab_reported_selector', 'value')])
def display_type(selector):
    if selector == 'all':
        return list(ynLabels.keys())
    else:
        return []

@app.callback(
    Output('qc_options', 'style'),
    [Input('qa_qc_selector', 'value')]
)
def show_full_list(field_selection):
    if field_selection == 'custom':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output('qc_options', 'value'),
              [Input('qa_qc_selector', 'value')])
def display_type(selector):
    if selector == 'all':
        return list(ynLabels.keys())
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
        #summaryboxes,
        html.Div(
            [
                dbc.Col([filtersAvailable], className="three columns"),
                dbc.Col([mapPlotFiltered], className="five columns"),
                dbc.Col([tn_tp_scatter_filter], className="four columns"),
                dbc.Col([overTimeFiltered], className="five columns"),
                dbc.Col([choose2Filtered], className="four columns"),

            ], className="twelve columns"),

        html.Div(id='intermediate-value', style={'display': 'none'}, children=convert_to_json(df)),
    ], id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    },
    className="twelve columns",
)


def FilteredView():
    layout = body
    return layout
