import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

fifa_data = pd.DataFrame([
    {'Year': 1930, 'Winner': 'Uruguay', 'Runner-Up': 'Argentina'},
    {'Year': 1934, 'Winner': 'Italy', 'Runner-Up': 'Czechoslovakia'},
    {'Year': 1938, 'Winner': 'Italy', 'Runner-Up': 'Hungary'},
    {'Year': 1950, 'Winner': 'Uruguay', 'Runner-Up': 'Brazil'},
    {'Year': 1954, 'Winner': 'Germany', 'Runner-Up': 'Hungary'},
    {'Year': 1958, 'Winner': 'Brazil', 'Runner-Up': 'Sweden'},
    {'Year': 1962, 'Winner': 'Brazil', 'Runner-Up': 'Czechoslovakia'},
    {'Year': 1966, 'Winner': 'England', 'Runner-Up': 'West Germany'},
    {'Year': 1970, 'Winner': 'Brazil', 'Runner-Up': 'Italy'},
    {'Year': 1974, 'Winner': 'Germany', 'Runner-Up': 'Netherlands'},
    {'Year': 1978, 'Winner': 'Argentina', 'Runner-Up': 'Netherlands'},
    {'Year': 1982, 'Winner': 'Italy', 'Runner-Up': 'Germany'},
    {'Year': 1986, 'Winner': 'Argentina', 'Runner-Up': 'Germany'},
    {'Year': 1990, 'Winner': 'Germany', 'Runner-Up': 'Argentina'},
    {'Year': 1994, 'Winner': 'Brazil', 'Runner-Up': 'Italy'},
    {'Year': 1998, 'Winner': 'France', 'Runner-Up': 'Brazil'},
    {'Year': 2002, 'Winner': 'Brazil', 'Runner-Up': 'Germany'},
    {'Year': 2006, 'Winner': 'Italy', 'Runner-Up': 'France'},
    {'Year': 2010, 'Winner': 'Spain', 'Runner-Up': 'Netherlands'},
    {'Year': 2014, 'Winner': 'Germany', 'Runner-Up': 'Argentina'},
    {'Year': 2018, 'Winner': 'France', 'Runner-Up': 'Croatia'},
    {'Year': 2022, 'Winner': 'Argentina', 'Runner-Up': 'France'},
])

fifa_data.replace({'West Germany': 'Germany'}, inplace= True)
count_wins = fifa_data['Winner'].value_counts().reset_index()
count_wins.columns = ['Country', 'Wins']


app = dash.Dash(__name__)

server = app.server

app.title = "Fifa World Cup Winner Dashboard"

app.layout = html.Div([

    html.H1("FIFA World Cup Winner Dashboard", style = {'textAlign': 'center'}),
    dcc.Graph(id = 'world-cup-map'),
    html.Label("select a country: "), 
    dcc.Dropdown(
        id = 'country-dropdown',
        options = [{'label': country, 'value': country} for country in count_wins['Country']],
        value = 'Brazil'

    ),
    html.Div( id = 'country-wins'),

    html.Label("select a year:"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in sorted(fifa_data['Year'])],
        value=2022
    ),
    html.Div(id='year-result')


])

@app.callback(
    Output('world-cup-map',  'figure'), 
    Input('country-dropdown', 'value')

)

def update_map(selected_country):
    fig = px.choropleth(
        count_wins,
        locations="Country",
        locationmode='country names',
        color="Wins",
        hover_name="Country",
        color_continuous_scale=px.colors.sequential.Plasma,
        title="FIFA World Cup Wins by Country"
    )
    return fig

@app.callback(
    Output('country-wins', 'children'),
    Input('country-dropdown', 'value')
)

def update_country_wins(selected_country):
    wins = count_wins[count_wins['Country'] == selected_country]['Wins'].values
    return html.H3(f"{selected_country} has won {wins[0]} times" if len(wins) > 0 else f"{selected_country} has not won a World Cup.")


@app.callback(
    Output('year-result', 'children'),
    Input('year-dropdown', 'value')
)
def update_year_result(selected_year):
    result = fifa_data[fifa_data['Year'] == selected_year]
    if not result.empty:
        return html.H3(f"{selected_year}: Winner - {result['Winner'].values[0]}, Runner-Up - {result['Runner-Up'].values[0]}")
    return html.H3("No data available.")


# runs app
if __name__ == '__main__':
    app.run_server(debug=True)

