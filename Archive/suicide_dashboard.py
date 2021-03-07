import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import altair as alt

import pandas as pd

suicide_dataset = pd.read_csv('master.csv')
suicide_dataset = suicide_dataset.head(5000)

dropdown_columns = ['country', 'generation', 'age']
calender_columns = ['year']
radio_buttons = ['sex']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
app.layout = dbc.Container([
    html.H1('Global Suicide Dashboard'),
    dbc.Row([
        dbc.Col([
            dcc.RadioItems(
                id='gender-dropdown',
                value='male',
                options=[{'label': col, 'value': col} for col in suicide_dataset['sex'].unique()],
                labelStyle={'display': 'inline-block'}),
            dcc.Dropdown(
                id='year-dropdown',
                value='2010',
                options=[{'label': col, 'value': col} for col in suicide_dataset['year'].unique()]),
            dcc.Dropdown(
                id='country-dropdown',
                value='Albania',
                options=[{'label': col, 'value': col} for col in suicide_dataset['country'].unique()])],
            md=4, style={'border': '1px solid #d3d3d3', 'border-radius': '10px'}),

        dbc.Col(
            html.Iframe(
                id='scatter',
                style={'border-width': '0', 'width': '100%', 'height': '300px'}))])])



# Set up callbacks/backend
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('gender-dropdown', 'value'),
    Input('year-dropdown', 'value'),
    Input('country-dropdown', 'value')
)
def plot_altair(sex, year, country):
    df = suicide_dataset[suicide_dataset['country'] == country]
    df = df[df['sex']==sex]
    df = df[df['year']==year]

    chart = alt.Chart(df).mark_point().encode(
        x='gdp_per_capita ($)',
        y='suicides_no').interactive()
    return chart.to_html()


if __name__ == '__main__':
    app.run_server(debug=True)
