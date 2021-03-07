import pandas as pd
import pycountry


def clean_data(file_path):
    data = pd.read_csv(file_path)
    filtered_data = data[['country', 'suicides_no']]
    filtered_data = filtered_data.groupby(['country']).sum().sort_values(by=['suicides_no'],
                                                                         ascending=False)
    filtered_data = filtered_data.reset_index()

    list_countries = filtered_data['country'].unique().tolist()
    country_code_dict = {}

    for country in list_countries:
        try:
            country_data = pycountry.countries.search_fuzzy(country)
            country_code = country_data[0].alpha_3
            country_code_dict.update({country: country_code})
        except:
            country_code_dict.update({country: country_code})

    country_df = pd.DataFrame.from_dict(country_code_dict, orient='index')
    country_df = country_df.reset_index()
    country_df.columns = ['country', 'code']

    filtered_data['code'] = country_df['code']

    return filtered_data
