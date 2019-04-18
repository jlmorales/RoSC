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

filepath = "C4G Agent Activity Detail.xlsx"
data = pd.read_excel(filepath)
df = pd.DataFrame(data)
data = df.dropna(subset=['Activity Time'])
data = data[:-1]

### read and clean the data
dataframe = data
dataframe = dataframe.dropna(subset=['Activity Time'])

## change to datetime
dataframe['Activity Time'] = pd.to_datetime(dataframe['Activity Time'])
dataframe['by_hour'] = dataframe['Activity Time'].dt.floor('h')
dataframe['by_day'] = dataframe['Activity Time'].dt.floor('d')

newdf = dataframe.loc[ dataframe['by_day'] == '2019-02-02']
byhr = newdf.groupby(['by_hour']).count()

df = byhr

df['index'] = range(1, len(df) + 1)

# print(df.columns)
# print(df.dtypes)

# print(mydf.apply(lambda x: x.str.isnumeric()))

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Call counts by Hour", style={"textAlign": "center"}),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='product-selected1',
                options=[{'label': i.title(), 'value': i} for i in df.columns.values[1:7]],
                value="Callers/Called Number")], className="six columns", style={"width": "40%", "float": "right"}),
        html.Div([
            dcc.Dropdown(
                id='product-selected2',
                options=[{'label': i.title(), 'value': i} for i in df.columns.values[1:7]],
                value='Number Called')], className="six columns", style={"width": "40%", "float": "left"}),

    ], className="row", style={"padding": 50, "width": "60%", "margin-left": "auto", "margin-right": "auto"}),
    dcc.Graph(id='my-graph')

], className="container")


@app.callback(
    dash.dependencies.Output('my-graph', 'figure'),
    [dash.dependencies.Input('product-selected1', 'value'),
     dash.dependencies.Input('product-selected2', 'value')])
def update_graph(selected_product1, selected_product2):
    dff = df[(df[selected_product1] >= 0) & (df[selected_product2] >= 0)]

    trace1 = go.Bar(
        x=dff['index'],
        y=dff[selected_product1],
        name=selected_product1.title(),
        marker={

        }
    )
    trace2 = go.Bar(
        x=dff['index'],
        y=dff[selected_product2],
        name=selected_product2.title(),
        marker={

        }
    )

    return {
        'data': [trace1, trace2],
        'layout': go.Layout(
            title=f'Calls vs Hour: {selected_product1.title()}, {selected_product2.title()}',
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
                'title': "Call count",
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
