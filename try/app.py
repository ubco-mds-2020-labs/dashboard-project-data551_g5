
import dash 
import dash_html_components as html
import plotly.express as px
import pycountry
import pandas as pd
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output
import altair as alt
from altair import datum

# Initialise the app
app = dash.Dash(__name__)

# load the dataset
data = pd.read_csv("master.csv")

# Do the required wrangling:


### Extract only the required columns from the dataframe:
data_filtered = data[['country', 'suicides_no']]
data_filtered = data_filtered.groupby(['country']).sum().sort_values(by=['suicides_no'],ascending=False)
data_filtered = data_filtered.reset_index()

# Retrive only the column that contains the countries:
list_countries = data_filtered['country'].unique().tolist()


d_country_code = {} # to hold the country names and their ISO

for country in list_countries:
    try:
        country_data = pycountry.countries.search_fuzzy(country)
        country_code = country_data[0].alpha_3
        d_country_code.update({country: country_code})
    except:
        d_country_code.update({country: country_code})

df_1 = pd.DataFrame.from_dict(d_country_code, orient="index")
df_1= df_1.reset_index()
df_1.columns=['country', 'code']

data_filtered['code'] = df_1['code']


# Create the graph
fig_map = px.choropleth(data_filtered, locations="code",
                    color="suicides_no", # lifeExp is a column of gapminder
                    hover_name="country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma,
                    width=300, height=400)

fig_map.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
    width= 700,
    paper_bgcolor="Black",
)

# Define the code for box-plots
def plot_altair(country_dropdown):
    data_country_filter = data[data['country'] == country_dropdown]
    chart = alt.Chart(data_country_filter).mark_boxplot().encode(
    x='suicides/100k pop',  
    y= 'generation',
    fill = 'generation'
    ).interactive()
    return chart.to_html()

####### Poojitha's code:

suicide = data.copy()
suicide_subset = suicide.query('year >= 1996')
suicide2 = suicide_subset.drop('country-year', axis=1)
suicide_data = suicide2.copy()
#wrangling column names to be more intuitive
suicide_data.columns = ['country', 'year', 'sex', 'age', 'suicides_no', 'population',
       'suicides_per_100k_pop','HDI_for_year','gdp_for_year','gdp_per_capita', 'generation']

# AVERAGE SUICIDES PER CAPITA
avg_suicides_per_capita = suicide_data.groupby(['year', 'country', 'sex'])[
                                               'suicides_per_100k_pop'].mean().reset_index()
avg_suicides_per_capita
avg_suicides_per_capita.columns = [
    'year', 'country', 'sex', 'Average_suicides_per_capita']
avg_suicides_per_capita.sort_values(
    'Average_suicides_per_capita', ascending=False, inplace=True)


####### PLOTS for poojitha:

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



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = dbc.Container([
    html.H1("Sucide Dashboard"),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id= 'country_dropdown',
                value= 'Canada',
                options = [{'label': col, 'value': col} for col in list_countries]
                )
        ],md=2),
        dbc.Col([
            html.Div(
                dcc.Graph(id = 'world', figure= fig_map)
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Iframe(
            srcDoc = plot_altair(country_dropdown= 'Canada'),
            id = 'boxplot',
            style = {'border-width':'0', 'width':'200%', 'height':'400px'})
        ]),
        dbc.Col([
           # Poojitha
           html.Iframe(srcDoc= avgs_plot_altair(avg_suicides_per_capita),
                        id = 'barplot',
                        style = {'border-width':'0', 'width':'100%', 'height':'400px'})
        ])
    ])

])

@app.callback(
    Output('boxplot','srcDoc'),
    Output('barplot','srcDoc'),
    [Input('country_dropdown','value')]
    
)
def update_output(chosencountry):
    return plot_altair(chosencountry)



if __name__ == '__main__':
    app.run_server(debug=True)





