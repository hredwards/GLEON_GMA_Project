import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import dash_table
from app import app


import pandas as pd
from s3References import client, MasterData, dfMasterData, MetadataDB, dfMetadataDB, Bucket






refreshButton = html.Button(id='refresh-db-button', children='Refresh',
            style={
                'margin': '10px 0px 10px 0px'
            }
            ),



def get_metadata_table_content(current_metadata):
    '''
        returns the data for the specified columns of the metadata data table
    '''

    table_df = current_metadata[
        ['DB_ID', 'DB_name', 'Uploaded_by', 'Upload_date', 'Microcystin_method', 'N_lakes', 'N_samples']]
    return table_df.to_dict("rows")








dataPageTable = html.Div([
dash_table.DataTable(
        id='metadata_table',
        columns=[
            # the column names are seen in the UI but the id should be the same as dataframe col name
            # the DB ID column is hidden - later used to find DB pkl files in the filtering process
            # TODO: add column for field method in table
            {'name': 'Database ID', 'id': 'DB_ID', 'hidden': True},
            {'name': 'Database Name', 'id': 'DB_name'},
            {'name': 'Uploaded By', 'id': 'Uploaded_by'},
            {'name': 'Upload Date', 'id': 'Upload_date'},
            {'name': 'Microcystin Method', 'id': 'Microcystin_method'},
            {'name': 'Number of Lakes', 'id': 'N_lakes'},
            {'name': 'Number of Samples', 'id': 'N_samples'}, ],
        data=get_metadata_table_content(dfMetadataDB),
        row_selectable='multi',
        selected_rows=[],
        style_as_list_view=True,
        # sorting=True,
        #style_table={'overflowX': 'scroll'},
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
    ),

    # Export the selected datasets in a single csv file
    html.A(html.Button(id='export-data-button', children='Download Selected Data',
                       style={
                           'margin': '10px 0px 10px 10px'
                       }),
           href='',
           id='download-link',
           download='data.csv',
           target='_blank'
           ),
])
