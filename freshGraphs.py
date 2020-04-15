import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from app import app
import numpy as np
from settings import months, USEPA_LIMIT, WHO_LIMIT
import plotly.graph_objs as go
import plotly.express as px


app.config['suppress_callback_exceptions'] = True

"""
Dataframe calling/definition; calls for masterdata.csv from S3 bucket
"""
from s3References import dfMasterData
df = dfMasterData

allColumnNames = list(df.columns.values)
df['Year'] = pd.DatetimeIndex(df['DATETIME']).year



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

tn_tp_scatter_all = html.Div([
    html.Div([
        html.H2('Total Phosphorus vs Total Nitrogen'),
        dcc.Graph(
            id="tn_tp_scatter",
        ),
    ]),
    html.Div(id='intermediate-value', style={'display': 'none'}, children=convert_to_json(df))

], className="col")

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
    html.Div([
        html.H2('Scatter Plot of any X/Y'),
        dcc.Graph(
            id='crossfilter-indicator-scatter',
        )
    ]),
    html.Div(dcc.RangeSlider(
        id='crossfilter-year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=[df['Year'].min(), df['Year'].max()],
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    )),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Alloxanthin (ug/L)'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
            )
        ], ),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Cytotoxin Cylindrospermopsin (ug/L)'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
            )
        ]), ]),
    ], className="col")


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
Mapbox Plot -- Microcystin Concentration Geographically
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
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation='v'),
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



mapPlot =html.Div(
    [
        dcc.Graph(id='map_MCConc')
    ],
)

""""
From Oil and Dash
mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(
        l=30,
        r=30,
        b=20,
        t=40
    ),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation='h'),
    title='Satellite Overview',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(
            lon=-78.05,
            lat=42.54
        ),
        zoom=7,
    )
)

@app.callback(Output('main_graph', 'figure'),
              [Input('well_statuses', 'value'),
               Input('well_types', 'value'),
               Input('year_slider', 'value')],
              [State('lock_selector', 'values'),
               State('main_graph', 'relayoutData')])
def make_main_figure(well_statuses, well_types, year_slider,
                     selector, main_graph_layout):

    dff = filter_dataframe(df, well_statuses, well_types, year_slider)

    traces = []
    for well_type, dfff in dff.groupby('Well_Type'):
        trace = dict(
            type='scattermapbox',
            lon=dfff['Surface_Longitude'],
            lat=dfff['Surface_latitude'],
            text=dfff['Well_Name'],
            customdata=dfff['API_WellNo'],
            name=WELL_TYPES[well_type],
            marker=dict(
                size=4,
                opacity=0.6,
            )
        )
        traces.append(trace)

    if (main_graph_layout is not None and 'locked' in selector):

        lon = float(main_graph_layout['mapbox']['center']['lon'])
        lat = float(main_graph_layout['mapbox']['center']['lat'])
        zoom = float(main_graph_layout['mapbox']['zoom'])
        layout['mapbox']['center']['lon'] = lon
        layout['mapbox']['center']['lat'] = lat
        layout['mapbox']['zoom'] = zoom
    else:
        lon = -78.05
        lat = 42.54
        zoom = 7

    figure = dict(data=traces, layout=layout)
    return figure




"""



