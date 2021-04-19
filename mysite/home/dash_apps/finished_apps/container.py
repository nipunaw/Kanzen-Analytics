import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash
from jikanpy import Jikan
from home.dash_apps.finished_apps import graphs
from home.models import Anime
from datetime import date

# Stores all custom graphs

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://dl.dropboxusercontent.com/s/zbb8j15aa5ixsrf/plotly-dash.css'] #

class Container:

    def __init__(self, id:str, shared_info):
        self.shared_info = shared_info
        self.shared_info.pending_updates_main = True
        self.graphs_list = []
        self.jikan = Jikan()
        self.div = html.Div(id="graphcontainer")

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
        #      State('graphname', 'value')]
        # )
        @self.app.callback(
            [Output('table', 'data'),
            Output('table', 'dropdown')],
            [Input('search_button', 'n_clicks'),
            State('graphname', 'value'),
            State('genre_dropdown', 'value'),
            State('category_dropdown', 'value')]
        )
        def update_table(n_clicks, graphname, genre_dropdown, category_dropdown):
            data = [{'Name': "", 'Add Graph(s)': ""},
                    {'Name': "", 'Add Graph(s)': ""},
                    {'Name': "", 'Add Graph(s)': ""},
                    {'Name': "", 'Add Graph(s)': ""},
                    {'Name': "", 'Add Graph(s)': ""}]
            dropdown = {}

            if n_clicks > 0 and graphname is not None:
                data = []
                #self.search_anime_gender_birthday(1)
                selected_genre = int(genre_dropdown) - 1
                selected_category = self.category_options[int(category_dropdown) - 1]['label']
                results = self.search_anime(graphname, selected_genre, selected_category)

                for x in range(0, len(results)-1):
                    data.append({'Name': results[x]["title"], 'Add Graph(s)': "Don't add Graph"})

                dropdown = {
                    'Add Graph(s)': {
                        'options': [
                            {'label': "Don't add Graph", 'value': "Don't add Graph"},
                            {'label': "Add Graph", 'value': "Add Graph"}
                        ]
                    }
                }

            return data, dropdown

        @self.app.callback(
            Output('graphcontainer', 'children'),
            [Input('add_graphs', 'n_clicks'),
            State('table', 'data')]
        )
        def add_graph(n_clicks, data):
            id = 'graph-{}'.format(n_clicks)

            names_to_query = []

            for i in data:
                if i['Add Graph(s)'] == 'Add Graph':
                    names_to_query.append(i['Name'])
                    a = Anime(anime_name=i['Name'])
                    a.save()

            if n_clicks > 0 and len(names_to_query) > 0:
                self.shared_info.pending_updates_edit = True
                self.shared_info.pending_updates_export = True
                for i in names_to_query:
                    test = graphs.Graphs(i + 'app', i + ' Graph', i, i + 'slider', False,
                                        [Input(i + 'slider', 'value')], i)

                    self.graphs_list.append(test.return_layout())  # dcc.Graph(id='graph-{}'.format(n_clicks), figure=test.return_fig())

            return html.Div(self.graphs_list)

    def serve_layout(self):
        if self.shared_info.pending_updates_main:
            self.shared_info.pending_updates_main = False
            self.div = html.Div(children=self.init_graph(), id="graphcontainer")

        return html.Div([
            html.Div(
                id='searchtablearea',
                children=[
                html.Div(
                    id='searcharea',
                    children=[
                        dcc.Input(id='graphname', type='text', placeholder='Enter Show Name'),
                        html.Button(id="search_button", n_clicks=0, children="Search"),
                        html.P('Genre:'),
                        dcc.Dropdown(id='genre_dropdown',
                                     options=self.genre_options,
                                     value='1'
                                     ),

                        html.P('Category:'),
                        dcc.Dropdown(id='category_dropdown',
                                     options=self.category_options,
                                     value='1'
                                     ),

                        html.P('Select search range:'),

                        dcc.DatePickerRange(
                            id='date-picker-range',
                            start_date=date(2020, 3, 23),
                            end_date_placeholder_text='Select a date!'
                        ),
                    ]),
                html.Div(
                    id='tablearea',
                    children=
                    [self.init_table(),
                     html.Button(id="add_graphs", n_clicks=0, children="Add selected graphs"),
                ])
            ]),
            self.div
        ])

    def init_graph(self):
        initial_graphs = []
        self.graphs_list = []
        for a in Anime.objects.raw('SELECT * FROM home_anime'):
            p = str(a)

            initial_graphs.append(graphs.Graphs(p.replace(" ", ""), p, p.replace(" ", ""), p.replace(" ", "") + 'slider', False,
                               [Input(p.replace(" ", "") + 'slider', 'value')], p))

        if len(initial_graphs) != 0:
             for i in initial_graphs:
                 self.graphs_list.append(i.return_layout())

        return html.Div(self.graphs_list)

    def search_anime_gender_birthday(self, anime_id):
        data = [sub['username'] for sub in self.jikan.anime(anime_id, extension='userupdates', page=1)["users"]]
        user = [self.jikan.user(username=name) for name in data]
        print(name['birthday'] for name in user)
        print(name['gender'] for name in user)



    def search_anime(self, anime_name, genre_number, category_name):
        search_params = {}

        if genre_number > 0:
            search_params['genre'] = genre_number

        if category_name != "Any":
            search_params['type'] = category_name

        search = self.jikan.search('anime', anime_name, parameters=search_params)

        #user = self.jikan.user_list(38000)
        #print(user)
        #print(user['birthday'])
        #print(user['gender'])
        return search["results"]


    def init_table(self, type:str='Add', pg_size:int=5):
        layout = dash_table.DataTable(
            id='table',
            columns=[{"name": "Name", "id": "Name"}, {"name": type+' Graph(s)', "id": type+' Graph(s)', "presentation": "dropdown"}],
            data=[],
            page_size=pg_size,
            editable=True,
            #row_deletable=True,
        )

        return layout
