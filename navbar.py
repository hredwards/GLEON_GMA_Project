import dash_bootstrap_components as dbc
import dash_html_components as html

"""
This is the function that pulls the nav bar. It is pulled in application.py for all pages
"""
def NavBar():
    NavBar = dbc.Nav(
        [
            dbc.Col(NavPhoto1, className="one columns"),
            dbc.Col([
                dbc.Row(NavTitle, justify="center", form=True),
                dbc.Row(NavigationLinks, justify="center", form=True),
            ], className="eight columns"),
            dbc.Col(NavPhoto2, className="one columns"),

            #dbc.Row([NavigationLinks, NavTitle], className="twelve columns"),
            #NavigationLinks,
        ],
        pills=True,
        className="navbar pretty_container twelve columns",
    )
    return NavBar

""""
This is where the Page Title and Photo are defined; this is referenced in the navigation definitions
"""
PhotoForNavBar = "https://gleon.org/sites/default/files/images/Logo1.JPG"

NavPhoto1 =html.A((html.Img(src=PhotoForNavBar)),
        href="https://gleon.org/research/projects/global-microcystin-aggregation-gma")

NavPhoto2 =html.A((html.Img(src='assets/KBSLogo.jpg')),
        href="https://biosurvey.ku.edu", style={"padding-right":"1%", "align-items":"right", "align":"right", "float":"right"})




NavTitle = html.A("GLEON GMA Project", href="/PageHomepage", style={'color':'#000066', 'font-size':'3rem', "padding-top":"1rem", "padding-bottom":"2rem"})



""""
This is where the Navigation links are defined; the only difference is which page is marked as "Active" 
"""


NavigationLinks = dbc.Row(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/Homepage", id="page-1-link", style={"color":"#000066", "font-size":"1.8rem", "padding-bottom":"0rem"})),
        dbc.NavItem(dbc.NavLink("About", href="/About", id="page-2-link", style={"color":"#000066", "font-size":"1.8rem", "padding-bottom":"0rem"})),
        dbc.NavItem(dbc.NavLink("Filter Graphs", href="/FilterData", id="page-3-link", style={"color": "#000066", "font-size": "1.8rem", "padding-bottom":"0rem"})),
        dbc.NavItem(dbc.NavLink("Data", href="/Data", id="page-4-link", style={"color":"#000066", "font-size":"1.8rem", "padding-bottom":"0rem"})),
        dbc.NavItem(dbc.NavLink("Contact", href="/Contact", id="page-5-link", style={"color":"#000066", "font-size":"1.8rem", "padding-bottom":"0rem"})),
        dbc.NavItem(dbc.NavLink("Login", href="/Login", id="page-6-link", style={"color":"#000066", "font-size":"1.8rem", "padding-bottom":"0rem"})),
    ],
    style={"color":"green", 'float':'right'},
)

NavigationLinks2 = dbc.Row(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/PageHomepage", id="page-1-link", style={"color":"#000066", "font-size":"1.8rem", "padding-bottom":"0rem"})),
        dbc.NavItem(dbc.NavLink("Filter Graphs", href="/FilterData", id="page-3-link", style={"color": "#000066", "font-size": "1.8rem", "padding-bottom":"0rem"})),
        dbc.NavItem(dbc.NavLink("Data", href="/PageData", id="page-4-link", style={"color":"#000066", "font-size":"1.8rem", "padding-bottom":"0rem"})),
        dbc.NavItem(dbc.NavLink("Contact", href="/PageContact", id="page-5-link", style={"color":"#000066", "font-size":"1.8rem", "padding-bottom":"0rem"})),
        dbc.NavItem(dbc.NavLink("Login", href="/PageLogin", id="page-6-link", style={"color":"#000066", "font-size":"1.8rem", "padding-bottom":"0rem"})),
    ],
    style={"color":"green", 'float':'right'},
)