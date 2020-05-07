import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from app import app
from dash.dependencies import Input, Output

""""
body = dbc.Container(
    [
        dbc.Row(
            [
                html.H3("Gleon GMA Project - About", style={'textAlign':'center', 'vertical-align':'center'})
            ], style={'textAlign':'center', 'vertical-align':'center'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.P(
                                    "The goal of the Global Microcystin Aggregation (GMA) project is to compile a global spatial/temporal"
                                    "dataset of freshwater microcystin and associated physicochemical water quality (e.g., TN, TP, Chl, Secchi, "
                                    "temperature, etc.), lake morphology (e.g., mean depth, volume, surface area), and watershed (e.g., land use "
                                    "metrics, watershed area) data to:"
                                ),
                                html.Div(
                                    html.Ol(
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
                                    )
                                ),
                            ],
                        ),
                    ], className='seven columns'
                ),
                dbc.Col(
                            [
                                    html.Div([
                                        html.Section(id="slideshow", children=[
                                            html.Div(id="slideshow-container", children=[
                                                html.Div(id="image"),
                                                dcc.Interval(id='interval', interval=13500),
                                            ]),
                                        ]),
                                    ])
                            ], className='pretty_container four columns'
                        ),
            ],
        ),
        dbc.Row(
            [
                html.H4("If you are interested in the project or have data to contribute, please contact us!", style={'textAlign':'center'}),
            ],
            form=True,
            ),
        dbc.Row(
            [
                dbc.Button("Contact Us!", href="/PageContact", color="secondary", size="lg", className="mr-1", style={'textAlign':'center'}),
            ],
            justify="center", form=True
        ),
       ], className="ml-auto flex-nowrap mt-3 mt-md-0"
)


"""

body = html.Div(
    [
        dbc.Row(
            [
                html.Div([
                    dbc.Row(html.H3("Gleon GMA Project - About"), style={'width':'100%', 'text-align':'center'}),
                    html.P(
                                        "The goal of the Global Microcystin Aggregation (GMA) project is to compile a global spatial/temporal"
                                        "dataset of freshwater microcystin and associated physicochemical water quality (e.g., TN, TP, Chl, Secchi, "
                                        "temperature, etc.), lake morphology (e.g., mean depth, volume, surface area), and watershed (e.g., land use "
                                        "metrics, watershed area) data to:"
                                    ),
                                    html.Ol(
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
                                    ),
                                ], className='pretty_container seven columns'),
                                        html.Section(id="slideshow", children=[
                                            html.Div(id="slideshow-container", children=[
                                                html.Div(id="image"),
                                                dcc.Interval(id='interval', interval=6000),
                                            ]),
                                        ],className='pretty_container five columns')]),
        html.Div(
            [
                dbc.Row(html.H4("If you are interested in the project or have data to contribute, please contact us!", style={'textAlign':'center'})),
                dbc.Row(dbc.Button("Contact Us!", href="/PageContact", color="secondary", size="lg", className="mr-1",
                           style={'textAlign': 'center'}))

            ], className="pretty_container",
            ),
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
    layout = body
    return layout

AboutLayout = html.Div([
        body
    ])
