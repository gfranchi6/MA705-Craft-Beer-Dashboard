# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 08:34:22 2021
@author: Gaby

"""

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


df = pd.read_csv(r"C:\Users\Gaby\Downloads\beer_reviews.csv")
df.replace('?', np.NaN)

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


### pandas dataframe to html table

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app = dash.Dash(__name__, external_stylesheets=stylesheet)

fig = px.bar(df, x="beer_name", y="review_overall", color="beer_style")
fig.update_layout(title = 'Overall Review Score',
                  xaxis_title = 'Beer Name',
                  yaxis_title = 'Overall Score')

app.layout = html.Div(id = 'parent', children = [
    html.H1('International Beer Reviews', style={'textAlign' : 'center'}),
    dcc.Graph(figure=fig, id='beer_plot'),
    html.Div([html.H4('Beers to Display:'),
              dcc.Dropdown(id='style_dropdown',
                           options=[{'label': i, 'value': i} for i in df.beer_style.unique()],
                           multi=True,
                           value=[],
                           placeholder='Filter by Beer Style...')]),
    html.Label('ABV Range:', style={'paddingTop': '2rem'}),
    dcc.RangeSlider(id='abv_slider',
                    min=0,
                    max=60,
                    step=0.5,
                    tooltip = { 'always_visible': True },
                    value=[0, 60]),
    html.Div(id="beer_table")
    ])
    
server = app.server

@app.callback(
    Output(component_id="beer_plot", component_property="figure"),
    [Input(component_id="style_dropdown", component_property="value")]
)
def update_plot(beers):
    df2 = df[df.beer_style.isin(beers)].sort_values('review_overall', ascending=False)
    fig = px.bar(df2, x="beer_name", y="review_overall", color="beer_style")
    return fig
    
@app.callback(
    Output(component_id="beer_table", component_property="children"),
    [Input(component_id="style_dropdown", component_property="value"),
     Input(component_id="abv_slider", component_property="value")]
)
def update_table(beers, abvs):
    df2 = df[df.beer_style.isin(beers)].sort_values('review_overall')
    df2 = df2[(df2.beer_abv >= abvs[0]) & (df2.beer_abv <= abvs[1])]
    return generate_table(df2)


if __name__ == '__main__':
    app.run_server(debug=False)

    



    

    
