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
from datetime import date

# Stores all custom graphs

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

class Container:
    def __init__(self, id:str,initial_graphs=None, edit_page=False):
        if  edit_page==False:
            self.jikan = Jikan()
            self.graphs_list = []
            if initial_graphs is None:
                self.graphs_list = []
            else:
                for i in initial_graphs:
                    self.graphs_list.append(i.return_layout())

            self.app = DjangoDash(id, external_stylesheets=external_stylesheets)

            self.app.layout = html.Div([
                #html.H1("Create New Graph"),
                dcc.Input(id='graphname', type='text', placeholder='Enter Show Name'),
                html.Button(id="search_button", n_clicks=0, children="Search"),
                html.Div(id='output-container-button',children='Genre:'),
                dcc.Dropdown(
                    options=[
                        {'label': 'Any', 'value': '1'},
                        {'label': 'Action', 'value': '2'},
                        {'label': 'Adventure', 'value': '3'},
                        {'label': 'BL', 'value': '4'},
                        {'label': 'Comedy', 'value': '5'},
                        {'label': 'Drama', 'value': '6'},
                    ],
                    value='1'
                ),

                html.Div(id='output-container-button',
                         children='Category:'),

                dcc.Dropdown(
                    options=[
                        {'label': 'Any', 'value': '1'},
                        {'label': 'Movie', 'value': '2'},
                        {'label': 'TV', 'value': '3'},
                        {'label': 'Manga', 'value': '4'},
                    ],
                    value='1'
                ),

                html.Div(id='output-container-button',
                         children='Select the range of data:'),

                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=date(2020, 3, 23),
                    end_date_placeholder_text='Select a date!'
                ),

                self.init_table(),
                html.Button(id="add_graphs", n_clicks=0, children="Add selected graphs"),
                html.Div(id="graphcontainer"),

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

                if n_clicks > 0 and len(names_to_query) > 0:
                    for i in names_to_query:
                        test = graphs.Graphs(i + 'app', i + ' Graph', i, i + 'slider', False,
                                            [Input(i + 'slider', 'value')], i)
                        
                        self.graphs_list.append(
                            test.return_layout()) 
                        

                return html.Div(self.graphs_list)
        # edit page init
        else:
            self.app = DjangoDash(id, external_stylesheets=external_stylesheets)
            self.app.layout = html.Div([
                #html.H1("Create New Graph"),
                self.init_table('Remove', 5),
                html.Button('Remove Selected Graphs',id="remove_graphs",n_clicks=0),
                html.Div(id="graphcontainer")
            ])
            @self.app.callback(
                [Output('table', 'data'),
                Output('table', 'dropdown')],
                [Input('remove_graphs','n_clicks')])
            def remove_graphs(n_clicks):
                ye=1


        


    def search_anime(self, anime_name):
        search = self.jikan.search('anime', anime_name)
        return search["results"]


    def init_table(self, type:str='Add', pg_size:int=5):
        layout = dash_table.DataTable(
            id='table',
            columns=[{"name": "Name", "id": "Name"}, {"name": type+' Graph(s)', "id": 'Add Graph(s)', "presentation": "dropdown"}],
            data=[{'Name': "", 'Add Graph(s)': ""},
                  {'Name': "", 'Add Graph(s)': ""},
                  {'Name': "", 'Add Graph(s)': ""},
                  {'Name': "", 'Add Graph(s)': ""},
                  {'Name': "", 'Add Graph(s)': ""}],
            page_size=pg_size,
            editable=True
        )

        return layout

