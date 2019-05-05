#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime as dt


def readAndClean(filepath, col):
    #filepath = filepath
    data = pd.read_excel(filepath)
    df = pd.DataFrame(data)
    data = df.dropna(subset=[col])
    data = data[:-1]
    dataframe = data
    dataframe = dataframe.dropna(subset=[col])
    return dataframe

def processData(dataframe, col, day):
    dataframe[col] = pd.to_datetime(dataframe[col])
    dataframe['by_hour'] = dataframe[col].dt.floor('h')
    dataframe['by_day'] = dataframe[col].dt.floor('d')
    newdf = dataframe.loc[dataframe['by_day'] == day]
    return newdf
filepath1 = "C4G Agent Activity Detail.xlsx"
dataframe = readAndClean(filepath1,'Activity Time')
df = processData(dataframe, 'Activity Time', '2019-02-02')



pv = pd.pivot_table(df, index= ["by_hour"],  columns='Activity Detail', margins=False, aggfunc='count', fill_value=0)

status = list(set(list(df['Activity Detail'].T)))

trace = []

for i in range(len(status)):
    trace.append (go.Bar(x=pv.index, y=pv['Agent Name'][status[i]] , name= status[i]))





app = dash.Dash(__name__)






app.layout = html.Div(children=[
    html.H1(children='Agent Activity Report'),
    html.Div(children='''Agent Report By Hour'''),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': trace,
            'layout':
            go.Layout(title='Activity State Count vs Hour', barmode='stack')
        })
])





server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
