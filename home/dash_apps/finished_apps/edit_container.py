import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash
from home.models import Anime
import configparser
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://www.dl.dropboxusercontent.com/s/99knran9jmm5beo/plotly-dash.css']

class Edit_Container:

    def __init__(self, id:str, shared_info):
        self.shared_info = shared_info
        self.shared_info.pending_updates_edit = True
        self.graphs_list = []
        self.app = DjangoDash(id, external_stylesheets=external_stylesheets)
        self.table = dash_table.DataTable()
        #self.reorder_table = dash_table.DataTable()
        self.app.layout = self.serve_layout

        @self.app.callback(
            [Output('table', 'data'),
            Output('table', 'dropdown'),
            Output('hidden_div','style')
            ],
            [Input('remove_graphs','n_clicks'),
             State('line_color_dropdown', 'value'),
             State('time_range_dropdown', 'value'),
             State('table', 'data')])
        def remove_graphs(n_clicks, line_color, time_scale, value):
            options = []
            dropdown = {}
            #old_index = []
            #save old index's
            for i in range(1,len(value)+1):
                options.append({'label':str(i)+"⠀⠀",'value':i})
            # Setup remove data
            data = []
            dropdown = {
                    'Remove Graph(s)': {
                        'options': [
                            {'label': "No", 'value': "Don't remove Graph"},
                            {'label': "Yes", 'value': "Remove Graph"}
                        ],
                        'clearable': False,
                        'searchable': False
                    },
                    'Order': {
                        'options': options,
                        'clearable': False,
                        'searchable': False
                    }
                } 
            
            graphs_to_remove = []
            if n_clicks > 0:
                self.shared_info.pending_updates_main = True
                self.shared_info.pending_updates_export = True

                for i in value:
                    #print(i['Order'])
                    if i['Remove Graph(s)'] == 'Remove Graph':
                        graphs_to_remove.append(i['Name'])
                for name in graphs_to_remove:
                        self.graphs_list.remove(name)
                        a = Anime.objects.get(anime_name = name)
                        b = Anime.objects.all().filter(anime_order__gt=a.anime_order)
                        for element in b:
                            element.anime_order = element.anime_order-1
                            for i in value:
                                if i['Name'] == element.anime_name:
                                    i['Order'] = i['Order'] - 1
                            element.save()
                        a.delete()
                # remove elements then reorder to prevent any issues
                
                for i in value:
                    already_removed = False
                    temp = None
                    try:
                        temp = Anime.objects.get(anime_name = i['Name'])
                    except:
                        already_removed = True
                    if  already_removed == False:
                    
                        if temp.anime_order != i['Order']:
                            temp.anime_order = i['Order']
                            temp.save()

            div_style ={'display':'none'}
            # check if any order values are repeated
            
            for a in Anime.objects.all():
                #print(len(Anime.objects.filter(anime_order = a.anime_order)))
                if len(Anime.objects.filter(anime_order = a.anime_order)) > 1:
                    div_style = {'display': 'block'}
            
            for a in Anime.objects.raw('SELECT * FROM home_anime ORDER BY anime_order ASC'):
                    data.append({'Name': a.anime_name, 'Remove Graph(s)': "Don't remove Graph", 'Order':a.anime_order})

            if line_color is not self.shared_info.color_graphs:
                config = configparser.ConfigParser()
                path = os.path.join(os.path.dirname(__file__), 'config.ini')
                config.read(path)
                config['SETTINGS']['color'] = line_color
                with open(path, 'w') as configfile:
                    config.write(configfile)
                self.shared_info.color_graphs = line_color
                self.shared_info.pending_updates_main = True

            if time_scale is not self.shared_info.time_scale:
                config = configparser.ConfigParser()
                path = os.path.join(os.path.dirname(__file__), 'config.ini')
                config.read(path)
                config['SETTINGS']['time_scale'] = time_scale
                with open(path, 'w') as configfile:
                    config.write(configfile)
                self.shared_info.time_scale = time_scale
                self.shared_info.pending_updates_main = True

            return data, dropdown, div_style#, reorder_data, reorder_dropdown
        
        
    def serve_layout(self):
        if self.shared_info.pending_updates_edit:
            self.shared_info.pending_updates_edit = False
            self.table = self.init_table('Remove', 5)
            #self.reorder_table = self.init_reorder_table()

        return html.Div([
                html.H1("Settings"),
                self.table,
                html.P('Graph line color:'),
                dcc.Dropdown(id='line_color_dropdown',
                             options=[{'label': 'Blue', 'value': 'SteelBlue'},
                                      {'label': 'Red', 'value': 'Crimson'},
                                      {'label': 'Green', 'value': 'Green'},
                                      {'label': 'Orange', 'value': 'Orange'}],
                             value=self.shared_info.color_graphs,
                             clearable=False,
                             searchable=False
                             ),
                html.P('Graph time range:'),
                dcc.Dropdown(id='time_range_dropdown',
                         options=[{'label': '1 Month', 'value': '1-m'},
                                  {'label': '3 Months', 'value': '3-m'},
                                  {'label': '1 Year', 'value': '12-m'},
                                  {'label': '5 Years', 'value': '5-y'}],
                         value=self.shared_info.time_scale,
                         clearable=False,
                         searchable=False
                         ),
                html.Button('Submit Changes', id="remove_graphs", n_clicks=0),
                html.Div([html.H2('Invalid Input: 2 or more elements have the same order',style={'color':'red'})],id='hidden_div',style={'display':'none'},)
                #self.reorder_table,
                #html.Button('Reorder Graphs', id="reorder_btn", n_clicks=0),
        ])


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
                      "editable": False},
                     {"name": type+' Graph(s)',
                      "id": type+' Graph(s)',
                      "presentation": "dropdown",
                      "editable": True},
                     {"name": "Order",
                      "id": "Order",
                      "presentation": "dropdown",
                      "editable": True}],
            data=self.init_data(),
            page_size=pg_size,
        )

        return layout

    def init_data(self):
        data = []
        self.graphs_list = []
        for a in Anime.objects.raw('SELECT anime_name FROM home_anime ORDER BY anime_order ASC'):
            p = str(a)
            self.graphs_list.append(p)
        for title in self.graphs_list:
            data.append({'Name': title, 'Remove Graph(s)': "Don't remove Graph"})
        return data
    
