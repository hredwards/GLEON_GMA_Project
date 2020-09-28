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



"""
Old code for logins

"""


"""
Register Account
"""

registration_form = dbc.Row([
    html.Form([
        dcc.Input(placeholder='username', name='username', type='text'),
        dcc.Input(placeholder='password', name='password', type='password'),
        html.Button('Login', type='submit')
    ], action='/register', method='post')
], justify="center", form=True,   className="twelve columns",
)


register = html.Div([
    dbc.Row(html.H3("Welcome to the Login Page!"), justify="center", form=True, className="twelve columns"),
    html.Div(id='custom-auth-frame'),
    html.Div(id='custom-auth-frame-1', style={'textAlign': 'right', "background": "black"}),
    registration_form,
    dbc.Row(dbc.Button("Want a login?", href="/Contact", color="secondary", style={"margin":"2rem"}), justify="center", form=True),
], className="pretty_container four columns offset-by-four columns",
)


def Register():
    layout = register
    return layout

"""
Login to existing Account
loginExisting = html.Div([
    dbc.Row(html.H3("Welcome to the Login Page!"), justify="center", form=True, className="twelve columns"),
    html.Div(id='custom-auth-frame'),
    html.Div(id='custom-auth-frame-1', style={'textAlign': 'right', "background": "black"}),
    login_form,
    dbc.Row(dbc.Button("Want a login?", href="/Contact", color="secondary", style={"margin":"2rem"}), justify="center", form=True),
], className="pretty_container four columns offset-by-four columns",
)


def LoginExisting():
    layout = loginExisting
    return layout


"""


"""
Login


# Create a login route
_app_route = '/Upload'

@app.server.route('/login', methods=['POST'])
def route_login():
    data = flask.request.form
    username = data.get('username')
    password = data.get('password')

    if username not in creds.keys() or  creds[username] != password:
        return flask.redirect('/Login')
    else:

        # Return a redirect with
        rep = flask.redirect(_app_route)
        rep.set_cookie('custom-auth-session', username)
        return rep


login_form = dbc.Row([
    html.Form([
        dcc.Input(placeholder='username', name='username', type='text'),
        dcc.Input(placeholder='password', name='password', type='password'),
        html.Button('Login', type='submit')
    ], action='/login', method='post')
], justify="center", form=True,   className="twelve columns",
)


login = html.Div([
    dbc.Row(html.H3("Welcome to the Login Page!"), justify="center", form=True, className="twelve columns"),
    html.Div(id='custom-auth-frame'),
    html.Div(id='custom-auth-frame-1', style={'textAlign': 'right', "background": "black"}),
    login_form,
    dbc.Row(dbc.Button("Want a login?", href="/Contact", color="secondary", style={"margin":"2rem"}), justify="center", form=True),
], className="pretty_container four columns offset-by-four columns",
)


def Login():
    layout = login
    return layout

"""


"""
Filtered View

filtView = html.Div(
    [
        #summaryboxes,
        html.Div(
            [
                dbc.Col([filtersAvailable], className="three columns"),
                dbc.Col([mapPlotFiltered], className="five columns"),
                dbc.Col([tn_tp_scatter_filter], className="four columns"),
                dbc.Col([overTimeFiltered], className="five columns"),
                dbc.Col([choose2Filtered], className="four columns"),

            ], className="twelve columns"),

        html.Div(id='intermediate-value', style={'display': 'none'}, children=convert_to_json(dfMasterData)),
    ], id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    },
    className="twelve columns",
)


def FilteredView():
    layout = filtView
    return layout

"""







"""
From login with sessions
"""

"""
UserPage 

@app.server.route('/UserPage')
def get_metadata_table_content_User_SpecificTest():
    with app.app_context():
        table_df = dfMetadataDB[
                ['RefID', 'DB_ID', 'DB_name', 'Uploaded_by', 'Upload_date', 'PWYN', 'Microcystin_method', 'N_lakes',
                 'N_samples']]
        table_refid = table_df["RefID"]
        table_df = table_df[table_refid == session['user_id']]
        table_df = table_df.to_dict("rows")



        userPageTable = dbc.Container([
            dbc.Row(html.P(
                "Welcome, NAME. Here you can download any file that you have uploaded to our collection.",
                style={'textAlign': 'center'}),
                justify="center", form=True),

            dash_table.DataTable(
                id='metadata_table_userPage',
                columns=[
                    # {'name': 'Reference ID', 'id': 'RefID', 'hidden': True},
                    # {'name': 'Database ID', 'id': 'DB_ID', 'hidden': True},
                    {'name': 'Database Name', 'id': 'DB_name'},
                    {'name': 'Uploaded By', 'id': 'Uploaded_by'},
                    {'name': 'Upload Date', 'id': 'Upload_date'},
                    {'name': 'Microcystin Method', 'id': 'Microcystin_method'},
                    {'name': 'Number of Lakes', 'id': 'N_lakes'},
                    {'name': 'Number of Samples', 'id': 'N_samples'}, ],
                data=table_df,
                row_selectable='multi',
                selected_rows=[],
                style_as_list_view=True,
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                },
            ),

            dbc.Row(html.P(
                "Select as many as you'd like, the one file you download will contain all entries from selected sets.",
                style={'textAlign': 'center', 'margin': '2rem 0rem 0rem 0rem'}),
                justify="center", form=True),

            # Export the selected datasets in a single csv file
            dbc.Row(html.A(html.Button(id='export-data-button', children='Download Selected Data',
                                       style={
                                           'margin': '1rem 0px 1rem 1rem'
                                       }),
                           href='',
                           id='download-link-UserSpecific',
                           download='data.csv',
                           target='_blank'
                           ), justify="center", form=True)
        ], style={"max-width": "90%"}, )





    dataPageUserSpecific = html.Div(
        [
            html.Div(
                [
                    dbc.Row(html.H3("Download Available Datasets"), justify="center", form=True),
                    dbc.Row(userPageTable, justify="center", form=True)
                ],
                className="pretty_container ten columns offset-by-one column"),

        ],
        className="ten columns offset-by-one column")
    layout = dataPageUserSpecific
    return layout




"""

"""
session for user_id isn't iterable?

@app.server.route('/UserPage')
def get_metadata_table_content_User_SpecificTest():
    #with app.app_context():
        table_df = dfMetadataDB[
                ['RefID', 'DB_ID', 'DB_name', 'Uploaded_by', 'Upload_date', 'PWYN', 'Microcystin_method', 'N_lakes',
                 'N_samples']]

        if session.get('user_id', 0) != 0:
            table_refid = table_df["RefID"]
            table_df = table_df[table_refid == g.user_id]

        table_df = table_df.to_dict("rows")



        userPageTable = dbc.Container([
            dbc.Row(html.P(
                "Welcome, NAME. Here you can download any file that you have uploaded to our collection.",
                style={'textAlign': 'center'}),
                justify="center", form=True),

            dash_table.DataTable(
                id='metadata_table_userPage',
                columns=[
                    # {'name': 'Reference ID', 'id': 'RefID', 'hidden': True},
                    # {'name': 'Database ID', 'id': 'DB_ID', 'hidden': True},
                    {'name': 'Database Name', 'id': 'DB_name'},
                    {'name': 'Uploaded By', 'id': 'Uploaded_by'},
                    {'name': 'Upload Date', 'id': 'Upload_date'},
                    {'name': 'Microcystin Method', 'id': 'Microcystin_method'},
                    {'name': 'Number of Lakes', 'id': 'N_lakes'},
                    {'name': 'Number of Samples', 'id': 'N_samples'}, ],
                data=table_df,
                row_selectable='multi',
                selected_rows=[],
                style_as_list_view=True,
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                },
            ),

            dbc.Row(html.P(
                "Select as many as you'd like, the one file you download will contain all entries from selected sets.",
                style={'textAlign': 'center', 'margin': '2rem 0rem 0rem 0rem'}),
                justify="center", form=True),

            # Export the selected datasets in a single csv file
            dbc.Row(html.A(html.Button(id='export-data-button', children='Download Selected Data',
                                       style={
                                           'margin': '1rem 0px 1rem 1rem'
                                       }),
                           href='',
                           id='download-link-UserSpecific',
                           download='data.csv',
                           target='_blank'
                           ), justify="center", form=True)
        ], style={"max-width": "90%"}, )

        dataPageUserSpecific = html.Div(
            [
                html.Div(
                    [
                        dbc.Row(html.H3("Download Available Datasets"), justify="center", form=True),
                        dbc.Row(userPageTable, justify="center", form=True)
                    ],
                    className="pretty_container ten columns offset-by-one column"),

            ],
            className="ten columns offset-by-one column")

        layout = dataPageUserSpecific
        return layout


"""

""" THis one is kinda working except it doesnt reroute to the user page properly
@app.server.route('/UserPage')
def get_metadata_table_content_User_SpecificTest():
    if session.get('user_id', 0) != 0:
        table_df = dfMetadataDB[
            ['RefID', 'DB_ID', 'DB_name', 'Uploaded_by', 'Upload_date', 'PWYN', 'Microcystin_method', 'N_lakes',
             'N_samples']]
        table_refid = table_df["RefID"]
        table_df = table_df[table_refid == g.user_id]
        table_df = table_df.to_dict("rows")

    else:
        table_df = pd.DataFrame()
        table_df.to_dict("rows")



    userPageTable = dbc.Container([
        dbc.Row(html.P(
            "Welcome, NAME. Here you can download any file that you have uploaded to our collection.",
            style={'textAlign': 'center'}),
            justify="center", form=True),

        dash_table.DataTable(
            id='metadata_table_userPage',
            columns=[
                # {'name': 'Reference ID', 'id': 'RefID', 'hidden': True},
                # {'name': 'Database ID', 'id': 'DB_ID', 'hidden': True},
                {'name': 'Database Name', 'id': 'DB_name'},
                {'name': 'Uploaded By', 'id': 'Uploaded_by'},
                {'name': 'Upload Date', 'id': 'Upload_date'},
                {'name': 'Microcystin Method', 'id': 'Microcystin_method'},
                {'name': 'Number of Lakes', 'id': 'N_lakes'},
                {'name': 'Number of Samples', 'id': 'N_samples'}, ],
            data=table_df,
            row_selectable='multi',
            selected_rows=[],
            style_as_list_view=True,
            style_cell={'textAlign': 'left'},
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
        ),

        dbc.Row(html.P(
            "Select as many as you'd like, the one file you download will contain all entries from selected sets.",
            style={'textAlign': 'center', 'margin': '2rem 0rem 0rem 0rem'}),
            justify="center", form=True),

        # Export the selected datasets in a single csv file
        dbc.Row(html.A(html.Button(id='export-data-button', children='Download Selected Data',
                                   style={
                                       'margin': '1rem 0px 1rem 1rem'
                                   }),
                       href='',
                       id='download-link-UserSpecific',
                       download='data.csv',
                       target='_blank'
                       ), justify="center", form=True)
    ], style={"max-width": "90%"}, )

    dataPageUserSpecific = html.Div(
        [
            html.Div(
                [
                    dbc.Row(html.H3("Download Available Datasets"), justify="center", form=True),
                    dbc.Row(userPageTable, justify="center", form=True)
                ],
                className="pretty_container ten columns offset-by-one column"),

        ],
        className="ten columns offset-by-one column")

    layout = dataPageUserSpecific
    return layout



@app.server.route('/UserPage')
def get_metadata_table_content_User_SpecificTest():
    if session.get('user_id', 0) != 0:
        table_df = dfMetadataDB[
            ['RefID', 'DB_ID', 'DB_name', 'Uploaded_by', 'Upload_date', 'PWYN', 'Microcystin_method', 'N_lakes',
             'N_samples']]
        table_refid = table_df["RefID"]
        table_df = table_df[table_refid == g.user_id]
        table_df = table_df.to_dict("rows")

    else:
        table_df = pd.DataFrame()
        table_df.to_dict("rows")



    userPageTable = dbc.Container([
        dbc.Row(html.P(
            "Welcome, NAME. Here you can download any file that you have uploaded to our collection.",
            style={'textAlign': 'center'}),
            justify="center", form=True),

        dash_table.DataTable(
            id='metadata_table_userPage',
            columns=[
                # {'name': 'Reference ID', 'id': 'RefID', 'hidden': True},
                # {'name': 'Database ID', 'id': 'DB_ID', 'hidden': True},
                {'name': 'Database Name', 'id': 'DB_name'},
                {'name': 'Uploaded By', 'id': 'Uploaded_by'},
                {'name': 'Upload Date', 'id': 'Upload_date'},
                {'name': 'Microcystin Method', 'id': 'Microcystin_method'},
                {'name': 'Number of Lakes', 'id': 'N_lakes'},
                {'name': 'Number of Samples', 'id': 'N_samples'}, ],
            data=table_df,
            row_selectable='multi',
            selected_rows=[],
            style_as_list_view=True,
            style_cell={'textAlign': 'left'},
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
        ),

        dbc.Row(html.P(
            "Select as many as you'd like, the one file you download will contain all entries from selected sets.",
            style={'textAlign': 'center', 'margin': '2rem 0rem 0rem 0rem'}),
            justify="center", form=True),

        # Export the selected datasets in a single csv file
        dbc.Row(html.A(html.Button(id='export-data-button', children='Download Selected Data',
                                   style={
                                       'margin': '1rem 0px 1rem 1rem'
                                   }),
                       href='',
                       id='download-link-UserSpecific',
                       download='data.csv',
                       target='_blank'
                       ), justify="center", form=True)
    ], style={"max-width": "90%"}, )

    dataPageUserSpecific = html.Div(
        [
            html.Div(
                [
                    dbc.Row(html.H3("Download Available Datasets"), justify="center", form=True),
                    dbc.Row(userPageTable, justify="center", form=True)
                ],
                className="pretty_container ten columns offset-by-one column"),

        ],
        className="ten columns offset-by-one column")

    layout = dataPageUserSpecific
    return layout



def get_metadata_table_content_User_Specific(current_metadata):
    '''
        returns the data for the specified columns of the metadata data table
    '''
    with app.app_context():
    table_df = current_metadata[
        ['RefID', 'DB_ID', 'DB_name', 'Uploaded_by', 'Upload_date', 'PWYN', 'Microcystin_method', 'N_lakes', 'N_samples']]
    table_refid = table_df["RefID"]
    table_df = table_df[table_refid == g.userID]

    return table_df.to_dict("rows")



userPageTable = dbc.Container([
    dbc.Row(html.P(
        "Welcome, NAME. Here you can download any file that you have uploaded to our collection.", style={'textAlign':'center'}),
        justify="center", form=True),

    dash_table.DataTable(
        id='metadata_table_userPage',
        columns=[
            #{'name': 'Reference ID', 'id': 'RefID', 'hidden': True},
            #{'name': 'Database ID', 'id': 'DB_ID', 'hidden': True},
            {'name': 'Database Name', 'id': 'DB_name'},
            {'name': 'Uploaded By', 'id': 'Uploaded_by'},
            {'name': 'Upload Date', 'id': 'Upload_date'},
            {'name': 'Microcystin Method', 'id': 'Microcystin_method'},
            {'name': 'Number of Lakes', 'id': 'N_lakes'},
            {'name': 'Number of Samples', 'id': 'N_samples'}, ],
        data=get_metadata_table_content_User_SpecificTest(dfMetadataDB),
        row_selectable='multi',
        selected_rows=[],
        style_as_list_view=True,
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
    ),

    dbc.Row(html.P(
        "Select as many as you'd like, the one file you download will contain all entries from selected sets.",
        style={'textAlign': 'center', 'margin': '2rem 0rem 0rem 0rem'}),
        justify="center", form=True),

    # Export the selected datasets in a single csv file
    dbc.Row(html.A(html.Button(id='export-data-button', children='Download Selected Data',
                       style={
                           'margin': '1rem 0px 1rem 1rem'
                       }),
           href='',
           id='download-link-UserSpecific',
           download='data.csv',
           target='_blank'
           ),justify="center", form=True)
], style={"max-width":"90%"},)


dataPageUserSpecific = html.Div(
    [
        html.Div(
            [
                dbc.Row(html.H3("Download Available Datasets"), justify="center", form=True),
                dbc.Row(userPageTable, justify="center", form=True)
            ],
            className="pretty_container ten columns offset-by-one column"),

    ],
    className="ten columns offset-by-one column")


def UserPage():
    layout = dataPageUserSpecific
    return layout


@app.server.route('/UserPage')
def get_metadata_table_content_User_SpecificTest():
    if session.get('user_id', 0) != 0:
        table_df = dfMetadataDB[
            ['RefID', 'DB_ID', 'DB_name', 'Uploaded_by', 'Upload_date', 'PWYN', 'Microcystin_method', 'N_lakes',
             'N_samples']]
        table_refid = table_df["RefID"]
        table_df = table_df[table_refid == g.user_id]
        table_df = table_df.to_dict("rows")

    else:
        table_df = pd.DataFrame()
        table_df.to_dict("rows")
"""

















"""
class User:
    def __init__(self, id, username, password, fullName):
        self.id = id
        self.username = username
        self.password = password
        self.fullName = fullName

    def __repr__(self):
        return f'<User: {self.username}>'


# Pull User Data from AWS
users = []

for index, row in dfCreds.iterrows():
    users.append(User(id=row["id"], username=row["user"], password=row["pass"], fullName=row["name"]))


@app.server.before_request
def before_request_getUser():
    session['logged_in'] = False
    g.user = None
    g.table_df = None
    g.user_fullName = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        g.user_id = user.id
        g.user_fullName = user.fullName


# Page where users enter their credentials which are checked against AWS. If successful, they are redirected to their user page
@app.server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            session['logged_in'] = True

            return redirect('/successLogin')

        return redirect('/Login')

    return redirect('/Login')


@app.server.route('/successLogin')
def profile():
    if not g.user:
        return redirect('/Login')

    return redirect('/UserPage')

@app.server.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect('/Login')


"""





"""
Log in Page 

class User:
    def __init__(self, id, username, password, fullName):
        self.id = id
        self.username = username
        self.password = password
        self.fullName = fullName

    def __repr__(self):
        return f'<User: {self.username}>'


users = []

for index, row in dfCreds.iterrows():
    users.append(User(id=row["id"], username=row["user"], password=row["pass"], fullName=row["name"]))


@app.server.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user



@app.server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect('/successLogin')

        return redirect('/Login')

    return redirect('/Login')


@app.server.route('/successLogin')
def profile():
    if not g.user:
        return redirect('/Login')

    return redirect('/Upload')


@app.server.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect('/Login')

login_form = dbc.Row([
    html.Form([
        dcc.Input(placeholder='username', name='username', type='text'),
        dcc.Input(placeholder='password', name='password', type='password'),
        html.Button('Login', type='submit')
    ], action='/login', method='post')
], justify="center", form=True,   className="twelve columns",
)

login = html.Div([
    dbc.Row(html.H3("Welcome to the Login Page!"), justify="center", form=True, className="twelve columns"),
    html.Div(id='custom-auth-frame'),
    html.Div(id='custom-auth-frame-1', style={'textAlign': 'right', "background": "black"}),
    login_form,
    dbc.Row(dbc.Button("Want a login?", href="/Contact", color="secondary", style={"margin":"2rem"}), justify="center", form=True),
], className="pretty_container ten columns offset-by-one column",
)


def Login():
    layout = login
    return layout
"""""