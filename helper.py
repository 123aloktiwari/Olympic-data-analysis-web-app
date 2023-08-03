import numpy as np
import pandas as pd

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


# def medal_tally(df):
#
#     medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
#
#     medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
#                                                                                 ascending=False).reset_index()
#
#     medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
#
#     medal_tally['Gold'] = medal_tally['Gold'].astype('int')
#     medal_tally['Silver'] = medal_tally['Silver'].astype('int')
#     medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
#     medal_tally['total'] = medal_tally['total'].astype('int')
#     return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country

def participating_nations_over_time(df):
    # Group by 'Year' and count unique 'region' values (countries) for each year
    nations_over_time = df.groupby('Year')['region'].nunique().reset_index()

    # Rename the columns
    nations_over_time.rename(columns={'Year': 'Edition', 'region': 'No of Countries'}, inplace=True)

    return nations_over_time

def events_over_time(df):
    # Group by 'Year' and count the number of events for each year
    events_count = df.groupby('Year')['Event'].nunique().reset_index()

    # Rename the columns
    events_count.rename(columns={'Year': 'Edition', 'Event': 'No of Events'}, inplace=True)

    return events_count

def athletes_over_time(df):
    # Group by 'Year' and count the number of unique athletes for each year
    athletes_count = df.groupby('Year')['Name'].nunique().reset_index()

    # Rename the columns
    athletes_count.rename(columns={'Year': 'Edition', 'Athlete Name': 'Name'}, inplace=True)

    return athletes_count

def most_successful(df, selected_sport):
    # Filter the DataFrame based on the selected sport
    temp_df = df[df['Sport'] == selected_sport]

    # Count the number of medals (Medal column contains Gold, Silver, Bronze, or NaN)
    temp_df['Medal Count'] = temp_df['Medal'].apply(lambda x: 1 if x in ['Gold', 'Silver', 'Bronze'] else 0)

    # Group by 'Name' and count the number of medals for each athlete
    athlete_medal_count = temp_df.groupby('Name')['Medal Count'].sum().reset_index()

    # Sort by medal count in descending order and select the top 15 most successful athletes
    top_athletes = athlete_medal_count.sort_values(by='Medal Count', ascending=False).head(15)

    # Merge with the original DataFrame to get additional details about the athletes
    merged_df = top_athletes.merge(df, left_on='Name', right_on='Name', how='left')

    return merged_df

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df, selected_country):
    # Filter the DataFrame based on the selected country
    temp_df = df[df['region'] == selected_country]

    # Count the number of medals (Medal column contains Gold, Silver, Bronze, or NaN)
    temp_df['Medal Count'] = temp_df['Medal'].apply(lambda x: 1 if x in ['Gold', 'Silver', 'Bronze'] else 0)

    # Group by 'Name' and count the number of medals for each athlete
    athlete_medal_count = temp_df.groupby('Name')['Medal Count'].sum().reset_index()

    # Sort by medal count in descending order and select the top 10 most successful athletes
    top_athletes = athlete_medal_count.sort_values(by='Medal Count', ascending=False).head(10)

    # Merge with the original DataFrame to get additional details about the athletes
    merged_df = top_athletes.merge(df, left_on='Name', right_on='Name', how='left')

    return merged_df

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final