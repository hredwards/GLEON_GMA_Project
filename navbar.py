import dash_bootstrap_components as dbc
import dash_html_components as html


"""
This is the function that pulls the nav bar. It is pulled in application.py for all pages
"""
def NavBar():
    NavBar = dbc.Nav(
        [
            NavPhoto,
            NavTitle,
            NavigationLinks,
        ],
        pills=True,
        className="navbar navbar-default",
    )
    return NavBar

""""
This is where the Page Title and Photo are defined; this is referenced in the navigation definitions
"""
PhotoForNavBar = "https://gleon.org/sites/default/files/images/Logo1.JPG"

NavPhoto =html.A(
        dbc.Row(
            [
                dbc.Col((html.Img(src=PhotoForNavBar, height="125px"))),
            ],
        ),
        href="https://gleon.org/research/projects/global-microcystin-aggregation-gma"
    )


NavTitle = dbc.Row(
    [
        html.A("GLEON GMA Project", href="/PageHomepage", style={'color':'#000066', 'font-size':'30px'}),
    ],
    className="col-4 col-offset-2",
    align="center",
    justify=True,
    no_gutters=True,
)




""""
This is where the Navigation links are defined; the only difference is which page is marked as "Active" 
"""


NavigationLinks = dbc.Row(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/PageHomepage", id="page-1-link", style={"color":"#000066", "font-size":"15px"})),
        dbc.NavItem(dbc.NavLink("About", href="/PageAbout", id="page-2-link", style={"color":"#000066", "font-size":"15px"})),
        dbc.NavItem(dbc.NavLink("Data", href="/PageData", id="page-3-link", style={"color":"#000066", "font-size":"15px"})),
        dbc.NavItem(dbc.NavLink("Contact", href="/PageContact", id="page-4-link", style={"color":"#000066", "font-size":"15px"})),
        dbc.NavItem(dbc.NavLink("Login", href="/PageLogin", id="page-5-link", style={"color":"#000066", "font-size":"15px"})),
        dbc.NavItem(dbc.NavLink("Upload", href="/PageUpload", style={"color":"#000066", "font-size":"15px"})),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    style={"color":"green"},
    align="center",
    justify=True,
)

