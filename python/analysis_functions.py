import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns

clean_df = pd.read_csv("../data/clean/clean_summer_df_events.csv")
country_df = pd.read_csv("../data/raw/country_table.csv") 
event_df = pd.read_csv("../data/raw/event_table.csv")

def merge_dataframes(clean_df, country_df, event_df)
    merged_df = clean_df.merge(country_df, left_on="athlete_country", right_on="country_name", how = 'left').reset_index(drop=True)
    merged_df = merged_df.merge(event_df, left_on="event", right_on="event", how = 'left').reset_index(drop=True)
    
    merged_df = merged_df[['host_country', 'game_year', 'event', 'medal_type',
       'athlete_country', 'continent', 'hemisphere',
       'discipline', 'sub-discipline']]
    
    merged_df = merged_df.rename(columns={'continent': 'athlete_continent', 'hemisphere': 'athlete_hemisphere'})
    merged_df = merged_df.merge(country_df, left_on="host_country", right_on="country_name", how = 'left').reset_index(drop=True)

    merged_df = merged_df.rename(columns={'continent': 'host_continent', 'hemisphere': 'host_hemisphere'})
    merged_df.drop(columns="country_name", inplace=True)

    merged_df['is_host_country'] = merged_df['host_country'] == merged_df['athlete_country']
    merged_df['is_host_continent'] = merged_df['host_continent'] == merged_df['athlete_continent']

    filt_df = merged_df[['game_year', 'event', 'medal_type', 'athlete_country',
       'athlete_continent', 'discipline',
       'sub-discipline', 'host_country', 'host_continent',
       'is_host_country', 'is_host_continent']]
    
    country_medals = filt_df.groupby(['athlete_country', 'game_year', 'medal_type', 'discipline',
                                  'is_host_country', 'is_host_continent']).size().reset_index(name='medal_count')

    return country_medals

def get_ratio_data(df=country_medals, year_from=1960):
    '''Loops through host countries in a dataframe and returns their medal win% from specified start year (or 1960 as default)

    Prints the relative increase in medals won for hosting vs non-hosting years and being in host continent vs not
    Returns a dataframe summarising those values
    
    dateframe must have these columns:
    ['athlete_country', 'game_year', 'is_host_country', 'is_host_continent']
    '''   
    #year filter
    df = df[df['game_year'] >= year_from]
    
    df = df.groupby(['athlete_country', 'game_year', 'is_host_country', 'is_host_continent'], as_index=False)['medal_count'].sum()
    
    # total medals for each year
    df['year_total_medals'] = df.groupby('game_year')['medal_count'].transform('sum')
    
    # percentage of medals each country won per year
    df['medal_pct'] = (df['medal_count'] / df['year_total_medals']) * 100
    
    # `avg_win%` for each country across all years
    avg_win = (
        df.groupby('athlete_country', as_index=False)['medal_pct']
        .mean().round(2)
        .rename(columns={'medal_pct': 'avg_win%'})
    )
    
    # Calculate `avg_hosting_win%` - average win percentage when the country is hosting
    avg_hosting_win = (
        df[df['is_host_country']]
        .groupby('athlete_country', as_index=False)['medal_pct']
        .mean().round(2)
        .rename(columns={'medal_pct': 'avg_hosting_win%'})
    )
    
    # Calculate `avg_not_hosting_win%` - average win percentage when the country is not hosting
    avg_not_hosting_win = (
        df[~df['is_host_country']]
        .groupby('athlete_country', as_index=False)['medal_pct']
        .mean().round(2)
        .rename(columns={'medal_pct': 'avg_not_hosting_win%'})
    )
    
    # Calculate `avg_continent_win%` - average win percentage when a country on the same continent is hosting
    avg_continent_win = (
        df[df['is_host_continent']]
        .groupby('athlete_country', as_index=False)['medal_pct']
        .mean().round(2)
        .rename(columns={'medal_pct': 'avg_continent_win%'})
    )
    
    avg_not_continent_win = (
        df[~df['is_host_continent']]
        .groupby('athlete_country', as_index=False)['medal_pct']
        .mean().round(2)
        .rename(columns={'medal_pct': 'avg_not_continent_win%'})
    )
    

    result = avg_win.merge(avg_hosting_win, on='athlete_country', how='left') \
                    .merge(avg_not_hosting_win, on='athlete_country', how='left') \
                    .merge(avg_continent_win, on='athlete_country', how='left') \
                    .merge(avg_not_continent_win, on='athlete_country', how='left')
    
    result = result.rename(columns={'athlete_country':'country'})
    
    
    host_countries = list(df[df['is_host_country'] == True]['athlete_country'].unique())
    
    host_result = result[result['country'].isin(host_countries)]
    
    host_result['host/not_ratio'] = (host_result['avg_hosting_win%'] / host_result['avg_not_hosting_win%']).round(2)
    host_result['continent/not_ratio'] = (host_result['avg_continent_win%'] / host_result['avg_not_continent_win%']).round(2)
    
    print(f"Since {year_from} hosting delivers an average of { (100*(host_result['host/not_ratio'].mean()-1)).round(2)}% more medals")
    print(f"Since {year_from} being in the host continent wins you { (100*(host_result['continent/not_ratio'].mean()-1)).round(2)}% more medals")
    print()
    return(host_result)

def chart_ratio(df, year_from=1960):
    """ Charts each host country from start year onwards their win% by year, highlighting when hosting"""
    import matplotlib.pyplot as plt
    import seaborn as sns
       
    df_melted = df.melt(id_vars='country', value_vars=['avg_not_hosting_win%', 'avg_win%', 'avg_continent_win%', 'avg_hosting_win%'],
                        var_name='metric', value_name='value')
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x='country', y='value', hue='metric', data=df_melted)
    
    # Customize the plot
    plt.title(f"Impact of Hosting on Share of Medals Won Since {year_from}")
    plt.xlabel('Country')
    plt.ylabel('Percentage of medals won (%)')
    plt.xticks(rotation=45, ha='right')  # Rotate country labels for better readability
    plt.tight_layout()
    
    # Show the plot
    plt.show()

def continent_ratio(df):
    """returns for each continent how being the host continent benefits their countries on average """
    cont_result = df.merge(country_df, left_on="country", right_on="country_name", how = 'left').reset_index(drop=True)
    
    # Group by 'continent' and calculate the mean of 'continent/not_ratio'
    mean_continent_not_ratio = cont_result.groupby('continent')['continent/not_ratio'].mean().round(2).reset_index()
    
    # Display the result
    print(mean_continent_not_ratio)