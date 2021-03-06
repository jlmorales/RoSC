#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import datetime as dt


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
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Call Received', children=[
                dcc.Graph(
                    id='example-graph-3',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [2, 4, 3],
                                'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [5, 4, 3],
                             'type': 'bar', 'name': u'Montréal'},
                        ]
                    }
                ),
                dcc.RangeSlider(
                    marks={i: '{} :00'.format(i) for i in range(0, 24)},
                    min=-0,
                    max=23,
                    value=[0, 23]
                ),
                html.Br(),
                html.Br(),
                dcc.DatePickerRange(
                    id='call-received-status',
                    start_date=dt(2010, 1, 1),
                    end_date_placeholder_text='Select a date!'
                )
        ]),
        dcc.Tab(label='Agent Status', children=[
                dcc.Graph(
                    id='example-graph-4',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [2, 4, 3],
                                'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [5, 4, 3],
                             'type': 'bar', 'name': u'Montréal'},
                        ]
                    }
                ),
                dcc.RangeSlider(
                    marks={i: '{} :00'.format(i) for i in range(0, 24)},
                    min=-0,
                    max=23,
                    value=[0, 23]
                ),
                html.Br(),
                html.Br(),
                dcc.DatePickerRange(
                    id='agent-working-status',
                    start_date=dt(2010, 1, 1),
                    end_date_placeholder_text='Select a date!'
                )
        ]),
        dcc.Tab(label='Agent Working', children=[
                dcc.Graph(
                    id='example-graph-5',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [2, 4, 3],
                                'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [5, 4, 3],
                             'type': 'bar', 'name': u'Montréal'},
                        ]
                    }
                ),
                dcc.RangeSlider(
                    marks={i: '{} :00'.format(i) for i in range(0, 24)},
                    min=-0,
                    max=23,
                    value=[0, 23]
                ),
                html.Br(),
                html.Br(),
                dcc.DatePickerRange(
                    id='agent-working-datepicker',
                    start_date=dt(2010, 1, 1),
                    end_date_placeholder_text='Select a date!'
                )
        ])
    ])
])







server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
