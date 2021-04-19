import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash
from jikanpy import Jikan
from home.dash_apps.finished_apps import graphs
from home.models import Anime

# Stores all custom graphs

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://www.dl.dropboxusercontent.com/s/99knran9jmm5beo/plotly-dash.css'] #

class Container:

    def __init__(self, id:str, shared_info):
        self.shared_info = shared_info
        self.shared_info.pending_updates_main = True
        self.names_list = []
        self.graphs_list = []
        self.jikan = Jikan()
        self.div = html.Div(id="graphcontainer")

        self.status_children = "Status: No issues. Feel free to add graphs"
        self.add_graphs_disabled = False

        self.app = DjangoDash(id, external_stylesheets=external_stylesheets)
        self.genre_options = [
                    {'label': 'Any', 'value': '1'},
                    {'label': 'Action', 'value': '2'},
                    {'label': 'Adventure', 'value': '3'},
                    {'label': 'Cars', 'value': '4'},
                    {'label': 'Comedy', 'value': '5'},
                    {'label': 'Dementia', 'value': '6'},
                    {'label': 'Demons', 'value': '7'},
                    {'label': 'Mystery', 'value': '8'},
                    {'label': 'Drama', 'value': '9'},
                    {'label': 'Ecchi', 'value': '10'},
                    {'label': 'Fantasy', 'value': '11'},
                    {'label': 'Game', 'value': '12'},
                    {'label': 'Hentai', 'value': '13'},
                    {'label': 'Historical', 'value': '14'},
                    {'label': 'Horror', 'value': '15'},
                    {'label': 'Kids', 'value': '16'},
                    {'label': 'Magic', 'value': '17'},
                    {'label': 'Martial Arts', 'value': '18'},
                    {'label': 'Mecha', 'value': '19'},
                    {'label': 'Music', 'value': '20'},
                    {'label': 'Parody', 'value': '21'},
                    {'label': 'Samurai', 'value': '22'},
                    {'label': 'Romance', 'value': '23'},
                    {'label': 'School', 'value': '24'},
                    {'label': 'Sci Fi', 'value': '25'},
                    {'label': 'Shoujo', 'value': '26'},
                    {'label': 'Shoujo Ai', 'value': '27'},
                    {'label': 'Shounen', 'value': '28'},
                    {'label': 'Shounen Ai', 'value': '29'},
                    {'label': 'Space', 'value': '30'},
                    {'label': 'Sports', 'value': '31'},
                    {'label': 'Super Power', 'value': '32'},
                    {'label': 'Vampire', 'value': '33'},
                    {'label': 'Yaoi', 'value': '34'},
                    {'label': 'Yuri', 'value': '35'},
                    {'label': 'Harem', 'value': '36'},
                    {'label': 'Slice Of Life', 'value': '37'},
                    {'label': 'Supernatural', 'value': '38'},
                    {'label': 'Military', 'value': '39'},
                    {'label': 'Police', 'value': '40'},
                    {'label': 'Psychological', 'value': '41'},
                    {'label': 'Thriller', 'value': '42'},
                    {'label': 'Seinen', 'value': '43'},
                    {'label': 'Josei', 'value': '44'},

                ]

        self.category_options = [
                    {'label': 'Any', 'value': '1'},
                    {'label': 'TV', 'value': '2'},
                    {'label': 'OVA', 'value': '3'},
                    {'label': 'Movie', 'value': '4'},
                    {'label': 'Special', 'value': '5'},
                    {'label': 'ONA', 'value': '6'},
                    {'label': 'Music', 'value': '7'},
                ]


        self.app.layout = self.serve_layout

        # @self.app.callback(
        #     Output('graphcontainer', 'children'),
        #     [Input('search_button', 'n_clicks'),
        #      State('searchname', 'value')]
        # )
        @self.app.callback(
            [Output('table', 'data'),
            Output('table', 'dropdown')],
            [Input('search_button', 'n_clicks'),
            #Input("searchname", "value"),
            Input("searchname", 'n_submit'),
            State("searchname", "value"),
            State('genre_dropdown', 'value'),
            State('category_dropdown', 'value'),
            State('date_picker_range', 'start_date'),
            State('date_picker_range', 'end_date')]
        )
        def update_table(n_clicks, n_submit, searchname, genre_dropdown, category_dropdown, start_date, end_date):
            data = [{'Name': "", 'Add Graph(s)': ""},
                    {'Name': "", 'Add Graph(s)': ""},
                    {'Name': "", 'Add Graph(s)': ""},
                    {'Name': "", 'Add Graph(s)': ""},
                    {'Name': "", 'Add Graph(s)': ""}]
            dropdown = {}

            if searchname is not None:
                data = []
                #self.search_anime_gender_birthday(1)
                selected_genre = int(genre_dropdown) - 1
                selected_category = (self.category_options[int(category_dropdown) - 1]['label'])
                results = self.search_anime(searchname, selected_genre, selected_category, start_date, end_date)

                for x in range(0, len(results)-1):
                    data.append({'Name': results[x]["title"], 'Add Graph(s)': "Don't add Graph"})

                dropdown = {
                    'Add Graph(s)': {
                        'options': [
                            {'label': "No", 'value': "Don't add Graph"},
                            {'label': "Yes", 'value': "Add Graph"}
                        ],
                        'searchable': False,
                        'clearable': False
                    }
                }
            
            return data, dropdown

        @self.app.callback(
            [Output('graphcontainer', 'children'),
            Output('status_message', 'children'),
            Output('add_graphs', 'disabled')],
            [Input('add_graphs', 'n_clicks'),
            State('table', 'data')]
        )
        def add_graph(n_clicks, data):
            id = 'graph-{}'.format(n_clicks)

            disable_add_button = self.add_graphs_disabled
            children = self.status_children
            flag_duplicates = False

            names_to_query = []
            num_graphs = Anime.objects.count()
            for i in data:
                if i['Add Graph(s)'] == 'Add Graph' and num_graphs < 5:
                    if i['Name'] not in self.names_list:
                        num_graphs = num_graphs + 1
                        self.names_list.append(i['Name'])
                        names_to_query.append(i['Name'])
                        a = Anime(anime_name=i['Name'], anime_order=num_graphs)
                        a.save()
                        children = "Status: Graph(s) added successfully. "+str(num_graphs)+"/5 in total."
                    else:
                        flag_duplicates = True
                        children = "Status: Duplicate entries were detected; only non-duplicates (if any) were added."
                elif num_graphs >= 5:
                    disable_add_button = True
                    children = "Status: Max graphs (5) limit reached. Graphs may be removed via 'Settings' page."
                    if flag_duplicates:
                        children = "Status: Max graphs (5) limit reached. Duplicates that were detected were not added."

            if n_clicks > 0 and len(names_to_query) > 0:
                self.shared_info.pending_updates_edit = True
                self.shared_info.pending_updates_export = True
                for i in names_to_query:
                    test = graphs.Graphs(i + 'app', i, i, i + 'slider', False,
                                        [Input(i + 'slider', 'value')], self.shared_info.color_graphs, self.shared_info.time_scale, i)

                    self.graphs_list.append(test.return_layout())  # dcc.Graph(id='graph-{}'.format(n_clicks), figure=test.return_fig())
            if self.shared_info.pending_updates_main:
                self.shared_info.pending_updates_main = False
                self.div = html.Div(children=self.init_graph(), id="graphcontainer")
                return self.div, children, disable_add_button
 
            return html.Div(self.graphs_list), children, disable_add_button

    def serve_layout(self):
        if self.shared_info.pending_updates_main:
            self.shared_info.pending_updates_main = False
            self.div = html.Div(children=self.init_graph(), id="graphcontainer")

        num_graphs = Anime.objects.count()

        if num_graphs == 5:
            self.status_children = "Status: Max graphs (5) limit reached. Graphs may be removed via 'Settings' page."
            self.add_graphs_disabled = True
        else:
            self.status_children = "Status: No issues. Feel free to add graphs ("+str(num_graphs)+"/5 total limit)"
            self.add_graphs_disabled = False

        return html.Div([
            html.Div(
                id='searchtablearea',
                children=[
                html.Div(
                    id='searcharea',
                    children=[
                        dcc.Input(
                            id='searchname',
                            type='text',
                            placeholder='Enter Show Name',
                            debounce=True,
                            n_submit=0
                        ),
                        html.Button(id="search_button", n_clicks=0, children="Search"),
                        html.P('Genre:'),
                        dcc.Dropdown(id='genre_dropdown',
                                     options=self.genre_options,
                                     value='1',
                                     clearable=False
                                     ),

                        html.P('Category:'),
                        dcc.Dropdown(id='category_dropdown',
                                     options=self.category_options,
                                     value='1',
                                     clearable=False
                                     ),

                        html.P('Select search range:'),

                        dcc.DatePickerRange(
                            id='date_picker_range',
                            start_date_placeholder_text='Select start date',
                            end_date_placeholder_text='Select end date',
                            clearable=True,
                        ),
                    ]),
                html.Div(
                    id='tablearea',
                    children=
                    [self.init_table(),
                     html.P(id='status_message', children=self.status_children),
                     html.Button(id="add_graphs", n_clicks=0, children="Add selected graphs", disabled=self.add_graphs_disabled),
                ])

            ]),
            html.Hr(),
            self.div
        ])

    def init_graph(self):
        initial_graphs = []
        self.graphs_list = []
        self.names_list = []
        for a in Anime.objects.raw('SELECT anime_name FROM home_anime ORDER BY anime_order ASC'):
            p = str(a)
            self.names_list.append(p)
            initial_graphs.append(graphs.Graphs(p.replace(" ", ""), p, p.replace(" ", ""), p.replace(" ", "") + 'slider', False,
                               [Input(p.replace(" ", "") + 'slider', 'value')], self.shared_info.color_graphs, self.shared_info.time_scale, p))

        if len(initial_graphs) != 0:
             for i in initial_graphs:
                 self.graphs_list.append(i.return_layout())

        return html.Div(self.graphs_list)

    def search_anime_gender_birthday(self, anime_id):
        data = [sub['username'] for sub in self.jikan.anime(anime_id, extension='userupdates', page=1)["users"]]
        user = [self.jikan.user(username=name) for name in data]
        print(name['birthday'] for name in user)
        print(name['gender'] for name in user)



    def search_anime(self, anime_name, genre_number, category_name, start_date, end_date):
        search_params = {}

        if genre_number > 0:
            search_params['genre'] = genre_number

        if category_name != "Any":
            search_params['type'] = category_name

        if start_date is not None:
            search_params['start_date'] = start_date

        if end_date is not None:
            search_params['end_date'] = end_date

        search = self.jikan.search('anime', anime_name, parameters=search_params)

        #user = self.jikan.user_list(38000)
        #print(user)
        #print(user['birthday'])
        #print(user['gender'])
        return search["results"]


    def init_table(self, type:str='Add', pg_size:int=5):
        layout = dash_table.DataTable(
            id='table',
            style_cell={'textAlign': 'left'},
            style_data_conditional=[
                {
                    "if": {"state": "active"},  # 'active' | 'selected'
                    "backgroundColor": "#FFFFFF",
                    "border": "1px solid #3CCFCF",
                },
                {
                    "if": {"state": "selected"},
                    "backgroundColor": "##FFFFFF",
                    "border": "1px solid #3CCFCF",
                },
            ],
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            columns=[{"name": "Name",
                      "id": "Name",
                      "editable": False
                      },
                     {"name": type+' Graph(s)',
                      "id": type+' Graph(s)',
                      "presentation": "dropdown",
                      "editable": True,
                      }
            ],
            data=[],
            page_size=pg_size,
        )

        return layout

