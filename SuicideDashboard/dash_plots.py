import plotly.express as px
import altair as alt


def create_world_plot(data, location, color, hover_name):
    fig_map = px.choropleth(data,
                            locations=location,
                            color=color,
                            hover_name=hover_name,
                            color_continuous_scale=px.colors.sequential.Blues,
                            width=200, height=262)

    fig_map.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        width=700,
        #paper_bgcolor="Black",
        geo=dict(bgcolor='rgba(50,50,50,50)'),
        paper_bgcolor='#282b30'
    )

    return fig_map


def plot_suicide_boxplot(country_dropdown, data):
    data_country_filter = data[data['country'] == country_dropdown]
    chart = alt.Chart(data_country_filter).mark_boxplot().encode(
        alt.X('suicides/100k pop', title='Suicides per 100k'),
        alt.Y('generation', title=''),
        alt.Color('generation', legend=None)
    ).interactive()
    return chart.to_html()

def plot_suicide_gdp(data, sex, year, country, age, generation):
    df = data[data['country'] == country]
    for gender in sex:
        df = df[df['sex'] == gender]
    df = df[df['year'] == year]
    df = df[df['age'] == age]
    df = df[df['generation'] == generation]

    chart = alt.Chart(df).mark_point().encode(
        alt.X('gdp_per_capita ($)', title='GDP per Capita ($)'),
        alt.Y('suicides_no', title='Total Number of Suicides')).interactive()
    return chart.to_html()
