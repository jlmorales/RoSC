#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go


# df = pd.read_csv(
#     'https://gist.githubusercontent.com/chriddyp/'
#     'c78bf172206ce24f77d6363a2d754b59/raw/'
#     'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
#     'usa-agricultural-exports-2011.csv')



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
    return byhr


# 'Call Start Time'

filepath1 = "C4G Agent Activity Detail.xlsx"
col_subset = 'Activity Time'
df = readAndClean(filepath1,col_subset)
df = processData(df,col_subset, '2019-02-02')
df['index'] = range(1, len(df) + 1)

filepath2 = "C4G Call Center Call Detail .xlsx"
col_subset2 = 'Call Start Time'
df2 = readAndClean(filepath2,col_subset2)
df2 = processData(df2,col_subset2, '2019-02-02')
df2['index'] = range(1, len(df2) + 1)






# data = pd.read_excel(filepath)
# df = pd.DataFrame(data)
# data = df.dropna(subset=['Activity Time'])
# data = data[:-1]
#
# ### read and clean the data
# dataframe = data
# dataframe = dataframe.dropna(subset=['Activity Time'])
#
# ## change to datetime
# dataframe['Activity Time'] = pd.to_datetime(dataframe['Activity Time'])
# dataframe['by_hour'] = dataframe['Activity Time'].dt.floor('h')
# dataframe['by_day'] = dataframe['Activity Time'].dt.floor('d')
#
# newdf = dataframe.loc[ dataframe['by_day'] == '2019-02-02']
# byhr = newdf.groupby(['by_hour']).count()
#
# df = byhr



# print(df.columns)
# print(df.dtypes)

# print(mydf.apply(lambda x: x.str.isnumeric()))

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Counts by Hour", style={"textAlign": "center"}),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='product-selected1',
                options=[{'label': i.title(), 'value': i} for i in df.columns.values[1:7]],
                value="Callers/Called Number")], className="six columns", style={"width": "40%", "float": "right"}),
        html.Div([
            dcc.Dropdown(
                id='product-selected2',
                options=[{'label': i.title(), 'value': i} for i in df2.columns.values[1:12]],
                value='Callers Number')], className="six columns", style={"width": "40%", "float": "left"}),

    ], className="row", style={"padding": 50, "width": "60%", "margin-left": "auto", "margin-right": "auto"}),
    dcc.Graph(id='my-graph')

], className="container")







@app.callback(
    dash.dependencies.Output('my-graph', 'figure'),
    [dash.dependencies.Input('product-selected1', 'value'),
     dash.dependencies.Input('product-selected2', 'value')])
def update_graph(selected_product1, selected_product2):
    print(selected_product1)
    print(selected_product2)
    print(df)
    print(df2)
    dff = df[(df[selected_product1] >= 0)]
    dff2 = df2[ (df2[selected_product2] >= 0)]
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
