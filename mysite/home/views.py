from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
from pytrends.request import TrendReq
import pandas as pd


# Create your views here.

def home(request):
    def scatter():
        trendshow = TrendReq(hl='en-US', tz=360)
        kw_list = ["Halo", "CSGO", "League Of Legends", "Fortnite"]
        kw_group = list(zip(*[iter(kw_list)]*1))
        kw_grplist = [list(x) for x in kw_group]
        dic = {}
        i=0
        for kw in kw_grplist:
            trendshow.build_payload(kw,timeframe = 'today 5-y',geo='')
            dic[i] = trendshow.interest_over_time()
            i +=1

        trendframe = pd.concat(dic,axis=1)
        trendframe.columns = trendframe.columns.droplevel(0)
        trendframe = trendframe.drop('isPartial',axis=1)
        
        
        trace = [go.Scatter(
            x = trendframe.index,
            y=trendframe[col], name = col) for col in trendframe.columns]
        layout = dict(
            title='Test Graph'
        )
        fig = go.Figure(data=trace, layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div
        
        """x1 = [1,2,3,4]
        y1 = [30,35,25,45]

        trace = go.Scatter(
            x=x1,
            y=y1
        )
        layout = dict(
            title='Simple Graph',
            xaxis=dict(range=[min(x1), max(x1)]),
            yaxis=dict(range=[min(y1), max(y1)])
        )
        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div"""

    context = {
        'plot': scatter()
    }

    return render(request, 'home/welcome.html', context)
