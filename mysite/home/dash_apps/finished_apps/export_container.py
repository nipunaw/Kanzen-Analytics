import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash
from home.models import Anime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

class Export_Container:
    def __init__(self, id:str, shared_info):
        self.shared_info = shared_info
        self.shared_info.pending_updates_export = True
        self.graphs_list = []
        self.app = DjangoDash(id, external_stylesheets=external_stylesheets)
        self.table = dash_table.DataTable()
        self.app.layout = self.serve_layout

        @self.app.callback(
            [Output('table', 'data'),
            Output('table', 'dropdown')],
            [Input('export_graphs','n_clicks'),
            State('table', 'data')])
        def remove_graphs(n_clicks,value):
            data = []
            dropdown = {
                    'Export Graph(s)': {
                        'options': [
                            {'label': "Export Graph", 'value': "Export Graph"},
                            {'label': "Don't Export Graph", 'value': "Don't Export Graph"}
                        ]
                    }
                }

            graphs_to_remove = []
            if n_clicks >0:
                self.shared_info.pending_updates_main = True
                self.shared_info.pending_updates_edit = True
                for i in value:
                    if i['Export Graph(s)'] == 'Export Graph':
                        graphs_to_remove.append(i['Name'])    
                for name in graphs_to_remove:
                        self.graphs_list.remove(name)
                        Anime.objects.filter(pk=name).delete()
                        
            for title in self.graphs_list:
                    data.append({'Name':title,'Export Graph(s)':"Don't Export Graph"})
            return data, dropdown

    def serve_layout(self):
        if self.shared_info.pending_updates_export:
           self.shared_info.pending_updates_export = False
           self.table = self.init_table('Export', 5)

        return html.Div([
            html.H1("Export Page"),
            self.table,
            html.Button('Export Selected Graphs', id="export_graphs", n_clicks=0),
        ])

    def init_table(self, type:str='Add', pg_size:int=5):
        layout = dash_table.DataTable(
            id='table',
            columns=[{"name": "Name", "id": "Name"}, {"name": type+' Graph(s)', "id": type+' Graph(s)', "presentation": "dropdown"}],
            data=self.init_data(),
            page_size=pg_size,
            editable=True,
            #row_deletable=True,
        )

        return layout

    def init_data(self):
        data = []
        self.graphs_list = []
        for a in Anime.objects.raw('SELECT * FROM home_anime'):
            p = str(a)
            self.graphs_list.append(p)
        for title in self.graphs_list:
            data.append({'Name': title, 'Export Graph(s)': "Don't Export Graph"})
        return data