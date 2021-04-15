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
        #self.reorder_table = dash_table.DataTable()
        self.app.layout = self.serve_layout

        @self.app.callback(
            [Output('table', 'data'),
            Output('table', 'dropdown'),
            ],
            [Input('remove_graphs','n_clicks'),
            State('table', 'data')])
        def remove_graphs(n_clicks,value):
            #Begin new reorder code
            options = []
            dropdown = {}
            for i in range(1,len(value)+1):
                options.append({'label':i,'value':i})
            # Setup remove data
            data = []
            dropdown = {
                    'Remove Graph(s)': {
                        'options': [
                            {'label': "Don't remove Graph", 'value': "Don't remove Graph"},
                            {'label': "Remove Graph", 'value': "Remove Graph"}
                        ]
                    },
                    'Order':{
                        'options':options
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

            for a in Anime.objects.raw('SELECT * FROM home_anime ORDER BY anime_order ASC'):
                    data.append({'Name':a.anime_name,'Remove Graph(s)':"Don't remove Graph",'Order':a.anime_order})
            
            return data, dropdown#, reorder_data, reorder_dropdown
        '''@self.app.callback(
            [Output('reorder_table','data'),
            Output('reorder_table','dropdown')],
            [Input('reorder_btn','n_clicks'),
            State('reorder_table','data'),
            State('table','data')]
        )
        def reorder_graphs(n_clicks,reorder_values,remove_table):
            self.shared_info.pending_updates_main = True
            self.shared_info.pending_updates_export = True

            options = []
            anime_objects = Anime.objects.raw('SELECT * FROM home_anime ORDER BY anime_order ASC')
            for i in range(1,len(remove_table)+1):
                options.append({'label':i,'value':i})
            dropdown = {
                'Order':{
                    'options':options
                }
            }
            
            # get dropdown selections, edit database
            for i in reorder_values:
                temp = Anime.objects.get(anime_name = i['Name'])

                if temp.anime_order != i['Order']:
                    temp.anime_order = i['Order']
                    temp.save()

            data = []
            for a in Anime.objects.raw('SELECT * FROM home_anime ORDER BY anime_order ASC'):
                data.append({'Name':a.anime_name,'Order':a.anime_order})
            return data,dropdown'''
    def serve_layout(self):
        if self.shared_info.pending_updates_edit:
            self.shared_info.pending_updates_edit = False
            self.table = self.init_table('Remove', 5)
            #self.reorder_table = self.init_reorder_table()

        return html.Div([
                html.H1("Edit Page"),
                self.table,
                html.Button('Submit Changes', id="remove_graphs", n_clicks=0),
                #self.reorder_table,
                #html.Button('Reorder Graphs', id="reorder_btn", n_clicks=0),
        ])


    def init_table(self, type:str='Add', pg_size:int=5):
        layout = dash_table.DataTable(
            id='table',
            columns=[{"name": "Name", "id": "Name"}, {"name": type+' Graph(s)', "id": type+' Graph(s)', "presentation": "dropdown"},{"name":"Order","id":"Order","presentation":"dropdown"}],
            data=self.init_data(),
            page_size=pg_size,
            editable=True,
            #row_deletable=True,
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
    '''def init_reorder_table(self):
        layout = dash_table.DataTable(
            id='reorder_table',
            columns=[{"name":"Name","id":"Name"},{"name":'Order','id':'Order',"presentation":"dropdown"}],
            data = self.init_reorder_data(),
            page_size = 10,
            editable=True,
        )
        return layout
    def init_reorder_data(self):
        data = []
        for a in Anime.objects.raw('SELECT * FROM home_anime ORDER BY anime_order ASC'):
            p = str(a.anime_name)
            i = str(a.anime_order)
            data.append({"Name":p,"Order":i})
        return data'''
