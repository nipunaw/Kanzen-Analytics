import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from jikanpy import Jikan
from pytrends.request import TrendReq
import pandas as pd
import time

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


class Graphs:
    def __init__(self, app_name, graph_title, graph_id, slider_id, top_bool, app_input_state_list, graph_color='Crimson', time_scale='12-m',
                 anime_name="default"):
        self.jikan = Jikan()
        self.app_name = app_name
        self.graph_title = graph_title
        self.graph_id = graph_id
        self.slider_id = slider_id
        self.top_bool = top_bool
        self.app_input_state_list = app_input_state_list
        self.graph_color = graph_color
        self.time_scale = time_scale
        self.anime_name = anime_name
        self.app = DjangoDash(app_name, external_stylesheets=external_stylesheets)
        self.app.layout = html.Div([
            html.H1(graph_title),
            #html.Button("Custom export", id="export_table", **{"data-dummy": ""}),
            self.return_graph(), # dcc.Graph(id=graph_id, animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'})
            # html.Button("Custom export", id="export_table", **{"data-dummy": ""}),
            # dcc.Slider(
            #     id=slider_id,
            #     marks={i: '{}'.format(i) for i in range(20)},
            #     max=20,
            #     value=2,
            #     step=1,
            #     updatemode='drag',
            #     min=0,
            # ),
        ])

        self.app.clientside_callback(
            """
            function(n_clicks) {
                if (n_clicks > 0)
                    document.querySelector("#topanime a.modebar-btn").click()
                return ""
            }
            """,
            Output("export_table", "data-dummy"),
            [Input("export_table", "n_clicks")]
        )


        @self.app.callback(
            Output(graph_id, 'figure'),
            app_input_state_list)
        def display_value(value):

            trendshow = TrendReq(hl='en-US', tz=360)

            kw_list = []
            if top_bool:
                for k in range(0, 5):
                    kw_list.append(self.get_top_anime_names(k, 'tv'))
            else:
                kw_list.append(self.search_anime(anime_name))
            kw_group = list(zip(*[iter(kw_list)] * 1))
            kw_grplist = [list(x) for x in kw_group]
            dic = {}
            i = 0
            for kw in kw_grplist:
                trendshow.build_payload(kw, timeframe='today 1-w', geo='')
                dic[i] = trendshow.interest_over_time()
                i += 1

            trendframe = pd.concat(dic, axis=1)
            trendframe.columns = trendframe.columns.droplevel(0)
            trendframe = trendframe.drop('isPartial', axis=1)

            trace = [go.Scatter(
                x=trendframe.index,
                y=trendframe[col], name=col) for col in trendframe.columns]
            layout = dict(
                paper_bgcolor='#27293d',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=True
                
            )
            return {'data': trace, 'layout': layout}




    def get_top_anime_names(self, rank: int, subtype: str):
        top_anime = self.jikan.top(type='anime', page=1, subtype=subtype)
        time.sleep(0.5)
        return top_anime["top"][rank]["title"]

    def search_anime(self, anime_name):
        search = self.jikan.search('anime', anime_name)
        time.sleep(0.5)
        return search["results"][0]["title"]

    def return_graph(self):
        trendshow = TrendReq(hl='en-US', tz=360)

        kw_list = []
        if self.top_bool:
            for k in range(0, 5):
                kw_list.append(self.get_top_anime_names(k, 'tv'))
        else:
            kw_list.append(self.search_anime(self.anime_name))
        kw_group = list(zip(*[iter(kw_list)] * 1))
        kw_grplist = [list(x) for x in kw_group]
        dic = {}
        i = 0
        for kw in kw_grplist:
            trendshow.build_payload(kw, timeframe='today '+self.time_scale, geo='')
            dic[i] = trendshow.interest_over_time()
            i += 1

        trendframe = pd.concat(dic, axis=1)
        trendframe.columns = trendframe.columns.droplevel(0)
        trendframe = trendframe.drop('isPartial', axis=1)

        fig = {
            'data': [go.Scatter(
                x=trendframe.index,
                y=trendframe[col], name=col, line=dict(color=self.graph_color)) for col in trendframe.columns],
            'layout': dict(
                #legend=dict(font=dict(color='#7f7f7f')),
                paper_bgcolor='#27293d',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=True
            )
        }

        return dcc.Graph(id=self.graph_id, figure=fig)



    def return_layout(self):
        return self.app.layout
