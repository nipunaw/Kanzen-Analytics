import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import date
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from jikanpy import Jikan

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets)



def get_names():
    aio_jikan_2 = Jikan()
    top_anime = aio_jikan_2.top(type='anime', page=1, subtype='tv')
    return top_anime["top"][0]["title"]


app.layout = html.Div([
    html.H1(get_names()),
    html.Button("Custom export", id="export_table", **{"data-dummy": ""}),
    dcc.Graph(id='slider-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
    dcc.Slider(
        id='slider-updatemode',
        marks={i: '{}'.format(i) for i in range(20)},
        max=20,
        value=2,
        step=1,
        updatemode='drag',
        min=0,
    ),

    html.Div(dcc.Input(id='input-box', placeholder='Search:', type='text')),

    html.Button('Apply Filters', id='button'),

html.Div(id='output-container-button',
             children='Genre:'),

dcc.Dropdown(
        options=[
            {'label': 'Any', 'value': '1'},
            {'label': 'Action', 'value': '2'},
            {'label': 'Adventure', 'value': '3'},
            {'label': 'BL', 'value': '4'},
            {'label': 'Comedy', 'value': '5'},
            {'label': 'Drama', 'value': '6'},
        ],
        value='1'
    ),

html.Div(id='output-container-button',
             children='Category:'),

dcc.Dropdown(
        options=[
            {'label': 'Any', 'value': '1'},
            {'label': 'Movie', 'value': '2'},
            {'label': 'TV', 'value': '3'},
            {'label': 'Manga', 'value': '4'},
        ],
        value='1'
    ),

html.Div(id='output-container-button',
             children='Select the range of data:'),

    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=date(2020, 3, 23),
        end_date_placeholder_text='Select a date!'
    ),

])


@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(value):
    return 'Filtered By: "{}" '.format(
        value
    )

if __name__ == '__main__':
    app.run_server(debug=True)




app.clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks > 0)
            document.querySelector("#slider-graph a.modebar-btn").click()
        return ""
    }
    """,
    Output("export_table", "data-dummy"),
    [Input("export_table", "n_clicks")]
)

@app.callback(
               Output('slider-graph', 'figure'),
              [Input('slider-updatemode', 'value')])
def display_value(value):


    x = []
    for i in range(value):
        x.append(i)

    y = []
    for i in range(value):
        y.append(i*i)

    graph = go.Scatter(
        x=x,
        y=y,
        name='Manipulate Graph'
    )
    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[min(x), max(x)]),
        yaxis=dict(range=[min(y), max(y)]),
        font=dict(color='white'),

    )
    return {'data': [graph], 'layout': layout}


