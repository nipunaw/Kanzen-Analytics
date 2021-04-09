import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash
from home.models import Anime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

class Edit_Container:

    def __init__(self, id:str, shared_info):
        self.shared_info = shared_info
        self.shared_info.pending_updates_edit = True
        self.graphs_list = []
        self.app = DjangoDash(id, external_stylesheets=external_stylesheets)
        self.table = dash_table.DataTable()
        self.app.layout = self.serve_layout

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
            if n_clicks > 0:
                self.shared_info.pending_updates_main = True
                self.shared_info.pending_updates_export = True
                for i in value:
                    if i['Remove Graph(s)'] == 'Remove Graph':
                        graphs_to_remove.append(i['Name'])
                for name in graphs_to_remove:
                        self.graphs_list.remove(name)
                        Anime.objects.filter(pk=name).delete()

            for title in self.graphs_list:
                    data.append({'Name':title,'Remove Graph(s)':"Don't remove Graph"})
            return data, dropdown

    def serve_layout(self):
        if self.shared_info.pending_updates_edit:
            self.shared_info.pending_updates_edit = False
            self.table = self.init_table('Remove', 5)

        return html.Div([
                html.H1("Edit Page"),
                self.table,
                html.Button('Remove Selected Graphs', id="remove_graphs", n_clicks=0)
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
            data.append({'Name': title, 'Remove Graph(s)': "Don't remove Graph"})
        return data
