import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
from OldCode import data_analysis as da
from OldCode.settings import months, metadataDB
import db_engine as db
from db_info import db_info
import urllib.parse

app = dash.Dash(__name__)
server = app.server

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}
# initial data frame
empty_df = pd.DataFrame()

df1 = pd.read_csv("https://raw.githubusercontent.com/divyachandran-ds/dash1/master/Energy2.csv")
df = df1.dropna()


def convert_to_json(current_dataframe):
    '''
        converts all the data to a JSON string
    '''
    jsonStr = current_dataframe.to_json(orient='split')
    return jsonStr


def convert_to_df(jsonified_data):
    '''
        converts the JSON string back to a dataframe
    '''
    jsonStr = r'{}'.format(jsonified_data)
    dff = pd.read_json(jsonStr, orient='split')
    return dff


def get_metadata_table_content(current_metadata):
    '''
        returns the data for the specified columns of the metadata data table
    '''

    table_df = current_metadata[
        ['DB_ID', 'DB_name', 'Uploaded_by', 'Upload_date', 'Microcystin_method', 'N_lakes', 'N_samples']]
    return table_df.to_dict("rows")


# Website layout HTML code
app.layout = html.Div(children=[
    html.Div([
        html.H1(children='GLEON MC Data Analysis')
    ], className="title"),

    html.Div([
        html.Details([
            html.Summary('Upload New Data'),
            html.Div(children=[
                html.H4('How to Upload Data'),
                html.P('1. Download the outline file below and copy the appropriate data into the csv file.'),
                html.P(
                    '2. Fill out the metadata questionnaire below with appropriate information and links as needed.'),
                html.P('3. Select or drag and drop the filled out csv file containing your data.'),
                html.P('4. Click \'Upload\' to upload your data and information to the project.'),
                # TODO: datasheet outline is required for db to parse data correctly from spreadsheet, need to make this clearer to
                # users when we go live
                html.A('Download Datasheet Outline File',
                       id='example-outline-link',
                       href='assets/GLEON_GMA_Example.xlsx',
                       target='_blank',
                       download='GLEON_GMA_Example.xlsx')
            ], className="row"),

            # Upload New Data questionnaire
            html.Div(children=[
                html.Div([
                    html.Div([
                        html.P('Name'),
                        dcc.Input(id='user-name', type='text'),
                    ], className='one-third column'),
                    html.Div([
                        html.P('Institution'),
                        dcc.Input(id='user-inst', type='text'),
                    ], className='one-third column'),
                    html.Div([
                        html.P('Database Name'),
                        dcc.Input(id='db-name', type='text')
                    ], className='one-third column'),
                ], className="row"),

                html.P('Is the data peer reviewed or published?'),
                dcc.RadioItems(
                    id="is-data-reviewed",
                    options=[{'label': 'Yes', 'value': 'is-reviewed'},
                             {'label': 'No', 'value': 'not-reviewed'}],
                ),
                # if answered yes, URL link field appears for user to submit an appropriate link
                dcc.Input(
                    placeholder='URL Link',
                    type='text',
                    value='',
                    id='publication-url',
                    style={'display': 'none'}
                ),
                html.P('Is the field method reported?'),
                dcc.RadioItems(
                    id="is-field-method-reported",
                    options=[{'label': 'Yes', 'value': 'fm-reported'},
                             {'label': 'No', 'value': 'fm-not-reported'}],
                ),
                dcc.Input(
                    placeholder='URL Link',
                    type='text',
                    value='',
                    id='field-method-report-url',
                    style={'display': 'none'}
                ),
                html.P('Is the lab method reported?'),
                dcc.RadioItems(
                    id="is-lab-method bui-reported",
                    options=[{'label': 'Yes', 'value': 'lm-reported'},
                             {'label': 'No', 'value': 'lm-not-reported'}],
                ),
                dcc.Input(
                    placeholder='URL Link',
                    type='text',
                    value='',
                    id='lab-method-report-url',
                    style={'display': 'none'}
                ),
                html.P('Is the QA/QC data available?'),
                dcc.RadioItems(
                    id="is-qaqc-available",
                    options=[{'label': 'Yes', 'value': 'qaqc-available'},
                             {'label': 'No', 'value': 'qaqc-not-available'}],
                ),
                dcc.Input(
                    placeholder='URL Link',
                    type='text',
                    value='',
                    id='qaqc-url',
                    style={'display': 'none'}
                ),
                html.P('Is the full QA/QC data available upon request?'),
                dcc.RadioItems(
                    id="is-full-qaqc-available",
                    options=[{'label': 'Yes', 'value': 'full-qaqc-available'},
                             {'label': 'No', 'value': 'full-qaqc-not-available'}],
                ),
                dcc.Input(
                    placeholder='URL Link',
                    type='text',
                    value='',
                    id='full-qaqc-url',
                    style={'display': 'none'}
                ),

                html.P('Substrate'),
                dcc.Dropdown(
                    id='substrate-option',
                    multi=False,
                    options=[{'label': 'Planktonic', 'value': 'planktonic'},
                             {'label': 'Beach', 'value': 'beach'},
                             {'label': 'Periphyton', 'value': 'periphyton'}],
                    style={
                        'margin': '0 60px 0 0',
                        'width': '95%'
                    }
                ),
                html.P('Sample Types'),
                dcc.Dropdown(
                    id='sample-type-option',
                    multi=False,
                    options=[{'label': 'Routine Monitoring', 'value': 'routine-monitoring'},
                             {'label': 'Reactionary Water Column', 'value': 'reactionary-water-column'},
                             {'label': 'Scum Focused', 'value': 'scum-focused'}],
                    style={
                        'margin': '0 60px 0 0',
                        'width': '95%'
                    }
                ),
                html.P('Field Methods'),
                dcc.Dropdown(
                    id='field-method-option',
                    multi=False,
                    options=[{'label': 'Vertically Integrated Sample', 'value': 'vertically-integrated'},
                             {'label': 'Discrete Depth Sample', 'value': 'discrete-depth'},
                             {'label': 'Spatially Integrated Sample', 'value': 'spatially-integrated'}],
                    style={
                        'margin': '0 60px 10px 0',
                        'width': '95%'
                    }
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
                html.P('Microcystin Method'),
                dcc.Dropdown(
                    id='microcystin-method',
                    multi=False,
                    options=[
                        {'label': 'PPIA', 'value': 'PPIA'},
                        {'label': 'ELISA', 'value': 'ELISA'},
                        {'label': 'LC-MSMS', 'value': 'LC-MSMS'}
                    ],
                    style={
                        'margin': '0 60px 0 0',
                        'width': '95%'
                    }
                ),
                html.P('Was Sample Filtered?'),
                dcc.RadioItems(
                    id="sample-filtered",
                    options=[{'label': 'Yes', 'value': 'is-filtered'},
                             {'label': 'No', 'value': 'not-filtered'}]
                ),
                dcc.Input(
                    placeholder='Filter Size (μm)',
                    type='text',
                    id='filter-size',
                    style={'display': 'none'}
                ),
                html.P('Cell count method?'),
                dcc.Input(
                    placeholder='URL Link',
                    type='text',
                    value='',
                    id='cell-count-url',
                ),
                html.P('Ancillary data available?'),
                dcc.Textarea(
                    id='ancillary-data',
                    placeholder='Description of parameters or URL link'
                ),

                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Database File')
                    ]),
                    style={
                        'width': '90%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '25px 0 0 0',
                    },
                    # allow single file upload
                    multiple=False
                ),
                html.Div(id='upload-output'),
                html.Button(id='upload-button', n_clicks=0, children='Upload',
                            style={
                                'margin': '15px 0px 10px 0px'
                            }
                            ),
                html.P(id='upload-msg'),
            ], className="row p"),
        ]),
    ], className="row"),

    html.Button(id='refresh-db-button', children='Refresh',
                style={
                    'margin': '10px 0px 10px 0px'
                }
                ),

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
        data=get_metadata_table_content(metadataDB),
        row_selectable='multi',
        selected_rows=[],
        style_as_list_view=True,
        # sorting=True,
        style_table={'overflowX': 'scroll'},
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
    ),

    html.Button(id='apply-filters-button', children='Filter Data',
                style={
                    'margin': '10px 0px 10px 0px'
                }
                ),
    # Export the selected datasets in a single csv file
    html.A(html.Button(id='export-data-button', children='Download Filtered Data',
                       style={
                           'margin': '10px 0px 10px 10px'
                       }),
           href='',
           id='download-link',
           download='data.csv',
           target='_blank'
           ),
    # Geographical world map showing concentration locations
    html.Div([
        html.H2('Microcystin Concentration'),
        dcc.Graph(id='geo_plot'),
        html.Div([
            dcc.RadioItems(
                id="geo_plot_option",
                options=[{'label': 'Show Concentration Plot', 'value': 'CONC'},
                         {'label': 'Show Log Concentration Change Plot', 'value': 'LOG'}],
                value='CONC'),
        ]),
        html.Div([
            html.Div(html.P("Year:")),
            html.Div(
                dcc.Dropdown(
                    id='year-dropdown',
                    multi=True
                ),
            )
        ]),
        html.Div([
            html.P("Month:"),
            dcc.RangeSlider(
                id='month-slider',
                min=0,
                max=11,
                value=[0, 11],
                # included=False,
                marks={i: months[i] for i in range(len(months))}
            )
        ]),
    ], className="row"),

    html.Div([
        html.H2('Raw Data'),
        dcc.Graph(
            id="temporal-raw-scatter",
        ),
        html.Div([
            html.Div([
                html.P("Y-Axis Range"),
                dcc.RangeSlider(
                    id="axis_range_raw",
                    min=0,
                    step=0.5,
                    marks={
                        1: '1',
                        100: '100',
                        1000: '1000',
                        10000: '10000'},
                ),
            ], style={'marginBottom': 30}),
        ]),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id="temporal-raw-col"
                )], className='six columns'),
            html.Div([
                dcc.RadioItems(
                    id="temporal-raw-option",
                    options=[{'label': 'Show All Raw Data', 'value': 'RAW'},
                             {'label': 'Apply Log10 to Raw Data', 'value': 'LOG'},
                             {'label': 'Show Data Within 3 Standard Deviations', 'value': '3SD'}],
                    value='RAW')
            ], className='six columns'),
        ])
    ], className='row'),

    # comparison graph between two selected categories for the selected data
    html.Div([
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
    ], className='row'),

    # INCOMPLETE: correlation matrix for a single dataset to show a heatmap of correlations (Michael will finish this)
    # html.Div([
    #     html.H2('Correlation Matrix'),
    #     dcc.Graph(id='correlation-graph'),
    #     html.Div([
    #         html.Div([
    #             html.P('Dataset'),
    #             dcc.Dropdown(
    #                 id='correlation-dropdown'),
    #             ], className='six columns')
    #         ])
    #     ], className='row'),

    html.Div([
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
        ]),
        html.Div([
            html.P("Log TP:"),
            dcc.RangeSlider(
                id="tp_range",
                min=0,
                step=0.5,
                marks={
                    1000: '1',
                    4000: '100',
                    7000: '1000',
                    10000: '10000'
                },
            ),
        ]),
    ], className="row"),

    html.Div([
        html.H2('Data Trends by Lake'),
        html.P('Lakes require at least three data points to have a trendline', id='lake-minimum-points'),
        html.Div([
            html.Div([
                dcc.Graph(
                    id="temporal-lake-scatter",
                )
            ], className='six columns'),
            html.Div([
                dcc.Graph(
                    id="temporal-lake-pc-scatter",
                )
            ], className='six columns'),
        ]),
        dcc.Dropdown(
            id="temporal-lake-col",
            className='six columns'
        ),
        dcc.Dropdown(
            id='temporal-lake-location',
            className='six columns'
        )
    ], className="row"),

    html.Div([
        html.H2('Overall Temporal Data Trends'),
        html.P('Includes data from all lakes'),
        html.Div([
            html.Div([
                dcc.Graph(
                    id="temporal-avg-scatter",
                )
            ], className='six columns'),
            html.Div([
                dcc.Graph(
                    id="temporal-pc-scatter",
                )
            ], className='six columns'),
        ]),
        dcc.Dropdown(
            id="temporal-avg-col"
        )
    ], className='row'),

    # Hidden div inside the app that stores the intermediate value
    html.Div(id='intermediate-value', style={'display': 'none'}, children=convert_to_json(empty_df))
])


# Controls if text fields are visible based on selected options in upload questionnaire
@app.callback(
    dash.dependencies.Output('publication-url', 'style'),
    [dash.dependencies.Input('is-data-reviewed', 'value')]
)
def show_peer_review_url(is_peer_reviewed):
    if is_peer_reviewed == 'is-reviewed':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    dash.dependencies.Output('field-method-report-url', 'style'),
    [dash.dependencies.Input('is-field-method-reported', 'value')]
)
def show_field_method_url(is_fm_reported):
    if is_fm_reported == 'fm-reported':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    dash.dependencies.Output('lab-method-report-url', 'style'),
    [dash.dependencies.Input('is-lab-method bui-reported', 'value')]
)
def show_lab_method_url(is_lm_reported):
    if is_lm_reported == 'lm-reported':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    dash.dependencies.Output('qaqc-url', 'style'),
    [dash.dependencies.Input('is-qaqc-available', 'value')]
)
def show_qaqc_url(is_qaqc_available):
    if is_qaqc_available == 'qaqc-available':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    dash.dependencies.Output('full-qaqc-url', 'style'),
    [dash.dependencies.Input('is-full-qaqc-available', 'value')]
)
def show_full_qaqc_url(is_full_qaqc_available):
    if is_full_qaqc_available == 'full-qaqc-available':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    [dash.dependencies.Output('vertically-depth-integrated', 'style'),
     dash.dependencies.Output('discrete-depth-sampled', 'style'),
     dash.dependencies.Output('spatially-integrated-depth', 'style'),
     dash.dependencies.Output('num-spatially-integrated-samples', 'style')],
    [dash.dependencies.Input('field-method-option', 'value')])
def show_field_option_input(field_option):
    if field_option == 'vertically-integrated':
        return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}
    if field_option == 'discrete-depth':
        return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
    if field_option == 'spatially-integrated':
        return {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, {'display': 'block'}
    else:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}


@app.callback(
    dash.dependencies.Output('filter-size', 'style'),
    [dash.dependencies.Input('sample-filtered', 'value')]
)
def show_filter_size(visibility_state):
    if visibility_state == 'is-filtered':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    dash.dependencies.Output('metadata_table', 'data'),
    [dash.dependencies.Input('refresh-db-button', 'n_clicks')])
def upload_file(n_clicks):
    # read from MetadataDB to update the table
    metadataDB = pd.read_csv("../data/MetadataDB.csv")
    return get_metadata_table_content(metadataDB)


@app.callback(
    dash.dependencies.Output('geo_plot', 'figure'),
    [dash.dependencies.Input('year-dropdown', 'value'),
     dash.dependencies.Input('month-slider', 'value'),
     dash.dependencies.Input('geo_plot_option', 'value'),
     dash.dependencies.Input('intermediate-value', 'children')])
def update_geo_plot(selected_years, selected_month, geo_option, jsonified_data):
    dff = convert_to_df(jsonified_data)
    return da.geo_plot(selected_years, selected_month, geo_option, dff)


@app.callback(
    dash.dependencies.Output('comparison_scatter', 'figure'),
    [dash.dependencies.Input('compare-y-axis', 'value'),
     dash.dependencies.Input('compare-x-axis', 'value'),
     dash.dependencies.Input('intermediate-value', 'children')])
def update_comparison(selected_y, selected_x, jsonified_data):
    dff = convert_to_df(jsonified_data)
    return da.comparison_plot(selected_y, selected_x, dff)


# TODO: Correlation matrix in progress
# @app.callback(
#     dash.dependencies.Output('correlation-graph', 'figure'),
#     [dash.dependencies.Input('correlation-dropdown', 'value'),
#     dash.dependencies.Input('intermediate-value', 'children')])
# def update_correlation(selected_dataset, jsonified_data):
#     dff = convert_to_df(jsonified_data)
#     return da.correlation_plot(selected_dataset, dff)

@app.callback(
    dash.dependencies.Output('temporal-lake-scatter', 'figure'),
    [dash.dependencies.Input('temporal-lake-col', 'value'),
     dash.dependencies.Input('temporal-lake-location', 'value'),
     dash.dependencies.Input('intermediate-value', 'children')])
def update_temporal_output(selected_col, selected_loc, jsonified_data):
    dff = convert_to_df(jsonified_data)
    return da.temporal_lake(selected_col, selected_loc, 'raw', dff)


@app.callback(
    dash.dependencies.Output('temporal-lake-pc-scatter', 'figure'),
    [dash.dependencies.Input('temporal-lake-col', 'value'),
     dash.dependencies.Input('temporal-lake-location', 'value'),
     dash.dependencies.Input('intermediate-value', 'children')])
def update_output(selected_col, selected_loc, jsonified_data):
    dff = convert_to_df(jsonified_data)
    return da.temporal_lake(selected_col, selected_loc, 'pc', dff)


@app.callback(
    dash.dependencies.Output('tn_tp_scatter', 'figure'),
    [dash.dependencies.Input('tn_range', 'value'),
     dash.dependencies.Input('tp_range', 'value'),
     dash.dependencies.Input('intermediate-value', 'children')])
def update_output(tn_val, tp_val, jsonified_data):
    dff = convert_to_df(jsonified_data)
    return da.tn_tp(tn_val, tp_val, dff)


@app.callback(
    dash.dependencies.Output('temporal-avg-scatter', 'figure'),
    [dash.dependencies.Input('temporal-avg-col', 'value'),
     dash.dependencies.Input('intermediate-value', 'children')])
def update_output(selected_col, jsonified_data):
    dff = convert_to_df(jsonified_data)
    return da.temporal_overall(selected_col, 'avg', dff)


@app.callback(
    dash.dependencies.Output('temporal-pc-scatter', 'figure'),
    [dash.dependencies.Input('temporal-avg-col', 'value'),
     dash.dependencies.Input('intermediate-value', 'children')])
def update_output(selected_col, jsonified_data):
    dff = convert_to_df(jsonified_data)
    return da.temporal_overall(selected_col, 'pc', dff)


@app.callback(
    dash.dependencies.Output('temporal-raw-scatter', 'figure'),
    [dash.dependencies.Input('temporal-raw-option', 'value'),
     dash.dependencies.Input('temporal-raw-col', 'value'),
     dash.dependencies.Input('axis_range_raw', 'value'),
     dash.dependencies.Input('intermediate-value', 'children')
     ])
def update_output(selected_option, selected_col, log_range, jsonified_data):
    dff = convert_to_df(jsonified_data)
    return da.temporal_raw(selected_option, selected_col, log_range, dff)


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

            return db.upload_new_database(new_db, contents, filename)


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


# Update the download link to contain the data from the selected datasheets
@app.callback(
    dash.dependencies.Output('download-link', 'href'),
    [dash.dependencies.Input('apply-filters-button', 'n_clicks')],
    [dash.dependencies.State('metadata_table', 'derived_virtual_selected_rows'),
     dash.dependencies.State('metadata_table', 'derived_virtual_data')])
def update_data_download_link(n_clicks, derived_virtual_selected_rows, dt_rows):
    if n_clicks != None and n_clicks > 0 and derived_virtual_selected_rows is not None:
        selected_rows = [dt_rows[i] for i in derived_virtual_selected_rows]
        dff = db.update_dataframe(selected_rows)

        csv_string = dff.to_csv(index=False, encoding='utf-8')
        csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
        return csv_string


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/62f0eb4f1fadbefea64b2404493079bf848974e8/dash-uber-ride-demo.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                "https://codepen.io/chriddyp/pen/bWLwgP.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server(debug=True)
