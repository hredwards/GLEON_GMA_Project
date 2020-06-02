import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html



table_header = [
    html.Thead(html.Tr([html.Th("Name"), html.Th("Role"), html.Th("E-Mail")]))
]

row1 = html.Tr([html.Td("Dr. Ted Harris"), html.Td("GMA Project Lead"), html.Td("ted.daniel.harris@gmail.com")])
row2 = html.Tr([html.Td("Data Science Student"), html.Td("Data Scientist/Web Interface Manager"), html.Td("gleon.gma@gmail.com")])

table_body = [html.Tbody([row1, row2])]

contactsTable = dbc.Table(table_header + table_body, bordered=True)



body = html.Div(
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
                    dbc.Button("Learn More About the Project", href="/PageAbout", color="secondary", size="lg",
                               className="mr-1", style={'textAlign': 'center', "padding":"1rem"}),
                ],
                justify="center", form=True
            ),

        ], style={"padding":"3rem"}, className="pretty_container six columns offset-by-three columns"),

        dbc.Row(contactsTable, style={"padding":"2rem"}, className="pretty_container six columns offset-by-three columns"),

    ],

)



def Contact():
    layout = body
    return layout
