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
    byhr = newdf.groupby(['by_hour']).count()
    return newdf

def processData2(dataframe, col, day):
    dataframe[col] = pd.to_datetime(dataframe[col])
    dataframe['by_hour'] = dataframe[col].dt.floor('h')
    dataframe['by_day'] = dataframe[col].dt.floor('d')
    newdf = dataframe.loc[dataframe['by_day'] == day]
    byhr = newdf.groupby(['by_hour']).count()
    return byhr

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

filepath1 = "C4G Agent Activity Detail.xlsx"
col_subset = 'Activity Time'
df3 = readAndClean(filepath1,col_subset)
df3 = processData2(df3,col_subset, '2019-02-02')
df3['index'] = range(1, len(df3) + 1)
print(df3)
print(df3.columns)



filepath2 = "C4G Call Center Call Detail .xlsx"
col_subset2 = 'Call Start Time'
df4 = readAndClean(filepath2,col_subset2)
df4 = processData2(df4,col_subset2, '2019-02-02')
df4['index'] = range(1, len(df4) + 1)
print(df4)
print(df4.columns)

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Tab one', children=[
            
            html.H1("Counts by Hour", style={"textAlign": "center"}),
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='product-selected1',
                        options=[{'label': i.title(), 'value': i} for i in df3.columns.values[5:6]],
                        value="Callers/Called Number")], className="six columns", style={"width": "40%", "float": "right"}),
            html.Div([
                    dcc.Dropdown(
                        id='product-selected2',
                        options=[{'label': i.title(), 'value': i} for i in df4.columns.values[1:4]],
                        value='Callers Number')], className="six columns", style={"width": "40%", "float": "left"}),

            ], className="row", style={"padding": 50, "width": "60%", "margin-left": "auto", "margin-right": "auto"}),
            dcc.Graph(id='my-graph')

        ]),
        dcc.Tab(label='Tab two', children=[
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
    ])
])

# app.layout = html.Div(children=[
#     html.H1(children='Agent Activity Report'),
#     html.Div(children='''Agent Report By Hour'''),
#     html.Div([
#         dcc.Dropdown(
#         id = 'daydropdown',
#         options=[{'label': str(pd.to_datetime(i).date()), 'value': str(pd.to_datetime(i).date())} for i in days],
#         value = '2019-02-02'
#     )]),
#     dcc.Graph(
#         id='example-graph',
#         figure={
#             'data': trace,
#             'layout':
#             go.Layout(title='Activity State Count vs Hour', barmode='stack')
#         }),
#     dcc.RangeSlider(
#         id = 'slider',
#         min = 0,
#         max = 23,
#         value = [0,23],
#         marks = {i: str(i) for i in range(0,24)}
#     )
# ])

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

@app.callback(
    dash.dependencies.Output('my-graph', 'figure'),
    [dash.dependencies.Input('product-selected1', 'value'),
     dash.dependencies.Input('product-selected2', 'value')])
def update_graph(selected_product1, selected_product2):
    print(df3)
    print(df4)
    
    dff = df3[(df3[selected_product1] >= 0)]
    dff2 = df4[(df4[selected_product2] >= 0)]
    trace1 = go.Bar(
        x=dff['index'],
        y=dff[selected_product1],
        name=selected_product1.title(),
        marker={

        }
    )
    trace2 = go.Bar(
        x=dff['index'],
        y=dff2[selected_product2],
        name=selected_product2.title(),
        marker={

        }
    )

    return {
        'data': [trace1, trace2],
        'layout': go.Layout(
            title=f'Counts vs Hour: {selected_product1.title()}, {selected_product2.title()}',
            colorway=["#EF963B", "#EF533B"],
            hovermode="closest",
            xaxis={
                'title': "Hour",
                'titlefont': {
                    'color': 'black',
                    'size': 14},
                'tickfont': {
                    'size': 9,
                    'color': 'black'

                }
            },
            yaxis={
                'title': "Count",
                'titlefont': {
                    'color': 'black',
                    'size': 14,

                },

                'tickfont': {
                    'color': 'black'

                }
            }

        )

    }

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
