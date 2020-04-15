import base64
import os
from urllib.parse import quote as urlquote

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app
from s3References import session, client, MasterData, dfMasterData, MetadataDB, dfMetadataDB, Bucket, UploadFolder
from botocore.exceptions import ClientError, NoCredentialsError
import boto3

session =session
s3 = session.resource('s3')

#s3.meta.client.upload_file(Filename='input_file_path', Bucket='bucket_name', Key='s3_output_key')


uploadBar = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
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
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
])

@app.callback(dash.dependencies.Output('output-data-upload', 'children'),
              [dash.dependencies.Input('upload-data', 'contents')],
              [dash.dependencies.State('upload-data', 'file_name')])
def update_uploaded_file(contents, file_name):
    if contents is not None:
        with open('filename', 'rb') as data:
            s3.upload_fileobj(file_name, UploadFolder, 'test')
        #return response

















"""
uploadBar = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
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
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
])



"""




"""

@app.callback(dash.dependencies.Output('output-data-upload', 'children'),
              [dash.dependencies.Input('upload-data', 'contents')],
              [dash.dependencies.State('upload-data', 'file_name')])
def update_uploaded_file(contents, file_name):
    if contents is not None:
        object_name = file_name
        s3_client = client
        bucket=Bucket
        response = s3_client.upload_file(file_name, bucket, object_name)
        return response

@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'file_name'),
              Input('upload-data', 'bucket')])
def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    try:
        response = client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
"""




"""
@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'local_file'),
               Input('upload-data', 'bucket'),
               Input('upload-data', 's3_file')])
def upload_to_aws(local_file, bucket, s3_file):
    s3 = client
    local_file = str(local_file)
    bucket = UploadFolder
    s3_file = str(local_file)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


uploaded = upload_to_aws('local_file', 'bucket_name', 's3_file_name')



def download_file(file_name, bucket):
    Function to download a given file from an S3 bucket
    s3 = boto3.resource('s3')
    output = f"downloads/{file_name}"
    s3.Bucket(bucket).download_file(file_name, output)

    return output
"""






""""Old Code -- Hope don't need


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



def upload_new_database(new_dbinfo, contents, filename):

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
        new_df = new_df.dropna(axis=1, how='all')

        # save the pickle and csv file in the data directory
        pkldir = get_pkl_path(new_dbinfo.db_id)
        new_df.to_pickle(pkldir)

        csvdir = get_csv_path(new_dbinfo.db_id)
        new_df.to_csv(csvdir)

        # update the number of lakes and samples in db_info
        unique_lakes_list = list(new_df["Body of Water Name"].unique())
        new_dbinfo.db_num_lakes = len(unique_lakes_list)
        new_dbinfo.db_num_samples = new_df.shape[0]

        current_metadata = metadataDB
        update_metadata(new_dbinfo, current_metadata)
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
    [dash.dependencies.Input('upload-button', 'n_clicks')],
    [dash.dependencies.State('db-name', 'value'),
     dash.dependencies.State('user-name', 'value'),
     dash.dependencies.State('user-inst', 'value'),
     dash.dependencies.State('upload-data', 'contents'),
     dash.dependencies.State('upload-data', 'filename'),
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
def upload_file(n_clicks, dbname, username, userinst, contents, filename, publicationURL, fieldMURL, labMURL, QAQCUrl,
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


"""

