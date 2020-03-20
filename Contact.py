import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html



body = dbc.Container(
    [
       dbc.Row(html.H3("Welcome to the Contact Page!")),
        dbc.Row(html.P("""This would have contact info and a redirect to the about page""")),
    ],
    className="mt-4",
)



def Contact():
    layout = html.Div([
        body
    ])
    return layout
