import plotly as py
import plotly.graph_objs as go

import json

def plot_pie(values, labels, colors=None):
    trace = go.Pie(labels=labels, values=values, marker=dict(colors=colors))

    graphJSON = json.dumps([trace], cls=py.utils.PlotlyJSONEncoder)
    return graphJSON


def plot_bar(values, labels):
    data = [go.Bar(x=labels, y=values)]

    graphJSON = json.dumps(data, cls=py.utils.PlotlyJSONEncoder)
    return graphJSON

# TODO: Za ovo je potrebno pandas koristiti
def plot_timeseries(df, naziv, parametar):
    trace = go.Scatter(
        x=df.date,
        y=df[parametar],
        name=naziv,
        line=dict(color='#e8067f'),
        opacity=0.8)

    data = [trace]

    layout = dict(
        height='100%',
        title='Neki pandas timeseries',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(
                        count=1, label='1m', step='month',
                        stepmode='backward'),
                    dict(
                        count=6, label='6m', step='month',
                        stepmode='backward'),
                    dict(step='all')
                ])),
            rangeslider=dict(visible=True),
            type='date'))

    fig = dict(data=data, layout=layout)
    graphJSON = json.dumps(fig, cls=py.utils.PlotlyJSONEncoder)
    return graphJSON