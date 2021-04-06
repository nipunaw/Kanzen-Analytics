from home.dash_apps.finished_apps import graphs
from home.dash_apps.finished_apps import container
from dash.dependencies import Input, Output, State


initial_graphs = []
top_shows = graphs.Graphs('SimpleExample', 'Top 5 Anime', 'topanime', 'topanimeslider', True, [Input('topanimeslider', 'value')])

initial_graphs.append(top_shows)

container_object = container.Container('container',initial_graphs,False)

edit_page_container = container.Container('edit_container',[],True)
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output
# import plotly.graph_objs as go
# from django_plotly_dash import DjangoDash
# from jikanpy import Jikan
#
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#
# app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets)
#
#
# def get_names():
#     aio_jikan_2 = Jikan()
#     top_anime = aio_jikan_2.top(type='anime', page=1, subtype='tv')
#     return top_anime["top"][0]["title"]
#
#
# app.layout = html.Div([
#     html.H1(get_names()),
#     html.Button("Custom export", id="export_table", **{"data-dummy": ""}),
#     dcc.Graph(id='slider-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
#     dcc.Slider(
#         id='slider-updatemode',
#         marks={i: '{}'.format(i) for i in range(20)},
#         max=20,
#         value=2,
#         step=1,
#         updatemode='drag',
#         min=0,
#     ),
# ])
#
# app.clientside_callback(
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
#
# @app.callback(
#                Output('slider-graph', 'figure'),
#               [Input('slider-updatemode', 'value')])
# def display_value(value):
#
#
#     x = []
#     for i in range(value):
#         x.append(i)
#
#     y = []
#     for i in range(value):
#         y.append(i*i)
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