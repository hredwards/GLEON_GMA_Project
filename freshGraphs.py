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
import matplotlib
from matplotlib import pyplot as plt

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
from old dash 


choose2AllGraph = html.Div([
        dcc.Graph(
            id="comparison_scatter",
        ),
        html.Div([
            html.Div([
                html.P('Y-axis'),
                dcc.Dropdown(
                    id='compare-y-axis',
                )], className='six columns'),
            html.Div([
                html.P('X-axis'),
                dcc.Dropdown(
                    id='compare-x-axis')
            ], className='six columns')
        ])
    ], className='row')

@app.callback(
    dash.dependencies.Output('comparison_scatter', 'figure'),
    [dash.dependencies.Input('compare-y-axis', 'value'),
     dash.dependencies.Input('compare-x-axis', 'value'),
     dash.dependencies.Input('intermediate-value', 'children')])
def update_comparison(selected_y, selected_x, jsonified_data):
    dff = convert_to_df(jsonified_data)
    return comparison_plot(selected_y, selected_x, dff)


"""


