import base64
import os
from urllib.parse import quote as urlquote

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import datetime
import base64
import io
from dash.dependencies import Input, Output, State
from app import app
from s3References import session, client, MasterData, pullMasterdata, pullMetaDB, Bucket, UploadFolder, dfexampleSheet, AssetsFolder
from botocore.exceptions import ClientError, NoCredentialsError
import boto3
import fuzzywuzzy
from controls import month_Controls, Substrate_Status_options, Sample_Types_options, Field_Methods_options, Microcystin_Method_options, data_Review_options
from dash_reusable_components import Card, NamedSlider, NamedInlineRadioItems, HalsNamedInlineRadioItems
import dash_table
import urllib.parse

s3 = session.resource('s3')
dfMasterData = pullMasterdata()
dfMetadataDB = pullMetaDB()

dfexampleSheet = dfexampleSheet.to_csv(index=False, encoding='utf-8')
dfexampleSheet = "data:text/csv;charset=utf-8," + urllib.parse.quote(dfexampleSheet)



login_form = html.Div([
    html.Form([
        dcc.Input(placeholder='username', name='username', type='text'),
        dcc.Input(placeholder='password', name='password', type='password'),
        html.Button('Login', type='submit')
    ], action='/login', method='post')
])

class db_info:
    def __init__(self, db_name, uploaded_by, institution):
        current_date = datetime.datetime.now()
        self.RefID = ''
        self.db_name = db_name
        self.uploaded_by = uploaded_by
        self.institution = institution
        self.upload_date = current_date.strftime("%Y\%m\%d")
        self.db_id = db_name.replace(" ", "_") + '_' + uploaded_by.replace(" ", "_") + '_' + current_date.strftime(
            "%Y\%m\%d")
        self.db_publish_YN = ''
        self.db_field_method_YN = ''
        self.db_field_method = ''
        self.db_lab_method = ''
        self.db_qaqc = ''
        self.db_fullqaqc = ''
        self.db_filter = ''
        self.db_publication_url = ''
        self.db_field_method_url = ''
        self.db_lab_method_url = ''
        self.db_QAQC_url = ''
        self.db_full_QCQC_url = ''
        self.db_substrate = ''
        self.db_sample_type = ''
        self.db_microcystin_method = ''
        self.db_filter_size = ''
        self.db_cell_count_method = ''
        self.db_ancillary_url = ''
        self.db_num_lakes = 0
        self.db_num_samples = 0

def get_csv_path(db_id):
    return db_id + '.csv'

"""
Metadata
"""



"""
Upload Bar Layout and Callbacks
"""
## Step 1. Links to example csv
exampleBar = dbc.Container([
    html.H5('Step 3. Download the outline file below and copy the appropriate data into the csv file.', id="Instructions"),

    dbc.Row(html.A("Download Datasheet Outline File", href=dfexampleSheet, target='blank', download='GLEON_GMA_OUTLINE.csv',
           className="mr-1", style={'textAlign': 'center', "padding":"2rem .5rem 2rem .5rem"}), justify="center", form=True),
])

## Step 2. Spot to upload files
dragUpload = dbc.Container([
    html.H5('Step 4. Select or drag and drop the filled out csv file containing your data using the provided outline.', id="Instructions"),

    dcc.Upload(
        id="upload-data",
        children=[
            "Drag and Drop or ",
            html.A(children="Select a File"),
        ],
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },

        accept=".csv, .xls, .xlsx",
    ),
    html.Div(id='upload-output'),
],)

## Step 3. Questions for Data Source Information
uploadDataInfo = dbc.Container([
    html.H5('Step 1. Fill out the Data Source questionnaire below with appropriate information and links as needed.',
           id="Instructions"),

    #### Identifying - Name, Institution, Database Name
    dbc.Row([
        html.Form([
            dcc.Input(placeholder='Name', id='uploader-Name', type='text'),
            dcc.Input(placeholder='Institution', id='user-inst', type='text'),
            dcc.Input(placeholder='Database Name', id='db-name', type='text'),
        ]),
    ]),

    #### Things with URL inputs - Peer Reviewed, Field Method, Lab Method, QA, Full QA
    dbc.Row([
        HalsNamedInlineRadioItems(
            name="Is the data peer reviewed or published?",
            id="is-data-reviewed",
            options=data_Review_options,
        ),
        dcc.Input(
            placeholder='URL Link',
            type='text',
            id='publication-url',
            style={'display': 'none'}),
    ]),

    dbc.Row([
        HalsNamedInlineRadioItems(
            name="Is the field method reported?",
            id="is-field-method-reported",
            options=data_Review_options,
        ),
        dcc.Input(
            placeholder='URL Link',
            type='text',
            id='field-method-report-url',
            style={'display': 'none'}),
    ]),

    dbc.Row([
        HalsNamedInlineRadioItems(
            name="Is the lab method reported?",
            id="is-lab-method bui-reported",
            options=data_Review_options,
        ),
        dcc.Input(
            placeholder='URL Link',
            type='text',
            id='lab-method-report-url',
            style={'display': 'none'}),
   ]),
    dbc.Row([
        HalsNamedInlineRadioItems(
            name='Is the QA/QC data available?',
            id="is-qaqc-available",
            options=data_Review_options,
        ),
        dcc.Input(
            placeholder='URL Link',
            type='text',
            id='qaqc-url',
            style={'display': 'none'}
        ),
    ]),

    dbc.Row([
        HalsNamedInlineRadioItems(
            name = 'Is the full QA/QC data available upon request?',
            id="is-full-qaqc-available",
            options=data_Review_options,
        ),
        dcc.Input(
            placeholder='URL Link',
            type='text',
            id='full-qaqc-url',
            style={'display': 'none'}
        ),
    ]),
    # Cell Count
    dbc.Row([
        dbc.Row(html.P('Cell count method?')),
        dbc.Row(
            dcc.Input(
                placeholder='URL Link',
                type='text',
                id='cell-count-url',
                style={'display': 'inline-block', 'margin-left':'.5rem', 'text-align':'center'}

            ),
        ),
    ]),

    # Ancillary
    dbc.Row([
        dbc.Row(html.P('Ancillary data available?')),
        dbc.Row(
            dcc.Textarea(
                placeholder='Description of parameters or URL link',
                id='ancillary-data',
                style={'display': 'inline-block', 'margin-left': '.5rem', 'text-align': 'center'}

            ),
        ),
    ]),
],)


## Step 4. Questions for Methodology Information
uploadMethodologies = dbc.Container([
    html.H5('Step 2. Fill out the Methodology questionnaire below with appropriate information and links as needed.', id="Instructions"),

    # Substrate
    dbc.Row([
        HalsNamedInlineRadioItems(
        name="Substrate",
        id="substrate-option",
        options=Substrate_Status_options,
    )], className="uploadOption"),

    # Sample Type
    dbc.Row([HalsNamedInlineRadioItems(
        name="Sample Types",
        id="sample-type-option",
        options=Sample_Types_options,
    ),]),

    # Field Method
    dbc.Row([
        HalsNamedInlineRadioItems(
            name="Field Method",
            id="field-method-option",
            options=Field_Methods_options
        ),
        dcc.Input(
            placeholder='Depth Integrated (m)',
            type='text',
            id='vertically-depth-integrated',
            style={'display': 'none'}
        ),
        dcc.Input(
            placeholder='Depth Sampled (m)',
            type='text',
            id='discrete-depth-sampled',
            style={'display': 'none'}
        ),
        dcc.Input(
            placeholder='Depth of Sample (m)',
            type='text',
            id='spatially-integrated-depth',
            style={'display': 'none'}
        ),
        dcc.Input(
            placeholder='# of samples integrated',
            type='text',
            id='num-spatially-integrated-samples',
            style={'display': 'none'}
        ),
    ]),

    #### Microcystin Method and filtering
    dbc.Row([HalsNamedInlineRadioItems(
        name="Microcystin Method",
        id="microcystin-method",
        options=Microcystin_Method_options,
    ),]),
    dbc.Row([
        HalsNamedInlineRadioItems(
            name="Was Sample Filtered?",
            id="sample-filtered",
            options=data_Review_options,
        ),
        dcc.Input(
            placeholder='Filter Size (μm)',
            type='text',
            id='filter-size',
            style={'display': 'none'}
        ),
    ]),

],)


## Step 5. Upload button and warning about using outline
uploadButton = dbc.Container([
    html.H5('Step 5.  Click \'Upload\' to ''upload your data and information to the project.', id="Instructions"),

    html.P('**Please note, the data must be in the same format as the outline file provided in step 3 above. Failure to use this '
                'outline will likely return an error.**', style={'font-size': '1.5rem'}),

    html.Button(id='upload-button', n_clicks=0, children='Upload',
                style={'margin': '1rem .5rem .6rem .5rem', 'justify': 'center'}),

    dbc.Row(html.P(id='upload-msg')),
],)



## Combines all the questions/forms from above into one section, this is what's actually returned to the page
uploadBar=html.Div([
    dbc.Row([
                dbc.Row(html.H5(
                    "Thank you for your interest in contributing to our data collection! Please follow the 5 steps below to upload your file to our database.",
                    style={'textAlign': 'center'}), justify="center", form=True),
                dbc.Row(html.A("Contact us with any questions, problems, or concerns!", href="/PageContact",
                           className="mr-1", style={'textAlign': 'center', "padding":"2rem .5rem 2rem .5rem"}), justify="center", form=True),

    ], className="twelve columns"),


    dbc.Row([
        dbc.Col(exampleBar, className="pretty_container six columns"),
        dbc.Col(dragUpload, className="pretty_container six columns"),
    ], className="twelve columns"),


    dbc.Row([
        dbc.Col(uploadDataInfo, className="pretty_container six columns"),
        dbc.Col(uploadMethodologies, className="pretty_container six columns"),
    ], className="twelve columns"),

    html.Div([
        dbc.Col(uploadButton, className="pretty_container offset-by-two columns"),

    ], className="eight columns"),

], className="twelve columns")


uploadBar=html.Div([
    dbc.Col([
                dbc.Row(html.H5(
                    "Thank you for your interest in contributing to our data collection! Please follow the 5 steps below to upload your file to our database.",
                    style={'textAlign': 'center'}), justify="center", form=True),
                dbc.Row(html.A("Contact us with any questions, problems, or concerns!", href="/PageContact",
                           className="mr-1", style={'textAlign': 'center', "padding":"2rem .5rem 2rem .5rem"}), justify="center", form=True),

    ], className="twelve columns"),
    dbc.Row(uploadDataInfo, className='pretty_container ten columns offset-by-one'),
    dbc.Row(uploadMethodologies, className='pretty_container ten columns offset-by-one'),
    dbc.Row([
        dbc.Col(exampleBar, className="pretty_container five columns"),
        dbc.Col(dragUpload, className="pretty_container five columns"),
    ], className="ten columns offset-by-one"),
    dbc.Row(uploadButton, className= 'pretty_container ten columns offset-by-one')
], className="twelve columns")




"""
Callbacks for inputs with URLs or Other Fields if "Yes"
"""
# Controls if text fields are visible based on selected options in upload questionnaire
@app.callback(
    Output('publication-url', 'style'),
    [Input('is-data-reviewed', 'value')]
)
def show_peer_review_url(is_peer_reviewed):
    if is_peer_reviewed == 'Yes':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('field-method-report-url', 'style'),
    [Input('is-field-method-reported', 'value')]
)
def show_field_method_url(is_fm_reported):
    if is_fm_reported == 'Yes':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('lab-method-report-url', 'style'),
    [Input('is-lab-method bui-reported', 'value')]
)
def show_lab_method_url(is_lm_reported):
    if is_lm_reported == 'Yes':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('qaqc-url', 'style'),
    [Input('is-qaqc-available', 'value')]
)
def show_qaqc_url(is_qaqc_available):
    if is_qaqc_available == 'Yes':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('full-qaqc-url', 'style'),
    [Input('is-full-qaqc-available', 'value')]
)
def show_full_qaqc_url(is_full_qaqc_available):
    if is_full_qaqc_available == 'Yes':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    dash.dependencies.Output('filter-size', 'style'),
    [dash.dependencies.Input('sample-filtered', 'value')]
)
def show_filter_size(visibility_state):
    if visibility_state == 'Yes':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    [Output('vertically-depth-integrated', 'style'),
     Output('discrete-depth-sampled', 'style'),
     Output('spatially-integrated-depth', 'style'),
     Output('num-spatially-integrated-samples', 'style')],
    [Input('field-method-option', 'value')])
def show_field_option_input(field_option):
    if field_option == 'VIS':
        return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}
    if field_option == 'DDS':
        return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
    if field_option == 'SIS':
        return {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, {'display': 'block'}
    else:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}














"""
Upload Functionality
"""
def upload_to_aws(filename, objectName):
    s3 = client
    objectName = objectName + str(filename)

    try:
        s3.upload_file(filename, Bucket, objectName)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def update_metadata(new_dbinfo):
    """
        Add new database info to MetadataDB.csv
    """
    try:
        new_dbdf = pd.DataFrame({'DB_ID': [new_dbinfo.db_id],
                                 'RefID': [new_dbinfo.RefID],
                                 'Institution': [new_dbinfo.institution],
                                 'DB_name': [new_dbinfo.db_name],
                                 'Uploaded_by': [new_dbinfo.uploaded_by],
                                 'Upload_date': [new_dbinfo.upload_date],
                                 'Published_url': [new_dbinfo.db_publication_url],  # url
                                 'Field_method_url': [new_dbinfo.db_field_method_url],  # url
                                 'Lab_method_url': [new_dbinfo.db_lab_method_url],  # url
                                 'QA_QC_url': [new_dbinfo.db_QAQC_url],  # url
                                 'Full_QA_QC_url': [new_dbinfo.db_full_QAQC_url],  # url
                                 'Substrate': [new_dbinfo.db_substrate],
                                 'Sample_type': [new_dbinfo.db_sample_type],
                                 'Field_method': [new_dbinfo.db_field_method],
                                 'Microcystin_method': [new_dbinfo.db_microcystin_method],
                                 'Filter_size': [new_dbinfo.db_filter_size],
                                 'Cell_count_method': [new_dbinfo.db_cell_count_method],
                                 'Ancillary_data': [new_dbinfo.db_ancillary_url],
                                 'N_lakes': [new_dbinfo.db_num_lakes],
                                 'N_samples': [new_dbinfo.db_num_samples],
                                 'Published': [new_dbinfo.db_publish_YN],
                                 'Field_method_YN': [new_dbinfo.db_field_method_YN],
                                 'Lab_method': [new_dbinfo.db_lab_method],
                                 'QA_QC': [new_dbinfo.db_qaqc],
                                 'QA_QC_Request': [new_dbinfo.db_fullqaqc],
                                 'Filter_YN': [new_dbinfo.db_filter]})

        metadataDB = pd.concat([dfMetadataDB, new_dbdf], sort=False).reset_index(drop=True)
        metadataDB =metadataDB.fillna("Not Reported")
        metadataDB.to_csv("MetadataDB.csv", encoding='utf-8', index=False)
        upload_to_aws("MetadataDB.csv", AssetsFolder)
    except Exception as e:
        print(e)
        return 'Error saving metadata'

def upload_new_database(new_dbinfo, contents, filename):
    """
        Decode contents of the upload component and create a new dataframe
    """
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            new_df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            return parse_new_database(new_dbinfo, new_df)
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            new_df = pd.read_excel(io.BytesIO(decoded))
            return parse_new_database(new_dbinfo, new_df)
        else:
            return 'Invalid file type.'

    except Exception as e:
        print(e)
        return 'There was an error processing this file.'



def parse_new_database(new_dbinfo, new_df):
    """
        Convert CSV or Excel file data into Pickle file and store in the data directory
    """
    global dfMasterData, dfMetadataDB

    try:

        # delete the extra composite section of the lake names - if they have any
        new_df['Body of Water Name'] = new_df['Body of Water Name']. \
            str.replace(r"[-]?.COMPOSITE(.*)", "", regex=True). \
            str.strip()

        new_df['Date'] = pd.to_datetime(new_df['Date']).dt.strftime('%Y-%m-%d %H:%M:%S')
        new_df['RefID'] = new_dbinfo.RefID

        print(new_df['Body of Water Name'])
        """
        # convert mg to ug
        new_df['TP_mgL'] *= 1000
        new_df['TN_mgL'] *= 1000
        
        """


        # format all column names
        new_df.rename(columns={'Date': 'DATETIME',},
                      inplace=True)

        # remove NaN columns
        csvdir = get_csv_path(new_dbinfo.db_id)
        new_df.to_csv(csvdir)

        # update the number of lakes and samples in db_info
        unique_lakes_list = list(new_df["Body of Water Name"].unique())
        new_dbinfo.db_num_lakes = len(unique_lakes_list)
        new_dbinfo.db_num_samples = new_df.shape[0]

        filename = str(csvdir)
        upload_to_aws(filename, UploadFolder)
        update_metadata(new_dbinfo)

        masterDataDB = pd.concat([dfMasterData, new_df], sort=False).reset_index(drop=True)
        masterDataDB.to_csv("MasterData.csv", encoding='utf-8', index=False)
        upload_to_aws("MasterData.csv", AssetsFolder)

        dfMasterData = pullMasterdata()
        dfMetadataDB = pullMetaDB()

        return u'''Database "{}" has been successfully uploaded.'''.format(new_dbinfo.db_name)

    except Exception as e:
        print(e)
        return 'Error uploading database'



@app.callback(dash.dependencies.Output('upload-output', 'children'),
              [dash.dependencies.Input('upload-data', 'contents')],
              [dash.dependencies.State('upload-data', 'filename')])
def update_uploaded_file(contents, filename):
    if contents is not None:
        return html.Div([
            html.H6(filename),
        ])


@app.callback(
    dash.dependencies.Output('upload-msg', 'children'),
    [dash.dependencies.Input('upload-button', 'n_clicks'),
     dash.dependencies.Input('upload-data', 'contents'),
     dash.dependencies.Input('upload-data', 'filename')],
    [dash.dependencies.State('db-name', 'value'),
     dash.dependencies.State('uploader-Name', 'value'),
     dash.dependencies.State('user-inst', 'value'),
     dash.dependencies.State('publication-url', 'value'),
     dash.dependencies.State('field-method-report-url', 'value'),
     dash.dependencies.State('lab-method-report-url', 'value'),
     dash.dependencies.State('qaqc-url', 'value'),
     dash.dependencies.State('full-qaqc-url', 'value'),
     dash.dependencies.State('substrate-option', 'value'),
     dash.dependencies.State('sample-type-option', 'value'),
     dash.dependencies.State('field-method-option', 'value'),
     dash.dependencies.State('microcystin-method', 'value'),
     dash.dependencies.State('filter-size', 'value'),
     dash.dependencies.State('cell-count-url', 'value'),
     dash.dependencies.State('ancillary-data', 'value'),
     dash.dependencies.State('is-data-reviewed', 'value'),
     dash.dependencies.State('is-field-method-reported', 'value'),
     dash.dependencies.State('is-qaqc-available', 'value'),
     dash.dependencies.State('is-full-qaqc-available', 'value'),
     dash.dependencies.State('sample-filtered', 'value'),
     dash.dependencies.State('is-lab-method bui-reported', 'value'),
     ])
def upload_file(n_clicks, contents, filename, dbname, username, userinst,  publicationURL, fieldMURL, labMURL, QAQCUrl,
                fullQAQCUrl, substrate, sampleType, fieldMethod, microcystinMethod, filterSize, cellCountURL,
                ancillaryURL, publishYN, fMYN, qaqc, fullqaqc, filt, labMethod):
    if n_clicks != None and n_clicks > 0:
        if username == None or not username.strip():
            return 'Name field cannot be empty.'
        elif userinst == None or not userinst.strip():
            return 'Institution cannot be empty.'
        elif dbname == None or not dbname.strip():
            return 'Database name cannot be empty.'
        elif contents is None:
            return 'Please select a file.'
        else:
            new_db = db_info(dbname, username, userinst)
            new_db.institution = userinst
            new_db.db_publication_url = publicationURL
            new_db.db_field_method_url = fieldMURL
            new_db.db_lab_method_url = labMURL
            new_db.db_QAQC_url = QAQCUrl
            new_db.db_full_QAQC_url = fullQAQCUrl
            new_db.db_substrate = substrate
            new_db.db_sample_type = sampleType
            new_db.db_field_method = fieldMethod
            new_db.db_microcystin_method = microcystinMethod
            new_db.db_filter_size = filterSize
            new_db.db_cell_count_method = cellCountURL
            new_db.db_ancillary_url = ancillaryURL
            new_db.RefID = dfMetadataDB['RefID'].max()+1
            new_db.db_publish_YN = publishYN
            new_db.db_field_method_YN = fMYN
            new_db.db_field_method = fieldMethod
            new_db.db_qaqc = qaqc
            new_db.db_fullqaqc = fullqaqc
            new_db.db_filter = filt
            new_db.db_lab_method = labMethod
            return upload_new_database(new_db, contents, filename)




"""
Download Bar
"""

## Download Layout

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
        ['RefID', 'DB_ID', 'DB_name', 'Uploaded_by', 'Upload_date', 'Microcystin_method', 'N_lakes', 'N_samples']]
    return table_df.to_dict("rows")








dataPageTable = dbc.Container([
dash_table.DataTable(
        id='metadata_table',
        columns=[
            # the column names are seen in the UI but the id should be the same as dataframe col name
            # the DB ID column is hidden - later used to find DB pkl files in the filtering process
            # TODO: add column for field method in table
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
        # sorting=True,
        #style_table={'overflowX': 'scroll'},
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



## Download Functionality


#need to figure this out; here is old code + a new function to download desired data from S3. need to figure out concat desired data
@app.callback(
    Output('download-link', 'href'),
    [Input('export-data-button', 'n_clicks')],
    [State('metadata_table', 'derived_virtual_selected_rows'),
     State('metadata_table', 'derived_virtual_data')])
def update_data_download_link(n_clicks, derived_virtual_selected_rows, dt_rows):
    if n_clicks != None and n_clicks > 0 and derived_virtual_selected_rows is not None:
        selected_rows = [dt_rows[i] for i in derived_virtual_selected_rows]

        try:
            new_dataframe = pd.DataFrame()
            # Read in data from selected Pickle files into Pandas dataframes, and concatenate the data
            for row in selected_rows:
                rowid = row["RefID"]
                db_data = dfMasterData[dfMasterData['RefID']==rowid]
                new_dataframe = pd.concat([new_dataframe, db_data], sort=False).reset_index(drop=True)
            dff= new_dataframe
            csv_string = dff.to_csv(index=False, encoding='utf-8')
            csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
            return csv_string
        except Exception as e:
            print("EXCEPTION: ", e)




def download_s3_file(filename):
    key = "UploadedData/" + filename + ".csv"
    print(key)
    s3File = client.get_object(Bucket='gleongmabucket', Key=key)
    dfS3File = pd.read_csv(io.BytesIO(s3File['Body'].read()))
    return dfS3File