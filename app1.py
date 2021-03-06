import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import altair as alt
from vega_datasets import data
import dash_bootstrap_components as dbc
import pandas as pd
from altair import datum

alt.data_transformers.disable_max_rows()

# Read in global data
suicide = pd.read_csv("master.csv", parse_dates=['year'])
suicide_subset = suicide.query('year >= 1996')
suicide2 = suicide_subset.drop('country-year', axis=1)
suicide_data = suicide2.copy()
#wrangling column names to be more intuitive
suicide_data.columns = ['country', 'year', 'sex', 'age', 'suicides_no', 'population',
       'suicides_per_100k_pop','HDI_for_year','gdp_for_year','gdp_per_capita', 'generation']

# wrangle data for the plot

# AVERAGE SUICIDES PER CAPITA
avg_suicides_per_capita = suicide_data.groupby(['year', 'country', 'sex'])[
                                               'suicides_per_100k_pop'].mean().reset_index()
avg_suicides_per_capita
avg_suicides_per_capita.columns = [
    'year', 'country', 'sex', 'Average_suicides_per_capita']
avg_suicides_per_capita.sort_values(
    'Average_suicides_per_capita', ascending=False, inplace=True)

def avgs_plot_altair(source):
    source = source
    color_scale = alt.Scale(domain=['male', 'female'], range=['#1f77b4', '#e377c2'])
    left = alt.Chart(source).transform_filter(
        datum.sex == 'female'
    ).encode(
        x = alt.X('Average_suicides_per_capita', title = 'Average_suicides_per_capita', 
        sort = alt.SortOrder('descending')),
        color = alt.Color('sex:N', scale = color_scale, legend = None),
        y = alt.Y('country', axis = None)
    ).mark_bar().properties(title = 'Female')

    middle = alt.Chart(source).encode(
            y=alt.Y('country', axis=None),
            text=alt.Text('country')).mark_text().properties(width=120)

    right = alt.Chart(source).transform_filter(
        datum.sex == 'male'
    ).encode(
        y = alt.Y('country', axis = None),
        x = alt.X('Average_suicides_per_capita', title = 'Average_suicides_per_capita'),
        color = alt.Color('sex:N', scale = color_scale, legend = None)
    ).mark_bar().properties(title = 'Male')

    chart = alt.concat(left, middle, right, spacing = 4)
    return chart.to_html()


#avgs_plot_altair(avg_suicides_per_capita)


# Setup app and layout/frontend
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    html.Iframe(
                srcDoc= avgs_plot_altair(avg_suicides_per_capita),
                id = 'scatter',
                style={'border-width': '0', 'width': '100%', 'height': '400px'})
        ])
# Set up callbacks/backend

if __name__ == '__main__':
    app.run_server(debug= True)

