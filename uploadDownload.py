import base64
import os
from urllib.parse import quote as urlquote

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import uuid
import pandas as pd
import datetime
import base64
import io
from dash.dependencies import Input, Output, State
from app import app
from s3References import session, client, MasterData, dfMasterData, MetadataDB, dfMetadataDB, Bucket, UploadFolder, dfexampleSheet, AssetsFolder
from botocore.exceptions import ClientError, NoCredentialsError
import boto3
import fuzzywuzzy
from controls import month_Controls, Substrate_Status_options, Sample_Types_options, Field_Methods_options, Microcystin_Method_options, data_Review_options
from dash_reusable_components import Card, NamedSlider, NamedInlineRadioItems, HalsNamedInlineRadioItems

s3 = session.resource('s3')


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
        self.db_name = db_name
        self.uploaded_by = uploaded_by
        self.institution = institution
        self.upload_date = current_date.strftime("%Y\%m\%d")
        self.db_id = db_name.replace(" ", "_") + '_' + uploaded_by.replace(" ", "_") + '_' + current_date.strftime(
            "%Y\%m\%d")

        self.db_publication_url = ''
        self.db_field_method_url = ''
        self.db_lab_method_url = ''
        self.db_QAQC_url = ''
        self.db_full_QCQC_url = ''
        self.db_substrate = ''
        self.db_sample_type = ''
        self.db_field_method = ''
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

def update_dataframe(selected_rows):
    """
        update dataframe based on selected databases
    """
    try:
        new_dataframe = pd.DataFrame()
        # Read in data from selected Pickle files into Pandas dataframes, and concatenate the data
        for row in selected_rows:
            rowid = row["DB_ID"]
            filepath = get_csv_path(rowid)
            db_data = pd.read_csv(filepath)
            new_dataframe = pd.concat([new_dataframe, db_data], sort=False).reset_index(drop=True)

        # Ratio of Total Nitrogen to Total Phosphorus
        # This line causes a problem on certain datasets as the columns are strings instead of ints and will not divide, dataset dependent
        print(new_dataframe["Total Nitrogen (ug/L)"])
        print("Phosphorus: ", new_dataframe["Total Phosphorus (ug/L)"])
        new_dataframe["TN:TP"] = new_dataframe["Total Nitrogen (ug/L)"] / new_dataframe["Total Phosphorus (ug/L)"]
        # Ration of Microcystin to Total Chlorophyll
        new_dataframe["Microcystin:Chlorophyll a"] = new_dataframe["Microcystin (ug/L)"] / new_dataframe[
            "Total Chlorophyll a (ug/L)"]
        # Percent change of microcystin
        new_dataframe["MC Percent Change"] = new_dataframe.sort_values("DATETIME"). \
            groupby(['LONG', 'LAT'])["Microcystin (ug/L)"]. \
            apply(lambda x: x.pct_change()).fillna(0)
        return new_dataframe
    except Exception as e:
        print("EXCEPTION: ", e)





"""
Upload Bar Layout and Callbacks
"""
### Questions
uploadBar = dbc.Container(
                id="sidebar",
                children=[
                    Card(
                        [
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
                                    value='',
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
                                    value='',
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
                                    value='',
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
                                    value='',
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
                                    value='',
                                    id='full-qaqc-url',
                                    style={'display': 'none'}
                                ),

                            ]),

### Methods
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

#### Microcystin Method
                            dbc.Row([HalsNamedInlineRadioItems(
                                name="Microcystin Method",
                                id="microcystin-method",
                                options=Microcystin_Method_options,
                            ),]),

#### Filtered/Cell Count/ Ancillary
                            # Filtered
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
                            # Cell Count
                            dbc.Row(html.P('Cell count method?')),
                            dbc.Row(
                                dcc.Input(
                                    placeholder='URL Link',
                                    type='text',
                                    value='',
                                    id='cell-count-url',
                                ),
                            ),


                            # Ancillary
                            dbc.Row(html.P('Ancillary data available?')),
                            dbc.Row(
                                dcc.Textarea(
                                    id='ancillary-data',
                                    placeholder='Description of parameters or URL link'
                                ),
                            ),

                        ]),


#### Upload Button
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
                            html.Button(id='upload-button', n_clicks=0, children='Upload',
                                        style={'margin': '1rem 0rem .6rem 0rem'}
                                        ),
                            dbc.Row(html.P(id='upload-msg')),
                    ], className="page-content")

"""
Callbacks for inputs with URLs or Other Fields if "Yes"
"""
# Controls if text fields are visible based on selected options in upload questionnaire
@app.callback(
    Output('publication-url', 'style'),
    [Input('is-data-reviewed', 'value')]
)
def show_peer_review_url(is_peer_reviewed):
    if is_peer_reviewed == 'is':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('field-method-report-url', 'style'),
    [Input('is-field-method-reported', 'value')]
)
def show_field_method_url(is_fm_reported):
    if is_fm_reported == 'is':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('lab-method-report-url', 'style'),
    [Input('is-lab-method bui-reported', 'value')]
)
def show_lab_method_url(is_lm_reported):
    if is_lm_reported == 'is':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('qaqc-url', 'style'),
    [Input('is-qaqc-available', 'value')]
)
def show_qaqc_url(is_qaqc_available):
    if is_qaqc_available == 'is':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('full-qaqc-url', 'style'),
    [Input('is-full-qaqc-available', 'value')]
)
def show_full_qaqc_url(is_full_qaqc_available):
    if is_full_qaqc_available == 'is':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    dash.dependencies.Output('filter-size', 'style'),
    [dash.dependencies.Input('sample-filtered', 'value')]
)
def show_filter_size(visibility_state):
    if visibility_state == 'is':
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
                                 'DB_name': [new_dbinfo.db_name],
                                 'Uploaded_by': [new_dbinfo.uploaded_by],
                                 'Upload_date': [new_dbinfo.upload_date],
                                 'Published_url': [new_dbinfo.db_publication_url],  # url
                                 'Field_method_url': [new_dbinfo.db_field_method_url],  # url
                                 'Lab_method_url': [new_dbinfo.db_lab_method_url],  # url
                                 'QA_QC_url': [new_dbinfo.db_QAQC_url],  # url
                                 'Full_QA_QC_url': [new_dbinfo.db_full_QCQC_url],  # url
                                 'Substrate': [new_dbinfo.db_substrate],
                                 'Sample_type': [new_dbinfo.db_sample_type],
                                 'Field-method': [new_dbinfo.db_field_method],
                                 'Microcystin_method': [new_dbinfo.db_microcystin_method],
                                 'Filter_size': [new_dbinfo.db_filter_size],
                                 'Cell_count_method': [new_dbinfo.db_cell_count_method],
                                 'Ancillary_data': [new_dbinfo.db_ancillary_url],
                                 'N_lakes': [new_dbinfo.db_num_lakes],
                                 'N_samples': [new_dbinfo.db_num_samples]})

        metadataDB = pd.concat([dfMetadataDB, new_dbdf], sort=False).reset_index(drop=True)
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

    try:

        # delete the extra composite section of the lake names - if they have any
        new_df['LakeName'] = new_df['LakeName']. \
            str.replace(r"[-]?.COMPOSITE(.*)", "", regex=True). \
            str.strip()

        new_df['Date'] = pd.to_datetime(new_df['Date']).dt.strftime('%Y-%m-%d %H:%M:%S')
        print(new_df['LakeName'])
        # convert mg to ug
        new_df['TP_mgL'] *= 1000
        new_df['TN_mgL'] *= 1000

        # format all column names
        new_df.rename(columns={'Date': 'DATETIME',
                               'LakeName': 'Body of Water Name',
                               'Lat': 'LAT',
                               'Long': 'LONG',
                               'Altitude_m': 'Altitude (m)',
                               'MaximumDepth_m': 'Maximum Depth (m)',
                               'MeanDepth_m': 'Mean Depth (m)',
                               'SecchiDepth_m': 'Secchi Depth (m)',
                               'SamplingDepth_m': 'Sampling Depth (m)',
                               'ThermoclineDepth_m': 'Thermocline Depth (m)',
                               'SurfaceTemperature_C': 'Surface Temperature (degrees celsius)',
                               'EpilimneticTemperature_C': 'Epilimnetic Temperature (degrees celsius)',
                               'TP_mgL': 'Total Phosphorus (ug/L)',
                               'TN_mgL': 'Total Nitrogen (ug/L)',
                               'NO3NO2_mgL': 'NO3 NO2 (mg/L)',
                               'NH4_mgL': 'NH4 (mg/L)',
                               'PO4_ugL': 'PO4 (ug/L)',
                               'Chlorophylla_ugL': 'Total Chlorophyll a (ug/L)',
                               'Chlorophyllb_ugL': 'Total Chlorophyll b (ug/L)',
                               'Zeaxanthin_ugL': 'Zeaxanthin (ug/L)',
                               'Diadinoxanthin_ugL': 'Diadinoxanthin (ug/L)',
                               'Fucoxanthin_ugL': 'Fucoxanthin (ug/L)',
                               'Diatoxanthin_ugL': 'Diatoxanthin (ug/L)',
                               'Alloxanthin_ugL': 'Alloxanthin (ug/L)',
                               'Peridinin_ugL': 'Peridinin (ug/L)',
                               'Chlorophyllc2_ugL': 'Total Chlorophyll c2 (ug/L)',
                               'Echinenone_ugL': 'Echinenone (ug/L)',
                               'Lutein_ugL': 'Lutein (ug/L)',
                               'Violaxanthin_ugL': 'Violaxanthin (ug/L)',
                               'TotalMC_ug/L': 'Microcystin (ug/L)',
                               'DissolvedMC_ugL': 'DissolvedMC (ug/L)',
                               'MC_YR_ugL': 'Microcystin YR (ug/L)',
                               'MC_dmRR_ugL': 'Microcystin dmRR (ug/L)',
                               'MC_RR_ugL': 'Microcystin RR (ug/L)',
                               'MC_dmLR_ugL': 'Microcystin dmLR (ug/L)',
                               'MC_LR_ugL': 'Microcystin LR (ug/L)',
                               'MC_LY_ugL': 'Microcystin LY (ug/L)',
                               'MC_LW_ugL': 'Microcystin LW (ug/L)',
                               'MC_LF_ugL': 'Microcystin LF (ug/L)',
                               'NOD_ugL': 'Nodularin (ug/L)',
                               'CYN_ugL': 'Cytotoxin Cylindrospermopsin (ug/L)',
                               'ATX_ugL': 'Neurotoxin Anatoxin-a (ug/L)',
                               'GEO_ugL': 'Geosmin (ug/L)',
                               '2MIB_ngL': '2-MIB (ng/L)',
                               'TotalPhyto_CellsmL': 'Phytoplankton (Cells/mL)',
                               'Cyano_CellsmL': 'Cyanobacteria (Cells/mL)',
                               'PercentCyano': 'Relative Cyanobacterial Abundance (percent)',
                               'DominantBloomGenera': 'Dominant Bloom',
                               'mcyD_genemL': 'mcyD gene (gene/mL)',
                               'mcyE_genemL': 'mcyE gene (gene/mL)', },
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
     dash.dependencies.State('ancillary-data', 'value')])
def upload_file(n_clicks, contents, filename, dbname, username, userinst,  publicationURL, fieldMURL, labMURL, QAQCUrl,
                fullQAQCUrl, substrate, sampleType, fieldMethod, microcystinMethod, filterSize, cellCountURL,
                ancillaryURL):
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

            return upload_new_database(new_db, contents, filename)





@app.callback(
    dash.dependencies.Output('download-link', 'href'),
    [dash.dependencies.Input('export-data-button', 'n_clicks')],
    [dash.dependencies.State('metadata_table', 'derived_virtual_selected_rows'),
     dash.dependencies.State('metadata_table', 'derived_virtual_data')])
def update_data_download_link(n_clicks, derived_virtual_selected_rows, dt_rows):
    if n_clicks != None and n_clicks > 0 and derived_virtual_selected_rows is not None:
        selected_rows = [dt_rows[i] for i in derived_virtual_selected_rows]
        dff = update_dataframe(selected_rows)

        csv_string = dff.to_csv(index=False, encoding='utf-8')
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string


















"""
def update_metadata(new_dbinfo):
    try:
        new_dbdf = pd.DataFrame({'DB_ID': [new_dbinfo.db_id],
                                 'DB_name': [new_dbinfo.db_name],
                                 'Uploaded_by': [new_dbinfo.uploaded_by],
                                 'Upload_date': [new_dbinfo.upload_date],
                                 'Published_url': [new_dbinfo.db_publication_url],  # url
                                 'Field_method_url': [new_dbinfo.db_field_method_url],  # url
                                 'Lab_method_url': [new_dbinfo.db_lab_method_url],  # url
                                 'QA_QC_url': [new_dbinfo.db_QAQC_url],  # url
                                 'Full_QA_QC_url': [new_dbinfo.db_full_QCQC_url],  # url
                                 'Substrate': [new_dbinfo.db_substrate],
                                 'Sample_type': [new_dbinfo.db_sample_type],
                                 'Field-method': [new_dbinfo.db_field_method],
                                 'Microcystin_method': [new_dbinfo.db_microcystin_method],
                                 'Filter_size': [new_dbinfo.db_filter_size],
                                 'Cell_count_method': [new_dbinfo.db_cell_count_method],
                                 'Ancillary_data': [new_dbinfo.db_ancillary_url],
                                 'N_lakes': [new_dbinfo.db_num_lakes],
                                 'N_samples': [new_dbinfo.db_num_samples]})

        metadataDB = pd.concat([dfMetadataDB, new_dbdf], sort=False).reset_index(drop=True)
        metadataDB.to_csv("MetadataDB.csv", encoding='utf-8', index=False)
        filename = str("MetadataDB.csv")

        return upload_to_aws(filename, AssetsFolder)

    except Exception as e:
        print(e)
        return 'Error saving metadata'
        
# Upload to the Uploaded Data Bucket in S3 upon upload
def upload_to_aws(filename, objectName):
    s3 = client
    objectName = objectName+str(filename)

    try:
        s3.upload_file(filename, Bucket, objectName)
        update_metadata(filename, AssetsFolder)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

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
    [Input('upload-button', 'n_clicks'),
     dash.dependencies.Input('upload-data', 'contents'),
     dash.dependencies.Input('upload-data', 'filename')],
    [dash.dependencies.State('db-name', 'value')])
def upload_file(n_clicks, contents, filename, dbname):
    if n_clicks != None and n_clicks > 0:
        if dbname == None or not dbname.strip():
            return 'Database name cannot be empty.'
        elif contents is None:
            return 'Please select a file.'
        else:
            dbname = str(dbname)
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)

            try:
                if 'csv' in filename or 'xls' in filename:
                    # Assume that the user uploaded a CSV file
                    filename = str(filename)
                    return upload_to_aws(filename, UploadFolder)

                else:
                    return 'Invalid file type.'
            except Exception as e:
                print(e)
                return 'There was an error processing this file.'



## Append new data to the master set








"""










"""
This was working but didn't take in metadata

def upload_to_aws(filename):
    s3 = client
    objectName = uploadBucket+str(filename)

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
    [Input('upload-button', 'n_clicks'),
     dash.dependencies.Input('upload-data', 'contents'),
     dash.dependencies.Input('upload-data', 'filename')],
    [dash.dependencies.State('db-name', 'value')])
def upload_file(n_clicks, contents, filename, dbname):
    if n_clicks != None and n_clicks > 0:
        if dbname == None or not dbname.strip():
            return 'Database name cannot be empty.'
        elif contents is None:
            return 'Please select a file.'
        else:
            dbname = str(dbname)
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)

            try:
                if 'csv' in filename or 'xls' in filename:
                    # Assume that the user uploaded a CSV file
                    filename = str(filename)
                    return upload_to_aws(filename)

                else:
                    return 'Invalid file type.'
            except Exception as e:
                print(e)
                return 'There was an error processing this file.'

"""





"""
Download Bar
"""



