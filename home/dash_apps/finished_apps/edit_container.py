import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash
from home.models import Anime
import configparser
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        'https://www.dl.dropboxusercontent.com/s/99knran9jmm5beo/plotly-dash.css']


class Edit_Container:

    def __init__(self, id: str, shared_info):
        self.shared_info = shared_info
        self.shared_info.pending_updates_edit = True
        # self.graphs_list = []
        self.app = DjangoDash(id, external_stylesheets=external_stylesheets)
        self.table = dash_table.DataTable()
        self.status_default = "Status: No changes made yet; feel free to update settings."
        self.app.layout = self.serve_layout
        self.start_data = []

        @self.app.callback(
            [Output('table', 'data'),
             Output('table', 'dropdown'),
             Output('status_message', 'children')],
            [Input('remove_graphs', 'n_clicks'),
             State('line_color_dropdown', 'value'),
             State('time_range_dropdown', 'value'),
             State('table', 'data')])
        def remove_graphs(n_clicks, line_color, time_scale, value):

            # Reset table data
            graphs_to_keep = []
            order_to_keep = []
            children = self.status_default

            if n_clicks > 0 and (
                    value != self.start_data or line_color != self.shared_info.color_graphs or time_scale != self.shared_info.time_scale):
                self.shared_info.pending_updates_main = True

                if value != self.start_data:
                    self.shared_info.pending_updates_export = True

                for i in value:
                    if i['Remove Graph(s)'] == 'Remove Graph':
                        pass
                    else:
                        graphs_to_keep.append(i['Name'])
                        order_to_keep.append(int(i['Order']))

                sorted_graphs_to_keep = [x for _, x in
                                         sorted(zip(order_to_keep, graphs_to_keep), key=lambda pair: pair[0])]
                Anime.objects.all().delete()

                num_graphs = 0

                for name in sorted_graphs_to_keep:
                    num_graphs = num_graphs + 1
                    a = Anime(anime_name=name, anime_order=num_graphs)
                    a.save()

                if line_color != self.shared_info.color_graphs:
                    config = configparser.ConfigParser()
                    path = os.path.join(os.path.dirname(__file__), 'config.ini')
                    config.read(path)
                    config['SETTINGS']['color'] = line_color
                    with open(path, 'w') as configfile:
                        config.write(configfile)
                    self.shared_info.color_graphs = line_color
                    self.shared_info.pending_updates_main = True

                if time_scale != self.shared_info.time_scale:
                    config = configparser.ConfigParser()
                    path = os.path.join(os.path.dirname(__file__), 'config.ini')
                    config.read(path)
                    config['SETTINGS']['time_scale'] = time_scale
                    with open(path, 'w') as configfile:
                        config.write(configfile)
                    self.shared_info.time_scale = time_scale
                    self.shared_info.pending_updates_main = True

                children = "Status: Settings updated correctly. Duplicate or invalid re-orders (if any) were re-assigned."

            # Update dropdown based on new objects
            dropdown = self.init_dropdown()

            # Update table data to reflect database
            data = self.init_data()

            return data, dropdown, children

    def serve_layout(self):
        if self.shared_info.pending_updates_edit:
            self.shared_info.pending_updates_edit = False
            self.table = self.init_table('Remove', 5)

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
            html.P(id='status_message', children=self.status_default, style={'font-style': 'italic'}),
            html.Button('Submit Changes', id="remove_graphs", n_clicks=0)
        ])

    def init_table(self, type: str = 'Add', pg_size: int = 5):
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
                     {"name": type + ' Graph(s)',
                      "id": type + ' Graph(s)',
                      "presentation": "dropdown",
                      "editable": True},
                     {"name": "Order",
                      "id": "Order",
                      "presentation": "dropdown",
                      "editable": True}],
            dropdown=self.init_dropdown(),
            data=self.init_data(),
            page_size=pg_size,
        )

        return layout

    def init_data(self):
        self.start_data = []
        # self.graphs_list = []
        for a in Anime.objects.raw('SELECT anime_name FROM home_anime ORDER BY anime_order ASC'):
            # self.graphs_list.append(str(a))
            self.start_data.append(
                {'Name': a.anime_name, 'Remove Graph(s)': "Don't remove Graph", 'Order': a.anime_order})
        return self.start_data

    def init_dropdown(self):
        options = []

        for i in range(1, Anime.objects.count() + 1):
            options.append({'label': str(i) + "⠀⠀", 'value': i})

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

        return dropdown