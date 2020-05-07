import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import datetime as dt
from dash.dependencies import Input, Output
from app import app
import numpy as np
from settings import months, USEPA_LIMIT, WHO_LIMIT
import plotly.graph_objs as go
import plotly.express as px
from s3References import dfMasterData


app.config['suppress_callback_exceptions'] = True

"""
Dataframe calling/definition; calls for masterdata.csv from S3 bucket
"""
df = dfMasterData

allColumnNames = list(df.columns.values)
df['Year'] = pd.DatetimeIndex(df['DATETIME']).year
df['Date Reported'] = pd.to_datetime(df['DATETIME'])



"""
Definitions used to convert dataframe to json list and back (used in callbacks and definitions)
"""

def convert_to_json(current_dataframe):
    # This converts the dataframe to a json file. This is necessary for app callbacks because they can't use a dataframe
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

# This definition makes the actual graph
def tn_tp_all(current_df):
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
        showlegend=True,
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


# This is the HTML output, it calls the graph with the id tn_tp_scatter which is pulled in an app callback
# The app callback just runs the tn_tp_all definition and outputs the returned figure as a graph figure here
# This definition is pulled in homepage.py to print the output on the homepage

tn_tp_scatter_all = dcc.Graph(id="tn_tp_scatter")

# App callback for unfiltered tn/tp scatter plot.
@app.callback(
    Output('tn_tp_scatter', 'figure'),
    [Input('intermediate-value', 'children')]
)
def update_output(jsonified_data):
    dff = convert_to_df(jsonified_data)
    return tn_tp_all(dff)



""" 
Choose 2 variables to compare (all data, unfiltered)
"""
available_indicators = allColumnNames



choose2All= html.Div([
        dcc.Graph(id='crossfilter-indicator-scatter'),
    html.Div([
        dcc.RangeSlider(
            id='crossfilter-year--slider',
            min=df['Year'].min(),
            max=df['Year'].max(),
            value=[df['Year'].min(), df['Year'].max()],
            marks={str(year): str(year) for year in df['Year'].unique()},
            step=None
        ),
            dcc.Dropdown(
                    id='crossfilter-xaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Alloxanthin (ug/L)',
                className="eight columns",
                ),
        dcc.RadioItems(
            id='crossfilter-xaxis-type',
            options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            value='Linear',
            style={"display": "block", "margin-left": "1rem", "padding-left": "1rem"},
            className="three columns",
        ),
        dcc.Dropdown(
            id='crossfilter-yaxis-column',
            options=[{'label': i, 'value': i} for i in available_indicators],
            value='Cytotoxin Cylindrospermopsin (ug/L)',
            className="eight columns",
        ),
        dcc.RadioItems(
            id='crossfilter-yaxis-type',
            options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            value='Linear',
            style={"display": "block", "margin-left": "1rem", "padding-left": "1rem"},
            className="three columns",
        ),
    ],)
    ],)


def comp2Graph(dataframe, xaxis_column_name, yaxis_column_name, yearRange):
    data = [
        go.Scatter(
        x=dataframe.loc[:, xaxis_column_name],
        y=dataframe.loc[:, yaxis_column_name],
        mode='markers',
        text=dataframe.loc[:, 'Body of Water Name'],
        marker=dict(
            size=8,
        )
    ),
    ]

    layout = go.Layout(
        title='Raw Data Comparison of any X/Y',
        title_x=0.5,
        xaxis=dict(
            title=xaxis_column_name),
        yaxis=dict(
            title=yaxis_column_name),
        hovermode='closest'
    )
    com2 = go.Figure(data=data, layout=layout)
    return com2


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):
    if type(year_value) is not list:
        year_value = [year_value]

    yearRange = list(range(year_value[0], year_value[1]+1, 1))


    selected_data = df[(df['Year'].isin(yearRange))]

    #dff = df[df['Year'] == year_value]
    return comp2Graph(selected_data, xaxis_column_name, yaxis_column_name, yearRange)



"""
Mapbox Plot -- Microcystin Concentration Geographically; all data (unfiltered)
"""
mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'

layout = dict(
    autosize=True,
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



def geo_concentration_plot(selected_data):
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
    fig=dict(data = data, layout= layout)
    return fig



@app.callback(
    Output('map_MCConc', 'figure'),
    [Input('intermediate-value', 'children')]
)
def update_output(jsonified_data):
    dff = convert_to_df(jsonified_data)
    return geo_concentration_plot(dff)

mapPlot = dcc.Graph(id='map_MCConc')


"""""""""""


THIS SECTION BEGINS THE GRAPHS FOR FILTERED FILTERED DATA



"""


"""
Total Phosphorus vs Total Nitrogen (filtered data)
"""


# This is the HTML output, it calls the graph with the id tn_tp_scatter which is pulled in an app callback
# The app callback just runs the tn_tp_all definition and outputs the returned figure as a graph figure here
# This definition is pulled in homepage.py to print the output on the homepage

def filter_dataframe(df, lake_name, year_slider):
    if type(year_slider) is not list:
        year_slider = [year_slider]

    yearRange = list(range(year_slider[0], year_slider[1]+1, 1))

    dff = df[df['Body of Water Name'].isin(lake_name)
             & (df['Year'].isin(yearRange))]
    return dff



def tn_tp_filtered(current_df):
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
        showlegend=True,
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


tn_tp_scatter_filter = dcc.Graph(id="tn_tp_filter_scatter")

@app.callback(Output('tn_tp_filter_scatter', 'figure'),
              [Input('intermediate-value', 'children'),
               Input('lake_statuses', 'value'),
               Input('filter-year-slider', 'value')],
              )
def make_filtered_TNTP_figure(jsonified_data, lake_statuses, year_value):
    df = convert_to_df(jsonified_data)
    dff = filter_dataframe(df, lake_statuses, year_value)
    return tn_tp_filtered(dff)




@app.callback(Output('lake_text', 'children'),
              [Input('lake_statuses', 'value'),
               Input('year_slider', 'value')])
def update_well_text(well_statuses, year_slider):

    dff = filter_dataframe(df, well_statuses, year_slider)
    return dff['Body of Water Name'].nunique()


choose2Filtered= html.Div([
        dcc.Graph(id='filtered-crossfilter-indicator-scatter'),
    html.Div([
        dcc.Dropdown(
            id='filtered-crossfilter-yaxis-column',
            options=[{'label': i, 'value': i} for i in available_indicators],
            value='Cytotoxin Cylindrospermopsin (ug/L)',
            className="eight columns",
        ),
    ],)
    ],)


def comp2GraphFiltered(dataframe, yaxis_column_name, yearRange):
    x.index = yearRange

    data = [
        go.Scatter(
        x=x.index,
        y=dataframe.loc[:, yaxis_column_name],
        mode='markers',
        text=dataframe.loc[:, 'Body of Water Name'],
        marker=dict(
            size=8,
        )
    ),
    ]

    layout = go.Layout(
        title='Raw Data Comparison of any Y over time',
        xaxis=dict(
            title="Date"),
        yaxis=dict(
            title=yaxis_column_name),
        hovermode='closest'
    )
    com2 = go.Figure(data=data, layout=layout)
    return com2


@app.callback(
    dash.dependencies.Output('filtered-crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('filtered-crossfilter-yaxis-column', 'value'),
     Input('lake_statuses', 'value'),
     Input('intermediate-value', 'children'),
     dash.dependencies.Input('filter-year-slider', 'value')])
def update_graph(yaxis_column_name, lake_statuses, jsonified_data, year_value):
    df = convert_to_df(jsonified_data)

    if type(year_value) is not list:
        year_value = [year_value]

    yearRange = list(range(year_value[0], year_value[1]+1, 1))
    dff = filter_dataframe(df, lake_statuses, yearRange)

    return comp2GraphFiltered(dff, yaxis_column_name, yearRange)
