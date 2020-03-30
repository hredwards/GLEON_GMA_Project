import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html



table_header = [
    html.Thead(html.Tr([html.Th("Name"), html.Th("Role"), html.Th("E-Mail")]))
]

row1 = html.Tr([html.Td("Dr. Ted Harris"), html.Td("Dent"), html.Td("Dent")])
row2 = html.Tr([html.Td("Ford"), html.Td("Prefect")])
row3 = html.Tr([html.Td("Zaphod"), html.Td("Beeblebrox")])
row4 = html.Tr([html.Td("Trillian"), html.Td("Astra")])

table_body = [html.Tbody([row1, row2, row3, row4])]

table = dbc.Table(table_header + table_body, bordered=True)
contacts = dbc.Table()



body = dbc.Container(
    [
       dbc.Row(html.H3("Welcome to the Contact Page!")),
        dbc.Row(html.P("")),
        dbc.Row(
            [
                dbc.Button("Learn More About the Project", href="/PageAbout", color="secondary"),
            ],
            justify="center", form=True
        ),
        dbc.Row(html.table),
    ],
    className="mt-4",
)



def Contact():
    layout = html.Div([
        body
    ])
    return layout
