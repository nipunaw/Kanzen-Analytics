import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash
from home.models import Anime
from pytrends.request import TrendReq
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://www.dl.dropboxusercontent.com/s/99knran9jmm5beo/plotly-dash.css']


class Export_Container:
    def __init__(self, id:str, shared_info):
        self.shared_info = shared_info
        self.shared_info.pending_updates_export = True
        self.graphs_list = []
        self.app = DjangoDash(id, external_stylesheets=external_stylesheets)
        self.table = dash_table.DataTable()
        self.app.layout = self.serve_layout
        self.trend_data = pd.DataFrame()
        @self.app.callback(
            [Output('table','data'),
            Output('table','columns')],
            [Input('table','data')]
        )
        def update_table(value):
            self.init_data()
            table_data = self.trend_data.to_dict('records')
            table_cols = [{"name": i,"id":i}for i in self.trend_data.columns]
            return table_data, table_cols
        
        

    def serve_layout(self):
        if self.shared_info.pending_updates_export:
           self.shared_info.pending_updates_export = False
           self.table = self.init_table('Export', 5)

        return html.Div([
            html.H1("Export Page"),
            self.table,
            #html.A('Download CSV', id='my_link',n_clicks=0,href=''),
            #Download(id='download')
        ])

    def init_table(self, type:str='Add', pg_size:int=5):
        names = self.init_data()
        #print(self.trend_data)
        
        layout = dash_table.DataTable(
            id='table',
            data=self.trend_data.to_dict('records'),
            columns=[{"name": i,"id":i}for i in self.trend_data.columns],
            page_size=50,
            editable=True,
            export_format='csv',
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
            data.append({'Name': title, 'Export Graph(s)': "Don't Export Graph"})
        trendshow = TrendReq(hl='en-US', tz=360)
        kw_group = list(zip(*[iter(self.graphs_list)] * 1))
        kw_grplist = [list(x) for x in kw_group]
        dic = {}
        i = 0
        for kw in kw_grplist:
            trendshow.build_payload(kw, timeframe='today 5-y', geo='')
            dic[i] = trendshow.interest_over_time()
            i += 1
        if len(dic) > 0:
            trendframe = pd.concat(dic, axis=1)
            trendframe.columns = trendframe.columns.droplevel(0)
            trendframe = trendframe.drop('isPartial', axis=1)
            trendframe = trendframe.reset_index()
            self.trend_data=trendframe
        else:
            self.trend_data = pd.DataFrame()
        return data
    