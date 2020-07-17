import dash_html_components as html
import dash_core_components as dcc


""""
controls (filters)
"""
# Year range definition -- change to be min/max of year from DATETIME in df??
Year_Range = [2000, 2020]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]



# Create controls - these reference definitions in controls.py
from controls import month_Controls, DB_Info, Reporting_Measures, Microcystin_Method, Field_Methods, Sample_Types, Substrate_Status, COUNTRIES, LAKES

month_Controls_options = [{'label': str(month_Controls[month_status]),
                      'value': str(month_status)}
                     for month_status in month_Controls]

Substrate_Status_options = [{'label': str(Substrate_Status[substrate_status]),
                      'value': str(substrate_status)}
                     for substrate_status in Substrate_Status]

Sample_Types_options = [{'label': str(Sample_Types[sample_types]),
                      'value': str(sample_types)}
                     for sample_types in Sample_Types]

Field_Methods_options = [{'label': str(Field_Methods[field_methods]),
                      'value': str(field_methods)}
                     for field_methods in Field_Methods]

Microcystin_Method_options = [{'label': str(Microcystin_Method[microcystin_method]),
                      'value': str(microcystin_method)}
                     for microcystin_method in Microcystin_Method]

Reporting_Measures_options = [{'label': str(Reporting_Measures[reporting_measures]),
                      'value': str(reporting_measures)}
                     for reporting_measures in Reporting_Measures]

DB_Info_options = [{'label': str(DB_Info[db_info]),
                      'value': str(db_info)}
                     for db_info in DB_Info]

lake_status_options = [{'label': str(LAKES[lake_info]),
                      'value': str(lake_info)}
                     for lake_info in LAKES]


""" 
Incomplete filters, uncomment once working
lake_status_options =




"""




""""
Database pull? should this be a diff .py that's imported?
"""


""""
Layouts
"""

# Create global chart template
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


### Layouts - filter sidebar

## Date Filters
Date_Filters = html.Div(
    [
        # Year Slider
        html.P(
            'Filter by year (or select range in histogram):',
            className="control_label"
        ),
        dcc.RangeSlider(
            id='year_slider',
            min=min(Year_Range),
            max=max(Year_Range),
            value=[2000, 2010],
            className="dcc_control"
        ),
        # Month Dropdown
        html.P(
            'Filter by month(s):',
            className="control_label"
        ),
        dcc.RadioItems(
            id='month_selector',
            options=[
                {'label': 'All ', 'value': 'all'},
                {'label': 'Customize ', 'value': 'custom'}
            ],
            value='all',
            labelStyle={'display': 'inline-block'},
            className="dcc_control"
        ),
        dcc.Dropdown(
            id='month_options',
            options=month_Controls_options,
            multi=True,
            value=list(month_Controls.keys()),
            className="dcc_control"
        ),
    ],

)

Geographic_Filters = html.Div(
    [
        # Lake Name
        html.P(
            'Filter by Lake Name: ',
            className="control_label"
        ),
        dcc.RadioItems(
            id='lake_name_selector',
            options=[
                {'label': 'All ', 'value': 'all'},
                {'label': 'Customize ', 'value': 'custom'}
            ],
            value='all',
            labelStyle={'display': 'inline-block'},
            className="dcc_control"
        ),
        dcc.Dropdown(
            id='lake_statuses',
            options=lake_status_options,
            multi=True,
            value=list(LAKES.keys()),
            className="dcc_control"
        ),
        # Country Name
        html.P(
            'Filter by Country Name: ',
            className="control_label"
        ),
        dcc.RadioItems(
            id='country_name_selector',
            options=[
                {'label': 'All ', 'value': 'all'},
                {'label': 'Customize ', 'value': 'custom'}
            ],
            value='all',
            labelStyle={'display': 'inline-block'},
            className="dcc_control"
        ),
        dcc.Dropdown(
            id='country_statuses',
            options=country_status_options,
            multi=True,
            value=list(COUNTRIES.keys()),
            className="dcc_control"
        ),
    ],
)

Method_Filters = html.Div(
    [
        # Substrate
        html.P(
            'Filter by Lake Name: ',
            className="control_label"
        ),
        dcc.RadioItems(
            id='lake_name_selector',
            options=[
                {'label': 'All ', 'value': 'all'},
                {'label': 'Customize ', 'value': 'custom'}
            ],
            value='all',
            labelStyle={'display': 'inline-block'},
            className="dcc_control"
        ),
        dcc.Dropdown(
            id='lake_statuses',
            options=lake_status_options,
            multi=True,
            value=list(LAKES.keys()),
            className="dcc_control"
        ),
        # Sample Type
        html.P(
            'Filter by Country Name: ',
            className="control_label"
        ),
        dcc.RadioItems(
            id='country_name_selector',
            options=[
                {'label': 'All ', 'value': 'all'},
                {'label': 'Customize ', 'value': 'custom'}
            ],
            value='all',
            labelStyle={'display': 'inline-block'},
            className="dcc_control"
        ),
        dcc.Dropdown(
            id='country_statuses',
            options=country_status_options,
            multi=True,
            value=list(COUNTRIES.keys()),
            className="dcc_control"
        ),
        # Field Method
        html.P(
            'Filter by Country Name: ',
            className="control_label"
        ),
        dcc.RadioItems(
            id='country_name_selector',
            options=[
                {'label': 'All ', 'value': 'all'},
                {'label': 'Customize ', 'value': 'custom'}
            ],
            value='all',
            labelStyle={'display': 'inline-block'},
            className="dcc_control"
        ),
        dcc.Dropdown(
            id='country_statuses',
            options=country_status_options,
            multi=True,
            value=list(COUNTRIES.keys()),
            className="dcc_control"
        ),
        # Microcystin Method
        html.P(
            'Filter by Country Name: ',
            className="control_label"
        ),
        dcc.RadioItems(
            id='country_name_selector',
            options=[
                {'label': 'All ', 'value': 'all'},
                {'label': 'Customize ', 'value': 'custom'}
            ],
            value='all',
            labelStyle={'display': 'inline-block'},
            className="dcc_control"
        ),
        dcc.Dropdown(
            id='country_statuses',
            options=country_status_options,
            multi=True,
            value=list(COUNTRIES.keys()),
            className="dcc_control"
        ),
    ],
)



filter_sideBar = html.Div(
    [

            html.P(
                'Filter by well status:',
                className="control_label"
            ),
            dcc.RadioItems(
                id='well_status_selector',
                options=[
                    {'label': 'All ', 'value': 'all'},
                    {'label': 'Active only ', 'value': 'active'},
                    {'label': 'Customize ', 'value': 'custom'}
                ],
                value='active',
                labelStyle={'display': 'inline-block'},
                className="dcc_control"
            ),
            dcc.Dropdown(
                id='well_statuses',
                options=well_status_options,
                multi=True,
                value=list(WELL_STATUSES.keys()),
                className="dcc_control"
            ),
            dcc.Checklist(
                id='lock_selector',
                options=[
                    {'label': 'Lock camera', 'value': 'locked'}
                ],
                values=[],
                className="dcc_control"
            ),
            html.P(
                'Filter by well type:',
                className="control_label"
            ),
            dcc.RadioItems(
                id='well_type_selector',
                options=[
                    {'label': 'All ', 'value': 'all'},
                    {'label': 'Productive only ',
                     'value': 'productive'},
                    {'label': 'Customize ', 'value': 'custom'}
                ],
                value='productive',
                labelStyle={'display': 'inline-block'},
                className="dcc_control"
            ),
            dcc.Dropdown(
                id='well_types',
                options=well_type_options,
                multi=True,
                value=list(WELL_TYPES.keys()),
                className="dcc_control"
            ),

        ],
    className="pretty_container four columns"
)







