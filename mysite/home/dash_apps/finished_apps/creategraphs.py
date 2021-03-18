import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from jikanpy import Jikan
from pytrends.request import TrendReq
import pandas as pd
# Stores all custom graphs
graphs = []
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('creategraph', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Create New Graph"),
    dcc.Input(id='graphname', type='text', value='Enter Search Term'),
    html.Button(id="creategraph_button", n_clicks=0,children="Add Graph"),
    html.Div(id="graphcontainer")
])

@app.callback (
    Output('graphcontainer','children'),
    [Input('creategraph_button','n_clicks'),
    State('graphname','value')]
)
def create_graph(n_clicks, value):
    trendshow = TrendReq(hl='en-US', tz=360)
    kw_list = [value]
    dic = {}
    trendshow.build_payload(kw_list,timeframe = 'today 5-y',geo='')
    trenddata = trendshow.interest_over_time()
    dic[0] = trenddata

    trendframe = pd.concat(dic,axis=1)
    trendframe.columns = trendframe.columns.droplevel(0)
    trendframe = trendframe.drop('isPartial',axis=1)
    
    fig = {
        'data' : [go.Scatter(
            x = trendframe.index,
            y=trendframe[col], name = col) for col in trendframe.columns],
        'layout' : dict(
            paper_bgcolor='#27293d',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=True
    )

    }
    if(n_clicks > 0):
        graphs.append(dcc.Graph(id='graph-{}'.format(n_clicks), figure=fig))
    
    return html.Div(graphs)