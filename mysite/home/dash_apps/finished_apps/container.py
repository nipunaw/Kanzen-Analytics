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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']




class Container:

    def __init__(self, id:str, shared_info):
        self.shared_info = shared_info
        self.shared_info.pending_updates_main = True
        self.graphs_list = []
        self.jikan = Jikan()
        self.div = html.Div(id="graphcontainer")

        self.app = DjangoDash(id, external_stylesheets=external_stylesheets)
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
            State('graphname', 'value')]
        )
        def update_table(n_clicks, value):
            data = []
            dropdown = {}

            if n_clicks > 0 and value is not None:
                results = self.search_anime(value)

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
            dcc.Input(id='graphname', type='text', placeholder='Enter Show Name'),
            html.Button(id="search_button", n_clicks=0, children="Search"),
            html.Hr(),
            html.Div(id='genre-dropdown',children='Genre:'),
            dcc.Dropdown(
                options=[
                    {'label': 'Any', 'value': '1'},
                    {'label': 'Action', 'value': '2'},
                    {'label': 'Cars', 'value': '3'},
                    {'label': 'Comedy', 'value': '4'},
                    {'label': 'Dementia', 'value': '5'},
                    {'label': 'Demons', 'value': '6'},
                    {'label': 'Mystery', 'value': '7'},
                    {'label': 'Drama', 'value': '8'},
                    {'label': 'Ecchi', 'value': '9'},
                    {'label': 'Fantasy', 'value': '10'},
                    {'label': 'Game', 'value': '11'},
                    {'label': 'Hentai', 'value': '12'},
                    {'label': 'Historical', 'value': '13'},
                    {'label': 'Horror', 'value': '14'},
                    {'label': 'Kids', 'value': '15'},
                    {'label': 'Magic', 'value': '16'},
                    {'label': 'Martial Arts', 'value': '17'},
                    {'label': 'Mecha', 'value': '18'},
                    {'label': 'Music', 'value': '19'},
                    {'label': 'Parody', 'value': '20'},
                    {'label': 'Samurai', 'value': '21'},
                    {'label': 'Romance', 'value': '22'},
                    {'label': 'School', 'value': '23'},
                    {'label': 'Sci Fi', 'value': '24'},
                    {'label': 'Shoujo', 'value': '25'},
                    {'label': 'Shoujo Ai', 'value': '26'},
                    {'label': 'Shounen', 'value': '27'},
                    {'label': 'Shounen Ai', 'value': '28'},
                    {'label': 'Space', 'value': '29'},
                    {'label': 'Sports', 'value': '30'},
                    {'label': 'Super Power', 'value': '31'},
                    {'label': 'Vampire', 'value': '32'},
                    {'label': 'Yaoi', 'value': '33'},
                    {'label': 'Yuri', 'value': '34'},
                    {'label': 'Harem', 'value': '35'},
                    {'label': 'Slice Of Life', 'value': '36'},
                    {'label': 'Supernatural', 'value': '37'},
                    {'label': 'Military', 'value': '38'},
                    {'label': 'Police', 'value': '39'},
                    {'label': 'Psychological', 'value': '40'},
                    {'label': 'Thriller', 'value': '41'},
                    {'label': 'Seinen', 'value': '42'},
                    {'label': 'Josei', 'value': '43'},

                ],
                value='1'
            ),

            html.Div(id='category-dropdown',
                     children='Category:'),

            dcc.Dropdown(
                options=[
                    {'label': 'Any', 'value': '1'},
                    {'label': 'TV', 'value': '2'},
                    {'label': 'OVA', 'value': '3'},
                    {'label': 'Movie', 'value': '4'},
                    {'label': 'Special', 'value': '5'},
                    {'label': 'ONA', 'value': '6'},
                    {'label': 'Music', 'value': '7'},
                ],
                value='1'
            ),

            html.Div(id='range-button',
                     children='Select the range of data:'),

            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=date(2020, 3, 23),
                end_date_placeholder_text='Select a date!'
            ),
            html.Hr(),
            self.init_table(),
            html.Button(id="add_graphs", n_clicks=0, children="Add selected graphs"),
            
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
        


    def search_anime(self, anime_name):
        search = self.jikan.search('anime', anime_name)
        #user = self.jikan.user_list(38000)
        #print(user)
        #print(user['birthday'])
        #print(user['gender'])
        return search["results"]


    def init_table(self, type:str='Add', pg_size:int=5):
        layout = dash_table.DataTable(
            id='table',
            columns=[{"name": "Name", "id": "Name"}, {"name": type+' Graph(s)', "id": type+' Graph(s)', "presentation": "dropdown"}],
            data=[{'Name': "", type+' Graph(s)': ""},
                  {'Name': "", type+' Graph(s)': ""},
                  {'Name': "", type+' Graph(s)': ""},
                  {'Name': "", type+' Graph(s)': ""},
                  {'Name': "", type+' Graph(s)': ""}],
            page_size=pg_size,
            editable=True,
            #row_deletable=True,
        )

        return layout

