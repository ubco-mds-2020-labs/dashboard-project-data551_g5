
# Load the required imports

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import altair as alt
import numpy
import pandas as pd
import pycountry
import plotly.express as px


# Load the required dataset

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


print(data_filtered.head(2))

# Create a world map after all the wrangling:
fig_map = px.choropleth(data_filtered, locations="code",
                    color="suicides_no", # lifeExp is a column of gapminder
                    hover_name="country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma,
                    width=800, height=400)

fig_map.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
    width= 1000,
    paper_bgcolor="LightBlue",
)


# Create a boxplot map that varies with the input value:
alt.data_transformers.disable_max_rows()
data = data[data.year > 1996]
data['year']= pd.to_datetime(data.year, format='%Y')

# Enclose the chart into a function for filtering purposes:
def plot_altair(chosencountry):
    data_country_filter = data[data['country'] == chosencountry]
    chart = alt.Chart(data_country_filter).mark_boxplot().encode(
    x='suicides/100k pop',  
    y= 'generation',
    fill = 'generation'
    ).interactive()
    return chart.to_html()

    



app = dash.Dash(__name__)


app.layout = html.Div(children=[html.H1(children='Suicide Rates DataFrame'),
    dcc.Graph(id='world',figure=fig_map),
    html.Div([html.P(),
        html.H5('Choose the country'),
        dcc.Dropdown(id= "country_dropdown",
        value= 'Canada',
        options= [
            {'label':i, 'value':i} for i in list_countries
        ],
        style={'height': '30px', 'width': '300px'})
        #dcc.Textarea(id='chosen_country')
    ]),
    html.Div([
        html.Iframe(
            id= 'boxplot',
            #srcDoc=plot_altair(chosencountry),
        style={'border-width': '0', 'width': '200%', 'height': '400px'})
    ])
    
])

@app.callback(
    #Output('chosen_country','value'),
    Output('boxplot','srcDoc'),
    Input('country_dropdown','value')
)
def update_output(chosencountry):
    return plot_altair(chosencountry)

if __name__ == '__main__':
    app.run_server(debug= True, use_reloader=False)




