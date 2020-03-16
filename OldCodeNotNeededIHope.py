"""
Nav Bar is a headache
"""


def Navbar():
     navbar = dbc.NavbarSimple(
           children=[
              dbc.NavItem(dbc.NavLink("About", href="/PageAbout")),
               dbc.NavItem(dbc.NavLink("Data", href="/PageData")),
               dbc.NavItem(dbc.NavLink("Contact", href="/PageContact")),
               dbc.NavItem(dbc.NavLink("Login", href="/PageLogin")),
               dbc.NavItem(dbc.NavLink("Upload", href="/PageUpload")),
                    ],

          brand="Home",
          brand_href="/home",
          sticky="top",
        )
     return navbar

"""Get rid of the drop down or use it; leaving code for reference but may not be in initial release"""


def NewestNavbar():
    ComeOn= dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/PageHomepage")),
            dbc.NavItem(dbc.NavLink("About", href="/PageAbout")),
            dbc.NavItem(dbc.NavLink("Data", href="/PageData")),
            dbc.NavItem(dbc.NavLink("Contact", href="/PageContact")),
            dbc.NavItem(dbc.NavLink("Login", href="/PageLogin")),
            dbc.NavItem(dbc.NavLink("Upload", href="/PageUpload")),
            html.Img(src="/GLEON_Logo"),

            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Menu",
                children=[
                    dbc.DropdownMenuItem("Entry 1"),
                    dbc.DropdownMenuItem("Entry 2"),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Entry 3"),
                ],
            ),
        ],
        brand=html.Img(src="/GLEON_Logo"),
        brand_href="https://gleon.org/research/projects/global-microcystin-aggregation-gma",
        #sticky="top",
    )
    return ComeOn



def oldNewNavBar():
    oldnewNavBar = dbc.Nav(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col((html.Img(src=PhotoForNavBar, height="100px")), className='nav navbar-nav'),
                        dbc.Row(
                            children=[
                                dbc.NavItem(dbc.NavLink("Home", href="/PageHomepage")),
                                dbc.NavItem(dbc.NavLink("About", href="/PageAbout")),
                                dbc.NavItem(dbc.NavLink("Data", href="/PageData")),
                                dbc.NavItem(dbc.NavLink("Contact", href="/PageContact")),
                                dbc.NavItem(dbc.NavLink("Login", href="/PageLogin")),
                                dbc.NavItem(dbc.NavLink("Upload", href="/PageUpload")),
                            ],
                            className='nav navbar-nav navbar-right',
                        ),
                    ],
                    no_gutters=True,
                ),
                href="https://gleon.org/research/projects/global-microcystin-aggregation-gma"
            ),
        ],
        #id="header",
        #className="row",
    )
    return oldnewNavBar

def SogdGlose():
    SogdGlose = dbc.NavbarSimple(
        [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PhotoForNavBar, height='100px')),
                    dbc.Col(dbc.NavbarBrand("GLEON GMA Project", className="ml-2", href="#"))
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://gleon.org/research/projects/global-microcystin-aggregation-gma",
        ),
            NavigationLinks,
        ]
    )
    return SogdGlose





def oldNewOldNewNavBar():
    oldNewOldNewNavBar = dbc.Nav(
        html.A(
            dbc.Row(
            [
                dbc.Col(
                html.Div(
                    [
                        html.Img(src="https://gleon.org/sites/default/files/images/Logo1.JPG", className='ml-2'),
                    ]
                ),
                ),
                dbc.Row(
                html.Div(
                    [
                        html.A(html.Button("Home", id="homePage"), href="http://127.0.0.1:8050/"),
                        html.A(html.Button("About", id="aboutPage"), href="https://gleon.org/research/projects/global-microcystin-aggregation-gma", className="mr-2"),
                        html.A(html.Button("Data", id="dataPage"), href="https://gleon.org/research/projects/global-microcystin-aggregation-gma"),
                        html.A(html.Button("Contact", id="contactPage"), href="https://gleon.org/research/projects/global-microcystin-aggregation-gma"),
                        html.A(html.Button("Login", id="loginPage"), href="http://127.0.0.1:8050/login"),

                    ],
                        ),
                        ),
            ],
                    ),
                ),
                                 )
    return oldNewOldNewNavBar
