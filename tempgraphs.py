### Just for testing S3 rn; move to graphys.py later ###

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import dash_table
from app import app
import numpy as np
import data_analysis as da
from settings import months, USEPA_LIMIT, WHO_LIMIT
#import db_engine as db
#from db_info import db_info
#import urllib.parse
import json

## pulls s3 info from s3References ##
from s3References import client, MasterData, dfMasterData, MetadataDB, dfMetadataDB

app.config['suppress_callback_exceptions'] = True


""""
Import MasterData file
"""
def get_masterData_table_tnnPlotAll(current_masterdata):
    '''
        returns the data for the specified columns of the master data table
    '''

    table_df = current_masterdata[
        ['Body of Water Name', 'Total Nitrogen (ug/L)', 'Total Phosphorus (ug/L)', 'Microcystin (ug/L)']]
    return table_df.to_dict("rows")

df = dfMasterData



def convert_list_to_json(current_dataframe):
    '''
        converts the master df to a JSON string
    '''
    jsonStr = json.dumps(current_dataframe)
    return jsonStr

def convert_list_to_df(jsonified_data):
    '''
        converts the JSON string back to a dataframe
    '''
    listDF = pd.DataFrame(jsonified_data)
    return listDF





""""
MappedMicrocystin -- Geographical map of Microcystin levels from MasterData
OverallTrends --
"""
### Graph Definitions ###






# Graph is id as tn_tp_scatter_all and uses range sliders tn_range_all and tp_range_all

""""
def tn_tp_all(tn_val, tp_val, current_df):
    min_tn = tn_val[0]
    max_tn = tn_val[1]
    min_tp = tp_val[0]
    max_tp = tp_val[1]


    if max_tn == 0:
        max_tn = np.max(current_df.loc[:, "Total Nitrogen (ug/L)"])

    if max_tp == 0:
        max_tp = np.max(current_df.loc[:, "Total Phosphorus (ug/L)"])

    dat = current_df[
        (current_df.loc[:, 'Total Nitrogen (ug/L)'] >= min_tn) & (current_df.loc[:, 'Total Nitrogen (ug/L)'] <= max_tn) & (
                    current_df.loc[:, 'Total Phosphorus (ug/L)'] >= min_tp) & (
                    current_df.loc[:, 'Total Phosphorus (ug/L)'] <= max_tp)]
    MC_conc = dat.loc[:, 'Body of Water Name']
    # make bins
    b1 = dat[MC_conc <= USEPA_LIMIT]
    b2 = dat[(MC_conc > USEPA_LIMIT) & (MC_conc <= WHO_LIMIT)]
    b3 = dat[MC_conc > WHO_LIMIT]

    data = [go.Scatter(
        x=np.log(b1[1]),
        y=np.log(b1[2]),
        mode='markers',
        name="<USEPA",
        text=current_df[0],
        marker=dict(
            size=8,
            color="green",  # set color equal to a variable
        )),
        go.Scatter(
            x=np.log(b2[1]),
            y=np.log(b2[2]),
            mode='markers',
            name=">USEPA",
            text=current_df[0],
            marker=dict(
                size=8,
                color="orange"  # set color equal to a variable
            )),
        go.Scatter(
            x=np.log(b3[1]),
            y=np.log(b3[2]),
            mode='markers',
            name=">WHO",
            text=current_df[0],
            marker=dict(
                size=8,
                color="red",  # set color equal to a variable
            ))]

    layout = go.Layout(
        showlegend=True,
        xaxis=dict(
            title='log TN'),
        yaxis=dict(
            title="log TP"),
        hovermode='closest'
    )

    return (go.Figure(data=data, layout=layout))

tnTPPlotAll = html.Div([
    html.H2('Total Phosphorus vs Total Nitrogen'),
    dcc.Graph(
        id="tn_tp_scatter_all",
    ),
    html.Div([
        html.P("Log TN:"),
        dcc.RangeSlider(
            id="tn_range_all",
            min=0,
            step=None,
            marks={
                1000: '1',
                4000: '100',
                7000: '1000',
                10000: '10000'
            },
        ),
    ]),
    html.Div([
        html.P("Log TP:"),
        dcc.RangeSlider(
            id="tp_range_all",
            min=0,
            step=None,
            marks={
                1000: '1',
                4000: '100',
                7000: '1000',
                10000: '10000'
            },
        ),
    ]),

], className="row")
















@app.callback(
    Output('tn_tp_scatter_all', 'figure'),
     [Input('tn_range_all', 'value'),
     Input('tp_range_all', 'value')])
def update_output(tn_val, tp_val):
    #dff = convert_list_to_df(df)
    return tn_tp_all(tn_val, tp_val, df)








"""











""""

tnTPPlot = html.Div([
             html.H2('Total Phosphorus vs Total Nitrogen'),
             dcc.Graph(
                 id="tn_tp_scatter",
             ),
             html.Div([
                 html.P("Log TN:"),
                 dcc.RangeSlider(
                     id="tn_range",
                     min=0,
                     step=0.5,
                     marks={
                         1000: '1',
                         4000: '100',
                         7000: '1000',
                         10000: '10000'
                     },
                 ),
                 html.Div(id='intermediate-value', style={'display': 'none'}, children=convert_to_json(pdDfMasterData))

             ]),])


@app.callback(
    [dash.dependencies.Output('intermediate-value', 'children'),
     dash.dependencies.Output('tn_range', 'max'),
     dash.dependencies.Output('tn_range', 'value'),
     dash.dependencies.Output('tp_range', 'max'),
     dash.dependencies.Output('tp_range', 'value'),
     dash.dependencies.Output('year-dropdown', 'options'),
     dash.dependencies.Output('year-dropdown', 'value'),
     dash.dependencies.Output('temporal-lake-location', 'options'),
     dash.dependencies.Output('temporal-lake-location', 'value'),
     dash.dependencies.Output('temporal-lake-col', 'options'),
     dash.dependencies.Output('temporal-lake-col', 'value'),
     dash.dependencies.Output('temporal-avg-col', 'options'),
     dash.dependencies.Output('temporal-avg-col', 'value'),
     dash.dependencies.Output('temporal-raw-col', 'options'),
     dash.dependencies.Output('temporal-raw-col', 'value'),
     dash.dependencies.Output('axis_range_raw', 'max'),
     dash.dependencies.Output('axis_range_raw', 'value'),
     dash.dependencies.Output('compare-y-axis', 'options'),
     dash.dependencies.Output('compare-y-axis', 'value'),
     dash.dependencies.Output('compare-x-axis', 'options'),
     dash.dependencies.Output('compare-x-axis', 'value')],
    # dash.dependencies.Output('correlation-dropdown', 'options'),
    # dash.dependencies.Output('correlation-dropdown', 'value')] -- for correlation matrix
    [dash.dependencies.Input('apply-filters-button', 'n_clicks')],
    [dash.dependencies.State('metadata_table', 'derived_virtual_selected_rows'),
     dash.dependencies.State('metadata_table', 'derived_virtual_data')])
def update_graph(n_clicks, derived_virtual_selected_rows, dt_rows):
    if n_clicks != None and n_clicks > 0 and derived_virtual_selected_rows is not None:
        # update the user's data based on the selected databases
        selected_rows = [dt_rows[i] for i in derived_virtual_selected_rows]
        new_df = db.update_dataframe(selected_rows)
        print("NEW DF: ", new_df)

        # List of datasets and notice for correlation matrix
        correlation_notice = {'display': 'block'}
        db_name = [{'label': row['DB_name'], 'value': row['DB_name']} for row in selected_rows]
        db_value = db_name[0]

        jsonStr = convert_to_json(new_df)

        # update range for raw data graph
        raw_range_max = np.max(new_df["Microcystin (ug/L)"])
        raw_range_value = [0, np.max(new_df["Microcystin (ug/L)"])]

        tn_max = np.max(new_df["Total Nitrogen (ug/L)"])
        tn_value = [0, np.max(new_df["Total Nitrogen (ug/L)"])]

        tp_max = np.max(new_df["Total Phosphorus (ug/L)"])
        tp_value = [0, np.max(new_df["Total Phosphorus (ug/L)"])]

        # update the date ranges
        year = pd.to_datetime(new_df['DATETIME']).dt.year
        years = range(np.min(year), np.max(year) + 1)
        years_options = [{'label': str(y), 'value': y} for y in years]

        # update the lake locations
        locs = list(new_df["Body of Water Name"].unique())
        locs.sort()
        locs_options = [{'label': loc, 'value': loc} for loc in locs]
        locs_value = locs[0]

        # get current existing column names and remove general info to update the dropdowns of plot axes
        colNames = new_df.columns.values.tolist()
        if 'DATETIME' in colNames: colNames.remove('DATETIME')
        if 'Body of Water Name' in colNames: colNames.remove('Body of Water Name')
        if 'DataContact' in colNames: colNames.remove('DataContact')
        if 'LONG' in colNames: colNames.remove('LONG')
        if 'LAT' in colNames: colNames.remove('LAT')
        if 'Comments' in colNames: colNames.remove('Comments')
        if 'MC Percent Change' in colNames: colNames.remove('MC Percent Change')
        if 'Maximum Depth (m)' in colNames: colNames.remove('Maximum Depth (m)')
        if 'Mean Depth (m)' in colNames: colNames.remove('Mean Depth (m)')

        colNames.sort()
        col_options = [{'label': col, 'value': col} for col in colNames]
        col_value = colNames[0]
        col_value_next = colNames[1]

        return jsonStr, tn_max, tn_value, tp_max, tp_value, years_options, years_options, locs_options, locs_value, col_options, col_value, col_options, col_value, col_options, col_value, raw_range_max, raw_range_value, col_options, col_value, col_options, col_value_next,  # db_name, db_value


def tn_tp(tn_val, tp_val, current_df):
    min_tn = tn_val[0]
    max_tn = tn_val[1]
    min_tp = tp_val[0]
    max_tp = tp_val[1]

    if max_tn == 0:
        max_tn = np.max(current_df["Total Nitrogen (ug/L)"])

    if max_tp == 0:
        max_tp = np.max(current_df["Total Phosphorus (ug/L)"])

    dat = current_df[
        (current_df["Total Nitrogen (ug/L)"] >= min_tn) & (current_df["Total Nitrogen (ug/L)"] <= max_tn) & (
                    current_df["Total Phosphorus (ug/L)"] >= min_tp) & (
                    current_df["Total Phosphorus (ug/L)"] <= max_tp)]
    MC_conc = dat['Microcystin (ug/L)']
    # make bins
    b1 = dat[MC_conc <= USEPA_LIMIT]
    b2 = dat[(MC_conc > USEPA_LIMIT) & (MC_conc <= WHO_LIMIT)]
    b3 = dat[MC_conc > WHO_LIMIT]

    data = [go.Scatter(
        x=np.log(b1["Total Nitrogen (ug/L)"]),
        y=np.log(b1["Total Phosphorus (ug/L)"]),
        mode='markers',
        name="<USEPA",
        text=current_df["Body of Water Name"],
        marker=dict(
            size=8,
            color="green",  # set color equal to a variable
        )),
        go.Scatter(
            x=np.log(b2["Total Nitrogen (ug/L)"]),
            y=np.log(b2["Total Phosphorus (ug/L)"]),
            mode='markers',
            name=">USEPA",
            text=current_df["Body of Water Name"],
            marker=dict(
                size=8,
                color="orange"  # set color equal to a variable
            )),
        go.Scatter(
            x=np.log(b3["Total Nitrogen (ug/L)"]),
            y=np.log(b3["Total Phosphorus (ug/L)"]),
            mode='markers',
            name=">WHO",
            text=current_df["Body of Water Name"],
            marker=dict(
                size=8,
                color="red",  # set color equal to a variable
            ))]

    layout = go.Layout(
        showlegend=True,
        xaxis=dict(
            title='log TN'),
        yaxis=dict(
            title="log TP"),
        hovermode='closest'
    )

    return (go.Figure(data=data, layout=layout))


@app.callback(
    dash.dependencies.Output('tn_tp_scatter', 'figure'),
    [dash.dependencies.Input('tn_range', 'value'),
     dash.dependencies.Input('tp_range', 'value'),
     dash.dependencies.Input('intermediate-value', 'children')])
def update_output(tn_val, tp_val, jsonified_data):
    dff = convert_to_df(jsonified_data)
    return tn_tp(tn_val, tp_val, dff)





"""




