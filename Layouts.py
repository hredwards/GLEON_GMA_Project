import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from app import app
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import flask
from s3References import session, client, MasterData, pullMasterdata, pullMetaDB, Bucket, UploadFolder, dfexampleSheet, AssetsFolder
from flask import g, session as flaskSession

# from freshGraphs import convert_to_json, overTimeAll,
from freshGraphs import tn_tp_scatter_all, tn_tp_scatter_filter, choose2All, choose2Filtered, mapPlotFiltered, overTimeAll, overTimeFiltered, mapPlot, convert_to_json
from ViewFilteredData import filtersAvailable, FilteredView
from Homepage import Homepage

app.config['suppress_callback_exceptions'] = True


s3 = session.resource('s3')
dfMasterData = pullMasterdata()
dfMetadataDB = pullMetaDB()

"""
This has the layouts for every page except for the Homepage, Login, and Filtered Graph pages

In order: About, Data, Contact, Upload, UserPage

"""





"""
About 
"""

about = html.Div(
    [
        dbc.Row(
            [
                html.Div([
                    dbc.Row(html.H3("Gleon GMA Project - About"), style={'width':'100%', 'text-align':'center'}, justify="center", form=True),
                        dbc.Row(html.P(
                                        "The goal of the Global Microcystin Aggregation (GMA) project is to compile a global spatial/temporal"
                                        "dataset of freshwater microcystin and associated physicochemical water quality (e.g., TN, TP, Chl, Secchi, "
                                        "temperature, etc.), lake morphology (e.g., mean depth, volume, surface area), and watershed (e.g., land use "
                                        "metrics, watershed area) data to:"
                                    ), style={"padding-left":"4rem", "padding-right":"4rem", "text-size":"3rem"}),
                                    dbc.Row(html.Ol(
                                        children=[
                                            html.Li(
                                                "Describe the occurrence and concentrations of microcystins on a global spatial scale."),
                                            html.Li(
                                                "Examine temporal trends of microcystin concentrations on a global scale."),
                                            html.Li(
                                                "Develop global predictive and forecasting models for microcystin occurrence and concentrations based on:"),
                                            html.Ul(
                                                children=[
                                                    html.Li(
                                                        "TN,TP, Chl, Secchi, temperature and other widely sampled limnology variables"),
                                                    html.Li(
                                                        "lake morphology variables such as depth, volume, surface area, etc."),
                                                    html.Li(
                                                        "watershed variables such as land use, watershed area, and soil type"),
                                                    html.Li("possibly climate conditions and weather patterns."),
                                                ],
                                            ),
                                        ],
                                    ), style={"padding-left":"6rem", "padding-right":"6rem", "text-size":"3rem"}),
                    dbc.Row(html.H4("If you are interested in the project or have data to contribute, please contact us!", style={'textAlign': 'center', "padding-top":"5rem"}), justify="center", form=True),
                    dbc.Row(dbc.Button("Contact Us!", href="/Contact", color="secondary", size="lg", className="mr-1", style={'textAlign': 'center'}), justify="center", form=True),
                ], style={"padding-left":"4rem", "padding-right":"4rem", "text-size":"4rem"}, className='pretty_container six columns'),


                    html.Section(id="slideshow", children=[
                        html.Div(id="slideshow-container",
                                 children=[html.Div(id="image"),
                                           dcc.Interval(id='interval', interval=6000),
                                           ]),
                    ],className='pretty_container six columns')]),
       ], className="twelve columns"
)





### Photo Carousel
Photo1 = app.get_asset_url('FieldStation.jpg')
Photo2 = app.get_asset_url('HarrisSampling.jpg')
Photo3 = app.get_asset_url('Tank.jpg')

@app.callback(Output('image', 'children'),
              [Input('interval', 'n_intervals')])
def display_image(n):
    if n == None or n % 3 == 1:
        img = html.Div(html.Img(src=Photo1))
    elif n % 3 == 2:
        img = html.Div(html.Img(src=Photo2))
    elif n % 3 == 0:
        img = html.Div(html.Img(src=Photo3))
    else:
        img = "None"
    return img

#        img = html.Div(html.Img(src=Photo2), style={'display':'flex', 'height':'auto', 'width':'100%'})


def About():
    layout = about
    return layout



"""
Data 
"""

def get_metadata_table_content(current_metadata):
    '''
        returns the data for the specified columns of the metadata data table
    '''

    table_df = current_metadata[
        ['RefID', 'DB_ID', 'DB_name', 'Uploaded_by', 'Upload_date', 'PWYN', 'Microcystin_method', 'N_lakes', 'N_samples']]
    table_pwyn = table_df["PWYN"]
    table_df = table_df[table_pwyn!="Yes"]

    return table_df.to_dict("rows")


dataPageTable = dbc.Container([
    dbc.Row(html.P(
        "Here you can download any file that's been uploaded to our collection.", style={'textAlign':'center'}),
        justify="center", form=True),

    dash_table.DataTable(
        id='metadata_table',
        columns=[
            #{'name': 'Reference ID', 'id': 'RefID', 'hidden': True},
            #{'name': 'Database ID', 'id': 'DB_ID', 'hidden': True},
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
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
    ),

    dbc.Row(html.P(
        "Select as many as you'd like, the one file you download will contain all entries from selected sets.",
        style={'textAlign': 'center', 'margin': '2rem 0rem 0rem 0rem'}),
        justify="center", form=True),

    # Export the selected datasets in a single csv file
    dbc.Row(html.A(html.Button(id='export-data-button', children='Download Selected Data',
                       style={
                           'margin': '1rem 0px 1rem 1rem'
                       }),
           href='',
           id='download-link',
           download='data.csv',
           target='_blank'
           ),justify="center", form=True)
], style={"max-width":"90%"},)


def get_metadata_table_content_pw_protect(current_metadata):
    '''
        returns the data for the specified columns of the metadata data table
    '''

    table_df = current_metadata[
        ['RefID', 'DB_ID', 'DB_name', 'Uploaded_by', 'Upload_date', 'PWYN', 'Microcystin_method', 'N_lakes', 'N_samples']]
    table_pwyn = table_df["PWYN"]
    table_df = table_df[table_pwyn=="Yes"]

    return table_df.to_dict("rows")


dataPageTablepwProtect = dbc.Container([
    dbc.Row(html.P(
        "These files have been password protected by the uploader. Log in to download them if you are the owner."),
            justify="center", form=True),

    dash_table.DataTable(
        id='metadata_table_pwProtect',
        columns=[
            #{'name': 'Reference ID', 'id': 'RefID', 'hidden': True},
            #{'name': 'Database ID', 'id': 'DB_ID', 'hidden': True},
            {'name': 'Database Name', 'id': 'DB_name'},
            {'name': 'Uploaded By', 'id': 'Uploaded_by'},
            {'name': 'Upload Date', 'id': 'Upload_date'},
            {'name': 'Microcystin Method', 'id': 'Microcystin_method'},
            {'name': 'Number of Lakes', 'id': 'N_lakes'},
            {'name': 'Number of Samples', 'id': 'N_samples'}, ],
        data=get_metadata_table_content_pw_protect(dfMetadataDB),
        #row_selectable='multi',
        #selected_rows=[],
        style_as_list_view=True,
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
    ),

], style={"max-width":"90%"},)

dataPage = html.Div(
    [
        html.Div(
            [
                dbc.Row(html.H3("Download Available Datasets"), justify="center", form=True),
                dbc.Row(dataPageTable, justify="center", form=True)
            ],
            className="pretty_container ten columns offset-by-one column"),
        dbc.Row([], className="separatingLine twelve columns"),
        html.Div(
            [
                dbc.Row(html.H3("Protected Datasets"), justify="center", form=True),
                dbc.Row(dataPageTablepwProtect, justify="center", form=True)
            ],
            className="pretty_container ten columns offset-by-one column"),
    ],
    className="ten columns offset-by-one column"),


def Data():
    layout = dataPage
    return layout





"""
Contact
"""

table_header = [
    html.Thead(html.Tr([html.Th("Name"), html.Th("Role"), html.Th("E-Mail")]))
]

row1 = html.Tr([html.Td("Dr. Ted Harris"), html.Td("GMA Project Lead"), html.Td("ted.daniel.harris@gmail.com")])
row2 = html.Tr([html.Td("Data Science Student"), html.Td("Data Scientist/Web Interface Manager"), html.Td("gleon.gma@gmail.com")])

table_body = [html.Tbody([row1, row2])]

contactsTable = dbc.Table(table_header + table_body, bordered=True)



contact = html.Div(
    [
        html.Div([
            dbc.Row(html.H3("Welcome to the Contact Page!"), justify="center", form=True),
            dbc.Row(html.P(
                "We are looking for cyanobacteria researchers, algal/metabolite ecologists, ecological modelers, "
                "and database managers to: help find data in the literature and/or request microcystin and "
                "associated water quality data from colleagues at governmental and non-profit agencies, "
                "aggregate microcystin and associated water quality data with different sampling and analytical "
                "methods, and analyze a large database of global microcystin and associated water quality data "
                "for temporal and spatial trends."), justify="center", form=True, style={"padding":"3rem"}),
            dbc.Row(
                html.P("If you are interested in the project or have data to contribute, please contact us!", style={"padding-top":"2rem", "padding-bottom":"1.5rem"}), justify="center", form=True),
            dbc.Row(
                [
                    dbc.Button("Learn More About the Project", href="/About", color="secondary", size="lg",
                               className="mr-1", style={'textAlign': 'center', "padding":"1rem"}),
                ],
                justify="center", form=True
            ),

        ], style={"padding":"3rem"}, className="pretty_container six columns offset-by-three columns"),

        dbc.Row(contactsTable, style={"padding":"2rem"}, className="pretty_container six columns offset-by-three columns"),

    ],

)

def Contact():
    layout = contact
    return layout







"""
Upload


def Upload():
    layout = html.Div([
        uploadPage
    ], className="page-content")
    return layout


"""




"""

def get_metadata_table_content_User_Specific(current_metadata):
    '''
        returns the data for the specified columns of the metadata data table
    '''

    if flaskSession.get('user_id', 0) != 0:
        table_df = current_metadata[
            ['RefID', 'DB_ID', 'DB_name', 'Uploaded_by', 'Upload_date', 'PWYN', 'Microcystin_method', 'N_lakes',
             'N_samples']]
        table_refid = table_df["RefID"]
        table_df = table_df[table_refid == g.user_id]

    else:
        table_df = pd.DataFrame()

    return table_df.to_dict("rows")



userPageTable = dbc.Container([
    dbc.Row(html.P(
        "Welcome, NAME. Here you can download any file that you have uploaded to our collection.", style={'textAlign':'center'}),
        justify="center", form=True),

    dash_table.DataTable(
        id='metadata_table_userPage',
        columns=[
            #{'name': 'Reference ID', 'id': 'RefID', 'hidden': True},
            #{'name': 'Database ID', 'id': 'DB_ID', 'hidden': True},
            {'name': 'Database Name', 'id': 'DB_name'},
            {'name': 'Uploaded By', 'id': 'Uploaded_by'},
            {'name': 'Upload Date', 'id': 'Upload_date'},
            {'name': 'Microcystin Method', 'id': 'Microcystin_method'},
            {'name': 'Number of Lakes', 'id': 'N_lakes'},
            {'name': 'Number of Samples', 'id': 'N_samples'}, ],
        data=get_metadata_table_content_User_Specific(dfMetadataDB),
        row_selectable='multi',
        selected_rows=[],
        style_as_list_view=True,
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
    ),

    dbc.Row(html.P(
        "Select as many as you'd like, the one file you download will contain all entries from selected sets.",
        style={'textAlign': 'center', 'margin': '2rem 0rem 0rem 0rem'}),
        justify="center", form=True),

    # Export the selected datasets in a single csv file
    dbc.Row(html.A(html.Button(id='export-data-button', children='Download Selected Data',
                       style={
                           'margin': '1rem 0px 1rem 1rem'
                       }),
           href='',
           id='download-link-UserSpecific',
           download='data.csv',
           target='_blank'
           ),justify="center", form=True)
], style={"max-width":"90%"},)


dataPageUserSpecific = html.Div(
    [
        html.Div(
            [
                dbc.Row(html.H3("Download Available Datasets"), justify="center", form=True),
                dbc.Row(userPageTable, justify="center", form=True)
            ],
            className="pretty_container ten columns offset-by-one column"),

    ],
    className="ten columns offset-by-one column")


def UserPage():
    if flaskSession.get('user_id', 0) != 0:
        layout = dataPageUserSpecific
    return layout
"""


"""
def get_metadata_table_content_User_Specific(current_metadata):
    if flaskSession.get('user_id', 0) != 0:
        table_df = current_metadata[
            ['RefID', 'DB_ID', 'DB_name', 'Uploaded_by', 'Upload_date', 'PWYN', 'Microcystin_method', 'N_lakes',
             'N_samples']]
        table_refid = table_df["RefID"]
        table_df = table_df[table_refid == g.user_id]
        table_df = table_df.to_dict("rows")

    else:
        table_df = pd.DataFrame()
        table_df.to_dict("rows")

    return table_df

userPageTable = dbc.Container([
    dbc.Row(html.P(
        "Welcome, NAME. Here you can download any file that you have uploaded to our collection.",
        style={'textAlign': 'center'}),
        justify="center", form=True),

    dash_table.DataTable(
        id='metadata_table_userPage',
        columns=[
            # {'name': 'Reference ID', 'id': 'RefID', 'hidden': True},
            # {'name': 'Database ID', 'id': 'DB_ID', 'hidden': True},
            {'name': 'Database Name', 'id': 'DB_name'},
            {'name': 'Uploaded By', 'id': 'Uploaded_by'},
            {'name': 'Upload Date', 'id': 'Upload_date'},
            {'name': 'Microcystin Method', 'id': 'Microcystin_method'},
            {'name': 'Number of Lakes', 'id': 'N_lakes'},
            {'name': 'Number of Samples', 'id': 'N_samples'}, ],
        data=get_metadata_table_content_User_Specific(dfMasterData),
        row_selectable='multi',
        selected_rows=[],
        style_as_list_view=True,
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
    ),

    dbc.Row(html.P(
        "Select as many as you'd like, the one file you download will contain all entries from selected sets.",
        style={'textAlign': 'center', 'margin': '2rem 0rem 0rem 0rem'}),
        justify="center", form=True),

    # Export the selected datasets in a single csv file
    dbc.Row(html.A(html.Button(id='export-data-button', children='Download Selected Data',
                               style={
                                   'margin': '1rem 0px 1rem 1rem'
                               }),
                   href='',
                   id='download-link-UserSpecific',
                   download='data.csv',
                   target='_blank'
                   ), justify="center", form=True)
], style={"max-width": "90%"}, )

dataPageUserSpecific = html.Div(
    [
        html.Div(
            [
                dbc.Row(html.H3("Download Available Datasets"), justify="center", form=True),
                dbc.Row(userPageTable, justify="center", form=True)
            ],
            className="pretty_container ten columns offset-by-one column"),

    ],
    className="ten columns offset-by-one column")

def UserPage():
    if flaskSession.get('user_id', 0) != 0:
        layout = dataPageUserSpecific
    return layout




"""

