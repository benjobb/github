# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
pd.core.common.is_list_like = pd.api.types.is_list_like

import pandas_datareader.data as web

app = dash.Dash()

df = pd.read_csv(
    'master df.csv'
    )

categories = df['Category'].unique()

df.sort_values(by=['Date'],inplace=True)
print(df.columns.values)
print(df.dropna(subset=['Index']))
df.dropna(subset=['Index'], inplace=True)

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[len(dataframe)-1-i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    ,style={'width':'60%',
    'border':'1px solid black'})


layout = dict(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=6,
                     label='6m',
                     step='month',
                     stepmode='forward'),
                dict(step='all')
            ])
        ),
        type='date'
    )
)


app.layout = html.Div(children=[
    dcc.Dropdown(
        id='categories-id',
        options=[{'label': i, 'value': i} for i in categories],
        value='Categories'
    ),

    html.H1(children='Index Tracker'),
    generate_table(df),
    dcc.Graph(id='indicator-graphic')
])

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('categories-id', 'value')])


def update_graph(category):
    dff = df[df['Category'] == category]
    return {
        'data': [go.Scatter(
            x=dff['Date'],
            y=dff['Index'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            margin={'l': 40, 'b': 40, 't': 60, 'r': 0},
            hovermode='closest',
            title = category + ' price'
        )


    }

external_css = ["https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css",
                ]
for css in external_css:
    app.css.append_css({"external_url": css})



if __name__ == '__main__':
    app.run_server(debug=True)
