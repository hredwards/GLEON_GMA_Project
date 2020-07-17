import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from app import app
from dash.dependencies import Input, Output
import dash_table
import flask
from s3References import session, client, MasterData, pullMasterdata, pullMetaDB, Bucket, UploadFolder, dfexampleSheet, AssetsFolder
from uploadDownload import uploadBar
# from freshGraphs import convert_to_json, overTimeAll,
from freshGraphs import tn_tp_scatter_all, tn_tp_scatter_filter, choose2All, choose2Filtered, mapPlotFiltered, overTimeAll, overTimeFiltered, mapPlot, convert_to_json
from ViewFilteredData import filtersAvailable, FilteredView
from Homepage import Homepage

app.config['suppress_callback_exceptions'] = True

s3 = session.resource('s3')
dfMasterData = pullMasterdata()
dfMetadataDB = pullMetaDB()

"""
HomePage 
homepage = html.Div(
    [
        dbc.Col([
            dbc.Row(html.H3("Welcome to the Global Microcystin Aggregation Project!"), justify="center", form=True),

            dbc.Row(html.P("Below are some interactive graphs visualizing all the data that has been uploaded so far. Visit "
                       " the \'Filter Graphs\' page to apply filters to the dataset. Data can be downloaded from the \'Data\' page. Please login "
                       "to upload data. If you would like to learn more, please visit our About page or contact us via information on the Contact page.", style={"padding":"1rem", "margin":"1rem"}), justify="center", form=True),
            dbc.Row(dbc.Button("Learn More About the Project", href="/PageAbout", color="secondary", size="lg"), justify="center", form=True),], className="pretty_container twelve columns"),
        html.Div(
            [
                dbc.Col([mapPlot], className="six columns"),
                dbc.Col([tn_tp_scatter_all], className="six columns"),
            ], className="twelve columns"),
        html.Div(
            [
                dbc.Col([choose2All], className="six columns"),
                dbc.Col([overTimeAll], className="six columns"),
            ], className="twelve columns"),
        html.Div(id='intermediate-value', style={'display': 'none'}, children=convert_to_json(dfMasterData)),
    ], className="twelve columns"
)


def Homepage():
    layout = homepage
    return layout


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
        row_selectable='multi',
        selected_rows=[],
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
       dbc.Row(html.H3("Welcome to the Data Page!"), justify="center", form=True),
        dbc.Row(html.P("Here you can download any file that's been uploaded to our collection. Select as many as you'd like, the one file you download will contain all entries from selected sets.", style={"padding":"2rem"}), justify="center", form=True),
        dbc.Row(dataPageTable, justify="center", form=True),
        dbc.Row(dataPageTablepwProtect, justify="center", form=True)

    ],
    className="pretty_container twelve columns",
)


def Data():
    layout = dataPage
    return layout

"""
Filtered View

filtView = html.Div(
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

        html.Div(id='intermediate-value', style={'display': 'none'}, children=convert_to_json(dfMasterData)),
    ], id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    },
    className="twelve columns",
)


def FilteredView():
    layout = filtView
    return layout

"""



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
Login


# Create a login route
_app_route = '/Upload'

@app.server.route('/login', methods=['POST'])
def route_login():
    data = flask.request.form
    username = data.get('username')
    password = data.get('password')

    if username not in creds.keys() or  creds[username] != password:
        return flask.redirect('/Login')
    else:

        # Return a redirect with
        rep = flask.redirect(_app_route)
        rep.set_cookie('custom-auth-session', username)
        return rep


login_form = dbc.Row([
    html.Form([
        dcc.Input(placeholder='username', name='username', type='text'),
        dcc.Input(placeholder='password', name='password', type='password'),
        html.Button('Login', type='submit')
    ], action='/login', method='post')
], justify="center", form=True,   className="twelve columns",
)


login = html.Div([
    dbc.Row(html.H3("Welcome to the Login Page!"), justify="center", form=True, className="twelve columns"),
    html.Div(id='custom-auth-frame'),
    html.Div(id='custom-auth-frame-1', style={'textAlign': 'right', "background": "black"}),
    login_form,
    dbc.Row(dbc.Button("Want a login?", href="/Contact", color="secondary", style={"margin":"2rem"}), justify="center", form=True),
], className="pretty_container four columns offset-by-four columns",
)


def Login():
    layout = login
    return layout




"""



"""
Upload
"""

def Upload():
    layout = html.Div([
        uploadBar
    ], className="page-content")
    return layout


"""
Register Account
"""

registration_form = dbc.Row([
    html.Form([
        dcc.Input(placeholder='username', name='username', type='text'),
        dcc.Input(placeholder='password', name='password', type='password'),
        html.Button('Login', type='submit')
    ], action='/register', method='post')
], justify="center", form=True,   className="twelve columns",
)


register = html.Div([
    dbc.Row(html.H3("Welcome to the Login Page!"), justify="center", form=True, className="twelve columns"),
    html.Div(id='custom-auth-frame'),
    html.Div(id='custom-auth-frame-1', style={'textAlign': 'right', "background": "black"}),
    registration_form,
    dbc.Row(dbc.Button("Want a login?", href="/Contact", color="secondary", style={"margin":"2rem"}), justify="center", form=True),
], className="pretty_container four columns offset-by-four columns",
)


def Register():
    layout = register
    return layout

"""
Login to existing Account
loginExisting = html.Div([
    dbc.Row(html.H3("Welcome to the Login Page!"), justify="center", form=True, className="twelve columns"),
    html.Div(id='custom-auth-frame'),
    html.Div(id='custom-auth-frame-1', style={'textAlign': 'right', "background": "black"}),
    login_form,
    dbc.Row(dbc.Button("Want a login?", href="/Contact", color="secondary", style={"margin":"2rem"}), justify="center", form=True),
], className="pretty_container four columns offset-by-four columns",
)


def LoginExisting():
    layout = loginExisting
    return layout


"""
