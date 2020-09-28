import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from app import app
from freshGraphs import tn_tp_scatter_all, choose2All, mapPlot, convert_to_json, overTimeAll, dfMasterData, df
from s3References import pullMasterdata

app.config['suppress_callback_exceptions'] = True
#app.title = "Homepage - GLEON GMA Project"



body = html.Div(
    [
        dbc.Col([
            dbc.Row(html.H3("Welcome to the Global Microcystin Aggregation Project!"), justify="center", form=True),

            dbc.Row(html.P("Below are some interactive graphs visualizing all the data that has been uploaded so far. Visit "
                       " the \'Filter Graphs\' page to apply filters to the dataset. Data can be downloaded from the \'Data\' page. Please login "
                       "to upload data. If you would like to learn more, please visit our About page or contact us via information on the Contact page.", style={"padding":"1rem", "margin":"1rem"}), justify="center", form=True),
            dbc.Row(dbc.Button("Learn More About the Project", href="/About", color="secondary", size="lg"), justify="center", form=True),], className="pretty_container twelve columns"),
        html.Div(
            [
                dbc.Col([mapPlot], className="six columns"),
                dbc.Col([tn_tp_scatter_all], className="six columns"),
                dbc.Col([choose2All], className="six columns"),
                dbc.Col([overTimeAll], className="six columns"),
            ], className="twelve columns"),
        html.Div(id='intermediate-value', style={'display': 'none'}, children=convert_to_json(df)),
    ], className="twelve columns"
)


def Homepage():
    layout = body
    app.title = "Homepage - GLEON GMA Project"
    return layout

