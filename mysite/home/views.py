from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
# Create your views here.

def home(request):
    # def scatter():
    #     x1 = [1,2,3,4]
    #     y1 = [30,35,25,45]
    #
    #     trace = go.Scatter(
    #         x=x1,
    #         y=y1
    #     )
    #     layout = dict(
    #         title='Simple Graph',
    #         xaxis=dict(range=[min(x1), max(x1)]),
    #         yaxis=dict(range=[min(y1), max(y1)])
    #     )
    #     fig = go.Figure(data=[trace], layout=layout)
    #     plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    #     return plot_div
    #
    # context = {
    #     'plot': scatter()
    # }

        trace = go.Scatter(
            x=x1,
            y=y1
        )
        layout = dict(
            title='Top 5 Results:',
            xaxis=dict(range=[min(x1), max(x1)]),
            yaxis=dict(range=[min(y1), max(y1)])
        )
        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    context = {
        'plot': scatter()
    }

    return render(request, 'home/index_load.html', context)

def edit(request):
    return render(request, 'home/edit_load.html')

def export(request):
    return render(request, 'home/export_load.html')
