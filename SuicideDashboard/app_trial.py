import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

import dash_plots


from data_mugging import clean_data
import pandas as pd

suicide_dataset = pd.read_csv('master.csv')
cleaned_data = clean_data('master.csv')

figure1 = global_suicide_stat = dash_plots.create_world_plot(cleaned_data,
                                                   location='code',
                                                   color='suicides_no',
                                                   hover_name='country')

app = dash.Dash(external_stylesheets=[dbc.themes.SKETCHY])

app.layout = dbc.Container([
    html.H1('Suicide Dashboard',
            style={'text-align': 'center'}),
    html.Br(),
    html.Div(
    [
        dbc.Row(
            [
                dbc.Col([dbc.Card(dbc.CardBody([html.P([

                dcc.Dropdown(
                id='country-dropdown',
                value='Canada',
                options=[{'label': col, 'value': col} for col in cleaned_data['country']]),

                html.Br(),

                dcc.Dropdown(
                id='year-dropdown',
                value='2010',
                options=[{'label': col, 'value': col} for col in suicide_dataset['year'].unique()]),

                html.Br(),

                dcc.Dropdown(
                id='age-dropdown',
                value='15-24 years',
                options=[{'label': col, 'value': col} for col in suicide_dataset['age'].unique()]),

                html.Br(),

                dcc.Dropdown(
                id='generation-dropdown',
                value='Generation X',
                options=[{'label': col, 'value': col} for col in suicide_dataset['generation'].unique()]),

                html.Br(),

                dcc.Checklist(
                id='gender-dropdown',
                value=['male', 'female'],
                options=[{'label': 'Male', 'value': 'male'},
                         {'label': 'Female', 'value': 'female'}],
                labelStyle={'display': 'inline-block', 'cursor': 'pointer', 'margin-left': '20px'})])]))], width=4),

                dbc.Col([dbc.Card(dbc.CardBody([html.P(dcc.Graph(figure=figure1))]))], width=8),
            ]
        ),
        html.Br(),

        html.H3('Socio-economic Factors'),

        dbc.Row(
            [
                dbc.Col([dbc.Card(dbc.CardBody([html.P([
                    dbc.Row([
                        dbc.Col([
                            html.Iframe(
                                id='scatter',
                                style={'border-width': '0', 'width': '100%', 'height': '400px'})]),
                        dbc.Col([
                            html.Iframe(
                                id='scatterv2',
                                style={'border-width': '0', 'width': '100%', 'height': '400px'})])])])]))], width=12)]),
        html.Br(),

        html.H3('Other Factors'),

        dbc.Row(
            [
                dbc.Col([dbc.Card(dbc.CardBody([html.P([
                    dbc.Row([
                        dbc.Col([
                            html.Iframe(
                                srcDoc=dash_plots.plot_suicide_boxplot(country_dropdown='Canada', data=suicide_dataset),
                                id='boxplot',
                                style={'border-width': '0', 'width': '100%', 'height': '400px'}
                            ),
                        ]),
                        ])])]))], width=12)])])])

@app.callback(
    Output('boxplot', 'srcDoc'),
    # Output('barplot', 'srcDoc'),
    [Input('country-dropdown', 'value')])
def update_output(chosencountry):
    return dash_plots.plot_suicide_boxplot(chosencountry, data=suicide_dataset)


@app.callback(
    Output('scatter', 'srcDoc'),
    Input('gender-dropdown', 'value'),
    Input('year-dropdown', 'value'),
    Input('country-dropdown', 'value'),
    Input('age-dropdown', 'value'),
    Input('generation-dropdown', 'value')
)
def update_output2(gender, year, country, age, generation):
    return dash_plots.plot_suicide_gdp(data=suicide_dataset, sex=gender, year=year, country=country, age=age, generation=generation)

@app.callback(
    Output('scatterv2', 'srcDoc'),
    Input('gender-dropdown', 'value'),
    Input('year-dropdown', 'value'),
    Input('country-dropdown', 'value'),
    Input('age-dropdown', 'value'),
    Input('generation-dropdown', 'value')
)
def update_output3(gender, year, country, age, generation):
    return dash_plots.plot_suicide_gdp(data=suicide_dataset, sex=gender, year=year, country=country, age=age, generation=generation)



if __name__ == '__main__':
    app.run_server(debug=True)