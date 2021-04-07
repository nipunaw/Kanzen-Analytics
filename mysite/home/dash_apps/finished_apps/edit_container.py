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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

class Edit_Container:
    def __init__(self,id:str):
        self.graphs_list = ["Demon Slayer","Sailor Moon", "Jojo"]
        #print(self.graphs_list)
        self.app = DjangoDash(id, external_stylesheets=external_stylesheets)
        self.app.layout = html.Div([
            html.H1("Edit Page"),
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
