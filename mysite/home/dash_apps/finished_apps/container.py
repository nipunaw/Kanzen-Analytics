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
        self.graphs_list = []
        if  edit_page==False:
            self.jikan = Jikan()
            
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
            #DEBUG
            self.graphs_list = ["Demon Slayer","Sailor Moon", "Jojo"]
            #print(self.graphs_list)
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
                [Input('remove_graphs','n_clicks'),
                State('table', 'data')])
            def remove_graphs(n_clicks,value):
                data = []
                dropdown = {
                        'Remove Graph(s)': {
                            'options': [
                                {'label': "Don't remove Graph", 'value': "Don't remove Graph"},
                                {'label': "Remove Graph", 'value': "Remove Graph"}
                            ]
                        }
                    }
                
        
                graphs_to_remove = []
                #print(self.graphs_list)
                if n_clicks >0:
                    #print(data)
                    for i in value:
                        #print(i)
                        if i['Remove Graph(s)'] == 'Remove Graph':
                            graphs_to_remove.append(i['Name'])    
                    for name in graphs_to_remove:
                            self.graphs_list.remove(name)
                            #print(self.graphs_list)
                            
                for title in self.graphs_list:
                        data.append({'Name':title,'Remove Graph(s)':"Don't remove Graph"})
                return data, dropdown


        


    def search_anime(self, anime_name):
        search = self.jikan.search('anime', anime_name)
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
        )

        return layout

