import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from app import app
import numpy as np
from OldCode.settings import USEPA_LIMIT, WHO_LIMIT
import plotly.graph_objs as go
from s3References import dfMasterData, dfMetadataDB, dfcsvOutline, pullMasterdata, pullMetaDB

app.config['suppress_callback_exceptions'] = True

"""
Dataframe calling/definition; calls for masterdata.csv from S3 bucket
"""
#df = dfMasterData
#df['Year'] = pd.DatetimeIndex(df['DATETIME']).year
#df['Month'] = pd.DatetimeIndex(df['DATETIME']).month
#df['Date Reported'] = pd.to_datetime(df['DATETIME'])

df = pullMasterdata()

dfMeta = dfMetadataDB
allColumnNames = list(dfMasterData.columns.values)


dfcsvOutline['Year'] = pd.DatetimeIndex(dfcsvOutline['DATETIME']).year
dfcsvOutline['Date Reported'] = pd.to_datetime(dfcsvOutline['DATETIME'])



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
Total Phosphorus vs Total Nitrogen (Unfiltered, all data)
"""
# This is the HTML output, it calls the graph with the id tn_tp_scatter which is pulled in an app callback
# The app callback just runs the tn_tp_all definition and outputs the returned figure as a graph figure here
# This definition is pulled in homepage.py to print the output on the homepage

tn_tp_scatter_all = html.Div([dcc.Graph(id="tn_tp_scatter")], className="pretty_container graph")

# App callback for unfiltered tn/tp scatter plot.
@app.callback(
    Output('tn_tp_scatter', 'figure'),
    [Input('intermediate-value', 'children')]
)
def update_output(jsonified_data):
    current_df = df
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
    tnTPAllScatter = go.Figure(data=data, layout=layout)
    return tnTPAllScatter



""" 
Choose 2 variables to compare (all data, unfiltered)
"""
available_indicators = allColumnNames

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




@app.callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    [Input('choose-2-scale-homepage', 'value'),
     Input('crossfilter-xaxis-column', 'value'),
     Input('crossfilter-yaxis-column', 'value'),
     Input('intermediate-value', 'children')])
def update_graph(selected_option, xaxis_column_name, yaxis_column_name, jsonified_data):
    dff = df
    dff = dff[dff[yaxis_column_name].notnull()
              & dff[yaxis_column_name]>0]

    dff = dff[dff[xaxis_column_name].notnull()
              & dff[xaxis_column_name]>0]

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
        'x': 0.5,},
        xaxis=dict(
            title=xaxis_column_name,
        ),

        yaxis=dict(
            title=yaxis_column_name,
    ),
        hovermode='closest',
    )
    allChoose2 = go.Figure(data=data, layout=layout)
    return allChoose2





"""
Mapbox Plot -- Microcystin Concentration Geographically; all data (unfiltered)
"""
mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'

mapLayout = dict(
    #autosize=True,
    automargin=True,
    margin=dict(
        l=30,
        r=30,
        b=20,
        t=40,
    ),
    hovermode="closest",
    #plot_bgcolor="#F9F9F9",
    #paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation='h'),
    title='Microcystin Concentration',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(
            lon=-30,
            lat=37.772537
        ),
        zoom = 1.5,
        layers = [
        {
            "below": 'traces',
            #"sourcetype": "raster",
            #"source": [
             #   "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            #]
        }
    ]
    ),
)

@app.callback(
    Output('map_MCConc', 'figure'),
    [Input('intermediate-value', 'children')])
def update_output(jsonified_data):
    selected_data = df
    data = []
    opacity_level = 0.8
    MC_conc = selected_data['Microcystin (ug/L)']
    # make bins
    b1 = selected_data[MC_conc <= USEPA_LIMIT]
    b2 = selected_data[(MC_conc > USEPA_LIMIT) & (MC_conc <= WHO_LIMIT)]
    b3 = selected_data[MC_conc > WHO_LIMIT]
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
    fig = dict(data=data, layout=mapLayout)
    return fig


mapPlot = html.Div([dcc.Graph(id="map_MCConc")], className="pretty_container graph")



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



@app.callback(
    Output('over-time-indicator-scatter', 'figure'),
    [Input('over-time-scale-homepage', 'value'),
     Input('over-time-yaxis-column', 'value'),
     Input('intermediate-value', 'children')])
def update_graph(selected_option, yaxis_column_name, jsonified_data):
    dff = df
    dff = dff[dff[yaxis_column_name].notnull()
              & dff[yaxis_column_name]>0]

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
        'x': 0.5,},
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



















"""""""""""


THIS SECTION BEGINS THE GRAPHS FOR FILTERED FILTERED DATA



"""


"""
Total Phosphorus vs Total Nitrogen (filtered data)
"""


# This is the HTML output, it calls the graph with the id tn_tp_scatter which is pulled in an app callback
# The app callback just runs the tn_tp_all definition and outputs the returned figure as a graph figure here
# This definition is pulled in homepage.py to print the output on the homepage

def filter_dataframe(df, lake_name, year_slider, month_value, substrate, microcystin_types, sample, field, filtered, institution, peerRev, fieldRep, labRep, QA):
    lake_name = list(lake_name)
    substrate = list(substrate)
    microcystin_types = list(microcystin_types)
    sample = list(sample)
    field = list(field)
    filtered = list(filtered)
    institution = list(institution)
    peerRev = list(peerRev)
    fieldRep = list(fieldRep)
    labRep = list(labRep)
    QA = list(QA)


# If any filter options are empty, return an empty dataframe. This is necessary bc without it, it returns key errors or doesn't remove the very last thing user says to remove
    if not lake_name or not substrate or not microcystin_types or not sample or not field or not filtered or not institution or not peerRev or not fieldRep or not labRep or not QA:
        dff= dfcsvOutline


    else:
        yearRange = list(range(year_slider[0], year_slider[1] + 1, 1))
        monthRange = list(range(month_value[0], month_value[1] + 1, 1))

        dfMeta = pullMetaDB()


        dffMeta = dfMeta[dfMeta['Microcystin_method'].isin(microcystin_types)
                 & (dfMeta['Field_method'].isin(field))
                 & (dfMeta['Field_method_YN'].isin(fieldRep))
                 & (dfMeta['Substrate'].isin(substrate))
                 & (dfMeta['Sample_Type'].isin(sample))
                 & (dfMeta['Filter_YN'].isin(filtered))
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







tn_tp_scatter_filter = html.Div([dcc.Graph(id="tn_tp_filter_scatter")], className="pretty_container graph")


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
def return_filtered_TNTP_figure(jsonified_data, lake_statuses, year_value, month_value, substrate, microcystin_types, sample, field, filtered, institution, peerRev, fieldRep, labRep, QA):
    current_df = filter_dataframe(df, lake_statuses, year_value, month_value, substrate, microcystin_types, sample, field, filtered, institution, peerRev, fieldRep, labRep, QA)
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
    tnTPAllFilteredScatter = go.Figure(data=data, layout=layout)
    return tnTPAllFilteredScatter


@app.callback(Output('lake_text', 'children'),
              [Input('lake_statuses', 'value'),
               Input('year_slider', 'value')])
def update_well_text(well_statuses, year_slider):
    dff = filter_dataframe(df, well_statuses, year_slider)
    return dff['Body of Water Name'].nunique()






# Any Y over time filtered graph

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
def update_graph(selected_option, yaxis_column_name, jsonified_data, lake_statuses, year_value, month_value, substrate, microcystin_types, sample, field, filtered, institution, peerRev, fieldRep, labRep, QA):
    dff = filter_dataframe(df, lake_statuses, year_value, month_value, substrate, microcystin_types, sample, field, filtered, institution, peerRev, fieldRep, labRep, QA)
    dff = dff[dff[yaxis_column_name].notnull()
              & dff[yaxis_column_name]>0]

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
        'x': 0.5,},
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









# Any X/Y filtered graph

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


# Any Y over time filtered graph
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
def update_graph(selected_option, xaxis_column_name, yaxis_column_name, jsonified_data, lake_statuses, year_value, month_value, substrate, microcystin_types, sample, field, filtered, institution, peerRev, fieldRep, labRep, QA):
    dff = filter_dataframe(df, lake_statuses, year_value, month_value, substrate, microcystin_types, sample, field, filtered, institution, peerRev, fieldRep, labRep, QA)
    dff = dff[dff[yaxis_column_name].notnull()
              & dff[yaxis_column_name]>0]

    dff = dff[dff[xaxis_column_name].notnull()
              & dff[xaxis_column_name]>0]

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
        'x': 0.5,},
        xaxis=dict(
            title=xaxis_column_name,
        ),

        yaxis=dict(
            title=yaxis_column_name,
    ),
        hovermode='closest'
    )
    filteredChoose2 = go.Figure(data=data, layout=layout)
    return filteredChoose2



# Map plot filtered data

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
def update_graph(jsonified_data, lake_statuses, year_value, month_value, substrate, microcystin_types, sample, field, filtered, institution, peerRev, fieldRep, labRep, QA):
    selected_data = filter_dataframe(df, lake_statuses, year_value, month_value, substrate, microcystin_types, sample, field, filtered, institution, peerRev, fieldRep, labRep, QA)
    data = []
    opacity_level = 0.8
    MC_conc = selected_data['Microcystin (ug/L)']
    # make bins
    b1 = selected_data[MC_conc <= USEPA_LIMIT]
    b2 = selected_data[(MC_conc > USEPA_LIMIT) & (MC_conc <= WHO_LIMIT)]
    b3 = selected_data[MC_conc > WHO_LIMIT]
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
    fig = dict(data=data, layout=mapLayout)
    return fig


mapPlotFiltered = html.Div([dcc.Graph(id="map_MCConc_Filtered")], className="pretty_container graph")
