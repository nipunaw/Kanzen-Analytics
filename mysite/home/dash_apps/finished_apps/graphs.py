import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from jikanpy import Jikan
from pytrends.request import TrendReq
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


class Graphs:
    def __init__(self, app_name, graph_title, graph_id, slider_id, top_bool, app_input_state_list, anime_name="default"):
        self.jikan = Jikan()

        def get_top_anime_names(rank: int, subtype: str):
            top_anime = self.jikan.top(type='anime', page=1, subtype=subtype)
            return top_anime["top"][rank]["title"]

        def search_anime(anime_name):
            search = self.jikan.search('anime', anime_name)
            return search["results"][0]["title"]


        self.app = DjangoDash(app_name, external_stylesheets=external_stylesheets)

        self.app.layout = html.Div([
            html.H1(graph_title), #
            # html.Button("Custom export", id="export_table", **{"data-dummy": ""}),
            dcc.Graph(id=graph_id, animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
            dcc.Slider(
                id=slider_id,
                marks={i: '{}'.format(i) for i in range(20)},
                max=20,
                value=2,
                step=1,
                updatemode='drag',
                min=0,
            ),
        ])

        # self.app.clientside_callback(
        #     """
        #     function(n_clicks) {
        #         if (n_clicks > 0)
        #             document.querySelector("#slider-graph a.modebar-btn").click()
        #         return ""
        #     }
        #     """,
        #     Output("export_table", "data-dummy"),
        #     [Input("export_table", "n_clicks")]
        # )

        @self.app.callback(
            Output(graph_id, 'figure'),
            app_input_state_list)
        def display_value(value):

            trendshow = TrendReq(hl='en-US', tz=360)

            kw_list = []
            if top_bool:
                for k in range(0, 5):
                    kw_list.append(get_top_anime_names(k, 'tv'))
            else:
                kw_list.append(search_anime(anime_name))
            kw_group = list(zip(*[iter(kw_list)] * 1))
            kw_grplist = [list(x) for x in kw_group]
            dic = {}
            i = 0
            for kw in kw_grplist:
                trendshow.build_payload(kw, timeframe='today 12-m', geo='')
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
            )
            return {'data': trace, 'layout': layout}


        # def display_value(value):
        #
        #     x = []
        #     for i in range(value):
        #         x.append(i)
        #
        #     y = []
        #     for i in range(value):
        #         y.append(i * i)
        #
        #     graph = go.Scatter(
        #         x=x,
        #         y=y,
        #         name='Manipulate Graph'
        #     )
        #     layout = go.Layout(
        #         paper_bgcolor='#27293d',
        #         plot_bgcolor='rgba(0,0,0,0)',
        #         xaxis=dict(range=[min(x), max(x)]),
        #         yaxis=dict(range=[min(y), max(y)]),
        #         font=dict(color='white'),
        #
        #     )
        #     return {'data': [graph], 'layout': layout}