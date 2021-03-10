import plotly.express as px
import altair as alt
from altair import datum
from vega_datasets import data
import pylab as plt
import pandas as pd

# The required world map code:
def create_world_plot(data, location, color, hover_name):
    fig_map = px.choropleth(data,
                            locations=location,
                            color=color,
                            hover_name=hover_name,
                            color_continuous_scale=px.colors.sequential.Viridis,
                            width=200, height=262)

    fig_map.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        width=700,
        #paper_bgcolor="Black",
        geo=dict(bgcolor='rgba(50,50,50,50)'),
        paper_bgcolor='White',
        legend = dict( font = dict(size =12, color = 'black'))
    )

    legend = plt.legend()
    plt.setp(legend.get_texts(), color = 'w')

    return fig_map

# The box plot that shows the variations across generations:
def plot_suicide_boxplot(country_dropdown, data):
        data_country_filter = data[data['country'] == country_dropdown]
        alt.themes.enable('dark')
        chart = alt.Chart(data_country_filter).mark_boxplot().encode(
            alt.X('suicides/100k pop', title='Suicides per 100k'),
            alt.Y('generation', title = None),
            fill = alt.Color('generation', legend=None, scale= alt.Scale(scheme= 'viridis'))
            ).facet('sex').properties(columns=1).interactive().configure_axis(labelFontSize=10)
        return chart.to_html()

# Aditya's plot:
def plot_suicide_gdp(data, sex, country, age, generation):
    data = data[data['country'] == country]
    #for gender in sex:
    #    df = df[df['sex'] == gender]
    #df = df[df['year'] == year]
    data = data[data['age'] == age]
    data = data[data['generation'] == generation]
    data['year'] = pd.to_datetime(data['year'], format='%Y')

    chart = alt.Chart(data).mark_point().encode(
        alt.X('year', title='Year'),
        alt.Y('suicides_no', title='Total Number of Suicides')).interactive()
    return chart.to_html()

# Poojitha's plot:
# Suicide per capita data plot:
def age_plot(country_dropdown,source):
    data = source
    data_country_filter = data[data['country'] == country_dropdown]
    point = alt.Chart(data_country_filter).mark_point(filled = True).encode(
    x = 'year',
    y = 'Average_suicides_per_capita',
    color = alt.Color('age', scale= alt.Scale(scheme= 'viridis'))).interactive().configure(background = '#282b30')

    return point.to_html()

# Suicide variations for the gender:
def suicdes_gender(source):
    group1 = source
    click = alt.selection_multi()
    alt.data_transformers.disable_max_rows()
    color_scale = alt.Scale(domain=['male', 'female'],
                            range=['#1f77b4', '#e377c2'])
    left = (alt.Chart(group1).transform_filter(
        (datum.sex == 'female')
    ).encode(
        y=alt.Y('country', axis=None),
        x=alt.X('Average_suicides_per_capita',
                title='Average_suicides_per_capita',
               sort = alt.SortOrder('descending'),
               axis = alt.Axis(orient = 'top')),
        color=alt.Color('sex:N', scale=color_scale, legend=None),
        opacity=alt.condition(click, alt.value(0.8), alt.value(0.4))
    ).mark_bar().properties(title='Female').add_selection(click))
    middle = alt.Chart(group1).encode(
        y=alt.Y('country', axis=None),
        text=alt.Text('country'),
    ).mark_text().properties(width=120)
    right = (alt.Chart(group1).transform_filter(
        (datum.sex == 'male')
    ).encode(
        y=alt.Y('country', axis=None),
        x=alt.X('Average_suicides_per_capita', title='Average_suicides_per_capita',axis = alt.Axis(orient = 'top')),
        color=alt.Color('sex:N', scale=color_scale, legend=None),
        opacity=alt.condition(click, alt.value(0.8), alt.value(0.4))
    ).mark_bar().properties(title='Male').add_selection(click))
    chartf = alt.concat(left, middle, right, spacing=4)
    return chartf.to_html()