import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html




body = dbc.Container(
    [
        dbc.Row(
            [
                html.H3("Gleon GMA Project - About"),
            ],
            form=True,
        ),
        dbc.Row(
            [
                html.H3("This will have more info as well as some pictures eventually"),
            ],
            form=True,
        ),

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
                   html.Li("Describe the occurrence and concentrations of microcystins on a global spatial scale."),
                   html.Li("Examine temporal trends of microcystin concentrations on a global scale."),
                   html.Li("Develop global predictive and forecasting models for microcystin occurrence and concentrations based on:"),
                           html.Ul(
                               children=[
                                   html.Li("TN,TP, Chl, Secchi, temperature and other widely sampled limnology variables"),
                                   html.Li("lake morphology variables such as depth, volume, surface area, etc."),
                                   html.Li("watershed variables such as land use, watershed area, and soil type"),
                                   html.Li("possibly climate conditions and weather patterns."),
                                   ],
                           ),
                   ],
                ),
               ),

           ],
           form=True,
       ),
       ],
className="mt-4",
)


def About():
    layout = html.Div([
        body
    ])
    return layout

AboutLayout = html.Div([
        body
    ])
