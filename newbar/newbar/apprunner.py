#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import time
from datetime import datetime as dt
from dash.dependencies import Input, Output


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

dataframe2 = readAndClean(filepath1,'Activity Time')
col ="Activity Time"
dataframe2[col] = pd.to_datetime(dataframe2[col])
dataframe2['by_day'] = dataframe2[col].dt.floor('d')
days = dataframe2["by_day"].unique()

pv = pd.pivot_table(df, index= ["by_hour"],  columns='Activity Detail', margins=False, aggfunc='count', fill_value=0)
status = list(set(list(df['Activity Detail'].T)))
trace = []
for i in range(len(status)):
    trace.append (go.Bar(x=pv.index, y=pv['Agent Name'][status[i]] , name= status[i]))

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Agent Activity Report'),
    html.Div(children='''Agent Report By Hour'''),
    html.Div([
        dcc.Dropdown(
        id = 'daydropdown',
        options=[{'label': str(pd.to_datetime(i).date()), 'value': str(pd.to_datetime(i).date())} for i in days],
        value = '2019-02-02'
    )]),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': trace,
            'layout':
            go.Layout(title='Activity State Count vs Hour', barmode='stack')
        }),
    dcc.RangeSlider(
        id = 'slider',
        min = 0,
        max = 23,
        value = [0,23],
        marks = {i: str(i) for i in range(0,24)}
    )
    
    
])

@app.callback(Output('example-graph', 'figure'),
             [Input('slider', 'value'),
            Input('daydropdown', 'value')])
def update_figure(X,day):
    df = processData(dataframe, 'Activity Time', day)
    pv = pd.pivot_table(df, index= ["by_hour"],  columns='Activity Detail', margins=False, aggfunc='count', fill_value=0)
    pv2 = pv[int(X[0]):int(X[1])]
    status2 = list(set(list(df['Activity Detail'].T)))
    trace_1 = []
    for i in range(len(status2)):
        trace_1.append(go.Bar(x=pv2.index, y=pv2['Agent Name'][status2[i]] , name= status2[i]))
    return {
        'data' : trace_1,
        'layout': go.Layout(title='Activity State Count vs Hour', barmode='stack')
    }

# @app.callback(Output('example-graph', 'figure'),
#             [Input('daydropdown', 'value')])
# def update_day(day):
#     print(day)
#     df2 = processData(dataframe, 'Activity Time', day)
#     pv = pd.pivot_table(df2, index= ["by_hour"],  columns='Activity Detail', margins=False, aggfunc='count', fill_value=0)
#     status = list(set(list(df2['Activity Detail'].T)))
#     trace = []
#     for i in range(len(status)):
#         trace.append (go.Bar(x=pv.index, y=pv['Agent Name'][status[i]] , name= status[i]))
#     return {
#         'data' : trace,
#         'layout': go.Layout(title='Activity State Count vs Hour', barmode='stack')
#     }

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
