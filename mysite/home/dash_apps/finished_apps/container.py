import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from jikanpy import Jikan
from pytrends.request import TrendReq
import pandas as pd
from home.dash_apps.finished_apps import graphs
from home.models import Anime

# Stores all custom graphs

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

class Container:

    def __init__(self, initial_graphs=None):
        self.jikan = Jikan()
        self.graphs_list = []
        if initial_graphs is None:
            self.graphs_list = []
        else:
            for i in initial_graphs:
                self.graphs_list.append(i.return_layout())

        self.app = DjangoDash('container', external_stylesheets=external_stylesheets)

        self.app.layout = html.Div([
            #html.H1("Create New Graph"),
            dcc.Input(id='graphname', type='text', placeholder='Enter Show Name'),
            html.Button(id="search_button", n_clicks=0, children="Search"),
            self.init_table(),
            html.Button(id="add_graphs", n_clicks=0, children="Add selected graphs"),
            html.Div(id="graphcontainer")
        ])

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
                for i in names_to_query:
                    test = graphs.Graphs(i + 'app', i + ' Graph', i, i + 'slider', False,
                                         [Input(i + 'slider', 'value')], i)
                    self.graphs_list.append(
                        test.return_layout())  # dcc.Graph(id='graph-{}'.format(n_clicks), figure=test.return_fig())
            return html.Div(self.graphs_list)


    def search_anime(self, anime_name):
        search = self.jikan.search('anime', anime_name)
        user = self.jikan.user_list(38000)
        print(user)
        #print(user['birthday'])
        #print(user['gender'])
        return search["results"]



    def init_table(self):
        layout = dash_table.DataTable(
            id='table',
            columns=[{"name": "Name", "id": "Name"}, {"name": 'Add Graph(s)', "id": 'Add Graph(s)', "presentation": "dropdown"}],
            data=[{'Name': "", 'Add Graph(s)': ""},
                  {'Name': "", 'Add Graph(s)': ""},
                  {'Name': "", 'Add Graph(s)': ""},
                  {'Name': "", 'Add Graph(s)': ""},
                  {'Name': "", 'Add Graph(s)': ""}],
            page_size=5,
            editable=True
        )

        return layout
