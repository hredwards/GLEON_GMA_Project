from s3References import dfMasterData, dfexampleSheet, dfcsvOutline, pullMasterdata, pullMetaDB
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from app import app
import numpy as np
import plotly.graph_objs as go

app.config['suppress_callback_exceptions'] = True

df = pullMasterdata()

dfMeta = pullMetaDB()
allColumnNames = list(df.columns.values)


dfcsvOutline['Year'] = pd.DatetimeIndex(dfcsvOutline['DATETIME']).year
dfcsvOutline['Date Reported'] = pd.to_datetime(dfcsvOutline['DATETIME'])

"""
Setting filters
"""
# Establish range of months and years that exist in data
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Established microcystin limits
USEPA_LIMIT = 4
WHO_LIMIT = 20

"""
Definitions used to convert dataframe to json list and back (used in callbacks and definitions)
"""

def convert_to_json(current_dataframe):
    # This converts the dataframe to a json file. This is necesary for app callbacks because they can't use a dataframe
    # as an input, only lists/tuples like a json str
    jsonStr = current_dataframe.to_json(orient='split')
    return jsonStr


def convert_to_df(jsonified_data):
    # This takes jsond data and turns it back into a dataframe; needed for definitions called inside of app callbacks
    jsonStr = r'{}'.format(jsonified_data)
    dff = pd.read_json(jsonStr, orient='split')
    return dff


"""
Definition to filter dataset
"""
def filter_dataframe(df, lake_name, year_slider, month, substrate, microcystin_types, sample, field, filter, institution, peerRev, fieldRep, labRep, QA):
    if type(lake_name) is not list:
        lake_name = [lake_name]

    if type(substrate) is not list:
        substrate = [substrate]

    if type(microcystin_types) is not list:
        microcystin_types = [microcystin_types]

    if type(sample) is not list:
        sample = [sample]

    if type(field) is not list:
        field = [field]

    if type(filter) is not list:
        filter = [filter]

    if type(institution) is not list:
        institution = [institution]

    if type(peerRev) is not list:
        peerRev = [peerRev]

    if type(fieldRep) is not list:
        fieldRep = [fieldRep]

    if type(labRep) is not list:
        labRep = [labRep]

    if type(QA) is not list:
        QA = [QA]

# If any filter options are empty, return an empty dataframe. This is necessary bc without it, it returns key errors or doesn't remove the very last thing user says to remove
    if not microcystin_types or not lake_name or not institution:
        dff= dfcsvOutline

    else:
        yearRange = list(range(year_slider[0], year_slider[1] + 1, 1))
        monthRange = list(range(month[0], month[1] + 1, 1))


        dffMeta = dfMeta[dfMeta['Microcystin_method'].isin(microcystin_types)
                 & (dfMeta['Field_method'].isin(field))
                 & (dfMeta['Field_method_YN'].isin(fieldRep))
                 & (dfMeta['Substrate'].isin(substrate))
                 & (dfMeta['Sample_Type'].isin(sample))
                 & (dfMeta['Filter_YN'].isin(filter))
                 & (dfMeta['Lab_method'].isin(labRep))
                 & (dfMeta['Published'].isin(peerRev))
                 & (dfMeta['QA_QC'].isin(QA))
                 & (dfMeta['Institution'].isin(institution))
        ]

        if dffMeta.empty:
            dff = dfcsvOutline
        else:

            dffMeta = list(dffMeta.apply(set)[0])
            dffMeta = sorted(dffMeta)

            dff = df[df['Body of Water Name'].isin(lake_name)
                     & (df['Year'].isin(yearRange))
                     & (df['Month'].isin(monthRange))
                     & (df['RefID'].isin(dffMeta))
                     ]

    return dff




"""
Total Phosphorus vs Total Nitrogen
"""

def tn_tp(desiredData):
    current_df = desiredData
    # Find MC concentration to compare to WHO/USEPA limits; filter into bins accordingly
    MC_conc = current_df['Microcystin (ug/L)']

    b1 = current_df[MC_conc <= USEPA_LIMIT]
    b2 = current_df[(MC_conc > USEPA_LIMIT) & (MC_conc <= WHO_LIMIT)]
    b3 = current_df[MC_conc > WHO_LIMIT]

    # define the data of the graph. there's 3 scatter plots here, one for each bin defined above
    # This returns the values in log(10) for now. Might change to a log slider down the line
    data = [go.Scatter(
        x=np.log10(b1.loc[:, 'Total Nitrogen (ug/L)']),
        y=np.log10(b1.loc[:, 'Total Phosphorus (ug/L)']),
        mode='markers',
        name="<USEPA",
        text=b1.loc[:, 'Body of Water Name'],
        marker=dict(
            size=8,
            color="green",
        )),
        go.Scatter(
            x=np.log10(b2.loc[:, 'Total Nitrogen (ug/L)']),
            y=np.log10(b2.loc[:, 'Total Phosphorus (ug/L)']),
            mode='markers',
            name=">USEPA",
            text=b2.loc[:, 'Body of Water Name'],
            marker=dict(
                size=8,
                color="orange",
            )),
        go.Scatter(
            x=np.log10(b3.loc[:, 'Total Nitrogen (ug/L)']),
            y=np.log10(b3.loc[:, 'Total Phosphorus (ug/L)']),
            mode='markers',
            name=">WHO",
            text=b3.loc[:, 'Body of Water Name'],
            marker=dict(
                size=8,
                color="red",
            )),
    ]
    # Defines layout of graph, axis names, and legend
    layout = go.Layout(
        legend=dict(font=dict(size=10), orientation='h'),
        title='Total Nitrogen vs Total Phosphorus',
        title_x=0.5,
        xaxis=dict(
            title='log TN'),
        yaxis=dict(
            title="log TP"),
        hovermode='closest'
    )
    # defines resulting GO figure and returns it from this definition
    tnTpScatter = go.Figure(data=data, layout=layout)
    return tnTpScatter

@app.callback(
    Output('tn_tp_scatter', 'figure'),
    [Input('intermediate-value', 'children')]
)
def update_output(jsonified_data):
    desiredData = pullMasterdata()
    return tn_tp(desiredData)

@app.callback(Output('tn_tp_filter_scatter', 'figure'),
              [Input('intermediate-value', 'children'),
               Input('lake_statuses', 'value'),
               Input('filter-year-slider', 'value'),
               Input('filter-month-slider', 'value'),
               Input('substrate_types', 'value'),
               Input('microcystin_types', 'value'),
               Input('sample_types', 'value'),
               Input('field_method_types', 'value'),
               Input('filt_options', 'value'),
               Input('institution_options', 'value'),
               Input('pr_options', 'value'),
               Input('fr_options', 'value'),
               Input('lm_options', 'value'),
               Input('qc_options', 'value')])
def make_filtered_TNTP_figure(jsonified_data, lake_statuses, year_value, month_value, substrate, microcystin_types, sample, field, filter, institution, peerRev, fieldRep, labRep, QA):
    current_df = filter_dataframe(df, lake_statuses, year_value, month_value, substrate, microcystin_types, sample, field, filter, institution, peerRev, fieldRep, labRep, QA)
    return tn_tp(current_df)


tn_tp_scatter_all = html.Div([dcc.Graph(id="tn_tp_scatter")], className="pretty_container graph")
tn_tp_scatter_filter = html.Div([dcc.Graph(id="tn_tp_filter_scatter")], className="pretty_container graph")



"""
Choose 2 variables to compare
"""

available_indicators = allColumnNames

def choose2(selected_option, xaxis_column_name, yaxis_column_name, desiredData):
    dff = desiredData
    dff = dff[dff[yaxis_column_name].notnull()
              & dff[yaxis_column_name] > 0]

    dff = dff[dff[xaxis_column_name].notnull()
              & dff[xaxis_column_name] > 0]

    if selected_option == '3SD':
        dff = dff[((dff[yaxis_column_name] - dff[yaxis_column_name].mean()) / dff[yaxis_column_name].std()).abs() < 3]
        dff = dff[((dff[xaxis_column_name] - dff[xaxis_column_name].mean()) / dff[xaxis_column_name].std()).abs() < 3]

    if selected_option == 'LOG':
        dff[yaxis_column_name] = np.log10(dff[yaxis_column_name])
        dff[xaxis_column_name] = np.log10(dff[xaxis_column_name])

    data = [
        go.Scatter(
            x=dff[xaxis_column_name],
            y=dff[yaxis_column_name],
            mode='markers',
            text=dff['Body of Water Name'],
            marker=dict(
                size=8,
            )
        ),
    ]

    layout = go.Layout(
        title={
            'text': xaxis_column_name + ' vs ' + yaxis_column_name,
            'x': 0.5, },
        xaxis=dict(
            title=xaxis_column_name,
        ),

        yaxis=dict(
            title=yaxis_column_name,
        ),
        hovermode='closest',
    )
    choose2Graph = go.Figure(data=data, layout=layout)
    return choose2Graph


@app.callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    [Input('choose-2-scale-homepage', 'value'),
     Input('crossfilter-xaxis-column', 'value'),
     Input('crossfilter-yaxis-column', 'value'),
     Input('intermediate-value', 'children')])
def update_graph(selected_option, xaxis_column_name, yaxis_column_name, jsonified_data):
    desiredData = pullMasterdata()
    return choose2(selected_option, xaxis_column_name, yaxis_column_name, desiredData)

@app.callback(
    Output('filtered-crossfilter-indicator-scatter', 'figure'),
    [Input('choose-2-scale', 'value'),
     Input('filtered-crossfilter-xaxis-column', 'value'),
     Input('filtered-crossfilter-yaxis-column', 'value'),
     Input('intermediate-value', 'children'),
     Input('lake_statuses', 'value'),
     Input('filter-year-slider', 'value'),
     Input('filter-month-slider', 'value'),
     Input('substrate_types', 'value'),
     Input('microcystin_types', 'value'),
     Input('sample_types', 'value'),
     Input('field_method_types', 'value'),
     Input('filt_options', 'value'),
     Input('institution_options', 'value'),
     Input('pr_options', 'value'),
     Input('fr_options', 'value'),
     Input('lm_options', 'value'),
     Input('qc_options', 'value')])
def update_graph(selected_option, xaxis_column_name, yaxis_column_name, jsonified_data, lake_statuses, year_value, month_value, substrate, microcystin_types, sample, field, filter, institution, peerRev, fieldRep, labRep, QA):
    filteredData = filter_dataframe(df, lake_statuses, year_value, month_value, substrate, microcystin_types, sample, field, filter, institution, peerRev, fieldRep, labRep, QA)
    return choose2(selected_option, xaxis_column_name, yaxis_column_name, filteredData)

choose2All= html.Div([
    dcc.Graph(id='crossfilter-indicator-scatter'),
    dbc.Row(
        dcc.RadioItems(
            id="choose-2-scale-homepage",
            options=[{'label': 'Show All Raw Data', 'value': 'RAW'},
                     {'label': 'Apply Log10 to Raw Data', 'value': 'LOG'},
                     {'label': 'Show Data Within 3 Standard Deviations', 'value': '3SD'}],
            value='RAW',
            labelStyle={"display": "inline-block",
                        "margin-bottom": "1rem",
                        "margin-right": "2rem",
                        "font-weight": "300"},
        ), form=True, justify="center",
    ),
    dbc.Row([
        dbc.Col([
            html.H6("Choose an X variable:"),
            dcc.Dropdown(
        id='crossfilter-xaxis-column',
        options=[{'label': i, 'value': i} for i in available_indicators],
        value='Microcystin (ug/L)',
            )], style={"text-align":"center"}, className="six columns"),

        dbc.Col([
            html.H6("Choose a Y variable:"),

            dcc.Dropdown(
            id='crossfilter-yaxis-column',
            options=[{'label': i, 'value': i} for i in available_indicators],
            value='Secchi Depth (m)',

        )],  style={"text-align":"center"}, className="six columns")]),
],  className="pretty_container graph")

choose2Filtered= html.Div([
    dcc.Graph(id='filtered-crossfilter-indicator-scatter'),
    dbc.Row(
        dcc.RadioItems(
            id="choose-2-scale",
            options=[{'label': 'Show All Raw Data', 'value': 'RAW'},
                     {'label': 'Apply Log10 to Raw Data', 'value': 'LOG'},
                     {'label': 'Show Data Within 3 Standard Deviations', 'value': '3SD'}],
            value='RAW',
            labelStyle={"display": "inline-block",
                        "margin-bottom": "1rem",
                        "margin-right": "2rem",
                        "font-weight": "300"},
        ), form=True, justify="center",
    ),
    dbc.Row([
        dbc.Col([
            html.H6("Choose an X variable:"),
            dcc.Dropdown(
                id='filtered-crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Microcystin (ug/L)',
            )],  style={"text-align": "center"}, className="six columns"),

        dbc.Col([
            html.H6("Choose a Y variable:"),

            dcc.Dropdown(
                id='filtered-crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Secchi Depth (m)',

            )], style={"text-align": "center"}, className="six columns")]),

], className="pretty_container graph")



"""
Map Plot
"""

def matPlot(desiredData):
    df = desiredData
    data = []
    opacity_level = 0.8
    MC_conc = df['Microcystin (ug/L)']
    # make bins
    b1 = df[MC_conc <= USEPA_LIMIT]
    b2 = df[(MC_conc > USEPA_LIMIT) & (MC_conc <= WHO_LIMIT)]
    b3 = df[MC_conc > WHO_LIMIT]
    data.append(go.Scattermapbox(
        lon=b1['LONG'],
        lat=b1['LAT'],
        mode='markers',
        text=b1["Body of Water Name"],
        visible=True,
        name="MC <= USEPA Limit",
        marker=dict(color="green", opacity=opacity_level)))
    data.append(go.Scattermapbox(
        lon=b2['LONG'],
        lat=b2['LAT'],
        mode='markers',
        text=b2["Body of Water Name"],
        visible=True,
        name="MC <= WHO Limit",
        marker=dict(color="orange", opacity=opacity_level)))
    data.append(go.Scattermapbox(
        lon=b3['LONG'],
        lat=b3['LAT'],
        mode='markers',
        text=b3["Body of Water Name"],
        visible=True,
        name="MC > WHO Limit",
        marker=dict(color="red", opacity=opacity_level)))
    fig = dict(data=data, layout=layout)
    return fig

@app.callback(
    Output('map_MCConc', 'figure'),
    [Input('intermediate-value', 'children')]
)
def update_output(jsonified_data):
    desiredData = pullMasterdata()
    return mapPlot(desiredData)



@app.callback(
    Output('map_MCConc_Filtered', 'figure'),
    [Input('intermediate-value', 'children'),
     Input('lake_statuses', 'value'),
     Input('filter-year-slider', 'value'),
     Input('filter-month-slider', 'value'),
     Input('substrate_types', 'value'),
     Input('microcystin_types', 'value'),
     Input('sample_types', 'value'),
     Input('field_method_types', 'value'),
     Input('filt_options', 'value'),
     Input('institution_options', 'value'),
     Input('pr_options', 'value'),
     Input('fr_options', 'value'),
     Input('lm_options', 'value'),
     Input('qc_options', 'value')])
def update_graph(jsonified_data, lake_statuses, year_value, month_value, substrate, microcystin_types, sample, field, filter, institution, peerRev, fieldRep, labRep, QA):
    fiteredData = filter_dataframe(df, lake_statuses, year_value, month_value, substrate, microcystin_types, sample, field, filter, institution, peerRev, fieldRep, labRep, QA)
    return matPlot(fiteredData)



mapPlotAll = html.Div([dcc.Graph(id="map_MCConc")], className="pretty_container graph")
mapPlotFiltered = html.Div([dcc.Graph(id="map_MCConc_Filtered")], className="pretty_container graph")






"""
Over Time
"""

overTimeAll= html.Div([
    dcc.Graph(id='over-time-indicator-scatter'),
    dbc.Row(
        dcc.RadioItems(
            id="over-time-scale-homepage",
            options=[{'label': 'Show All Raw Data', 'value': 'RAW'},
                     {'label': 'Apply Log10 to Raw Data', 'value': 'LOG'},
                     {'label': 'Show Data Within 3 Standard Deviations', 'value': '3SD'}],
            value='RAW',
            labelStyle={"display": "inline-block",
                        "margin-bottom": "1rem",
                        "margin-right": "2rem",
                        "font-weight": "300"},
        ), form=True, justify="center",
    ),
    dbc.Row([
        dbc.Col([
            html.H6("Choose a Y variable:"),

            dcc.Dropdown(
                id='over-time-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Microcystin (ug/L)',

            )], style={"text-align": "center"}, className="six columns")]),
],className="pretty_container graph")

overTimeFiltered= html.Div([
    dcc.Graph(id='filtered-over-time-indicator-scatter'),
    dbc.Row(
        dcc.RadioItems(
            id="over-time-scale",
            options=[{'label': 'Show All Raw Data', 'value': 'RAW'},
                     {'label': 'Apply Log10 to Raw Data', 'value': 'LOG'},
                     {'label': 'Show Data Within 3 Standard Deviations', 'value': '3SD'}],
            value='RAW',
            labelStyle={"display": "inline-block",
                        "margin-bottom": "1rem",
                        "margin-right": "2rem",
                        "font-weight": "300"},
        ), form=True, justify="center",
    ),
    dbc.Row([
        dbc.Col([
            html.H6("Choose a Y variable:"),

            dcc.Dropdown(
                id='filtered-over-time-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Microcystin (ug/L)',

            )], style={"text-align": "center"}, className="six columns")]),
], className="pretty_container graph")


def overTime(selected_option, yaxis_column_name, desiredData):
    dff = desiredData
    dff = dff[dff[yaxis_column_name].notnull()
              & dff[yaxis_column_name] > 0]

    if selected_option == '3SD':
        dff = dff[((dff[yaxis_column_name] - dff[yaxis_column_name].mean()) / dff[yaxis_column_name].std()).abs() < 3]

    if selected_option == 'LOG':
        dff[yaxis_column_name] = np.log10(dff[yaxis_column_name])

    data = [
        go.Scatter(
            x=dff["Year"],
            y=dff[yaxis_column_name],
            mode='markers',
            text=dff['Body of Water Name'],
            marker=dict(
                size=8,
            )
        ),
    ]

    layout = go.Layout(
        title={
            'text': yaxis_column_name + ' Over Time',
            'x': 0.5, },
        xaxis=dict(
            title="Date",
            dtick=1,
        ),

        yaxis=dict(
            title=yaxis_column_name,
        ),
        hovermode='closest'
    )
    com2 = go.Figure(data=data, layout=layout)
    return com2


@app.callback(
    Output('over-time-indicator-scatter', 'figure'),
    [Input('over-time-scale-homepage', 'value'),
     Input('over-time-yaxis-column', 'value'),
     Input('intermediate-value', 'children')])
def update_graph(selected_option, yaxis_column_name, jsonified_data):
    desiredData = pullMasterdata()
    overTime(selected_option, yaxis_column_name, desiredData)

@app.callback(
    Output('filtered-over-time-indicator-scatter', 'figure'),
    [Input('over-time-scale', 'value'),
     Input('filtered-over-time-yaxis-column', 'value'),
     Input('intermediate-value', 'children'),
     Input('lake_statuses', 'value'),
     Input('filter-year-slider', 'value'),
     Input('filter-month-slider', 'value'),
     Input('substrate_types', 'value'),
     Input('microcystin_types', 'value'),
     Input('sample_types', 'value'),
     Input('field_method_types', 'value'),
     Input('filt_options', 'value'),
     Input('institution_options', 'value'),
     Input('pr_options', 'value'),
     Input('fr_options', 'value'),
     Input('lm_options', 'value'),
     Input('qc_options', 'value')])
def update_graph(selected_option, yaxis_column_name, jsonified_data, lake_statuses, year_value, month_value, substrate, microcystin_types, sample, field, filter, institution, peerRev, fieldRep, labRep, QA):
    filteredData = filter_dataframe(df, lake_statuses, year_value, month_value, substrate, microcystin_types, sample, field, filter, institution, peerRev, fieldRep, labRep, QA)
    return overTime(selected_option, yaxis_column_name, filteredData)
