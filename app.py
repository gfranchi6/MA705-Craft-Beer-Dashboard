# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 15:32:33 2021

@author: Gaby
"""

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc


df = pd.read_csv('https://raw.githubusercontent.com/gfranchi6/MA705-Craft-Beer-Dashboard/main/beer_reviews.csv?token=AW5PDJTUV4FGTOLSSZJNBOTBXT44E')

df.replace('?', np.NaN)


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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

fig = px.bar(df, x="beer_name", y="review_overall", color="beer_style")
fig.update_layout(title = 'Overall Review Score',
                  xaxis_title = 'Beer Name',
                  yaxis_title = 'Overall Score')

app.layout = html.Div(id = 'parent', children = [
    html.H1('International Beer Reviews', style={'textAlign' : 'center'}),
    html.H6('The purpose of this dashboard is to help users find a craft beer they’ll love! This dashboard features nearly 38,000 beers, which means something for everyone! The below graph shows the names of different beers, the style of the beers and their overall rating from beer drinkers around the globe. There are two ways to filter your results and find a beer you’ll love; by using the dropdown tab below to select your preferred style(s) of beer and by using the slider below to indicate your preferred ABV range (or combine both!). The table will update to show you details about the beers, including the brewery they’re made in, the aroma, appearance, palate and taste scores while the graph will show you the overall score and the type/style of beer (indicated by color). Have fun exploring all of the amazing international craft beers there are to find! (And please enjoy responsibly).', style={'textAlign' : 'center'}),
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
    [Input(component_id="style_dropdown", component_property="value"),
    Input(component_id="abv_slider", component_property="value")]
)
def update_plot(beers, abvs):
    df2 = df[df.beer_style.isin(beers)].sort_values('review_overall', ascending=False)
    df2 = df2[(df2.beer_abv >= abvs[0]) & (df2.beer_abv <= abvs[1])]
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
