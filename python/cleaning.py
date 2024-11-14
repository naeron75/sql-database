def merge_and_clean():
    """ Takes data from 3 raw csv files. 
    Cleans, merges and outputs dataframe to work with"""

    import pandas as pd
    
    #Import the csv files as dataframes
    medals_df = pd.read_csv('../data/raw/olympic_medals.csv')
    hosts_df = pd.read_csv('../data/raw/olympic_hosts.csv')
    paris_df = pd.read_csv('../data/raw/paris_medallists.csv')

    # Removes duplicated event wins for team events to return one athlete per medal (bronze, silver, gold) per event
    medals_df = clean_medal_duplicates(medals_df)
    paris_df = clean_paris_duplicates(paris_df)

    # Removes unnecessary columns from medals table
    columns_to_drop = ['participant_title', 'participant_type', 'event_gender', 'athlete_url', 'athlete_full_name', 'country_code', 'country_3_letter_code']
    medals_df.drop(columns_to_drop, axis=1, inplace=True)

    # Filters host countries to just include Summer games
    summer_hosts = hosts_df[hosts_df['game_season'] == 'Summer']

    # Gets host country, and year for each game and filters to >1920
    df = medals_df.copy()
    df['host_country'] = medals_df['slug_game'].apply(create_country_column)
    df['game_year'] = medals_df['slug_game'].apply(create_year_column)
    df['game_season'] = medals_df['slug_game'].apply(create_season_column)
    df = df[df['game_season'] == 'Summer']
    df = df[df['game_year'] >= 1920]
    df.reset_index(drop=True, inplace=True)
    df.drop(['slug_game', 'game_season'], axis=1, inplace=True)

    # Removes unnecessary columns from paris dataset
    tiny_paris_df = paris_df.drop(columns=['medal_date', 'medal_code', 'name', 'gender',
       'country_code', 'country_long', 'nationality_code',
       'nationality', 'nationality_long', 'team', 'team_gender', 
       'event_type', 'url_event', 'birth_date', 'code_athlete',
       'code_team', 'is_medallist'])
    
    def standardize_medal_type(medal):
        return medal.lower().strip().replace(' medal', '')
    
    # Tidies and adds Paris games columns
    tiny_paris_df['medal_type'] = tiny_paris_df['medal_type'].apply(standardize_medal_type)
    tiny_paris_df['host_country'] = 'France'
    tiny_paris_df['game_year'] = 2024

    def standardize_string(string):
        return string.lower().strip()

    # Standardizes columns in paris dataframes
    tiny_paris_df['country'] = tiny_paris_df['country'].apply(standardize_string)
    tiny_paris_df['host_country'] = tiny_paris_df['host_country'].apply(standardize_string)
    tiny_paris_df['discipline'] = tiny_paris_df['discipline'].apply(standardize_string)
    tiny_paris_df['event'] = tiny_paris_df['event'].apply(standardize_string)
    tiny_paris_df.rename(columns={'country': 'athlete_country'}, inplace=True)    

    # Standardizes columns in medals dataframes
    df['medal_type'] = df['medal_type'].apply(standardize_string)
    df['host_country'] = df['host_country'].apply(standardize_string)
    df['country_name'] = df['country_name'].apply(standardize_string)
    df['discipline_title'] = df['discipline_title'].apply(standardize_string)
    df['event_title'] = df['event_title'].apply(standardize_string)
    df.rename(columns={'country_name': 'athlete_country'}, inplace=True)
    df.rename(columns={'discipline_title': 'discipline'}, inplace=True)
    df.rename(columns={'event_title': 'event'}, inplace=True)

    # Combines dataframes
    full_df = pd.concat([df, tiny_paris_df], ignore_index=True)

    # Clean country names
    full_df = clean_country_names(full_df)

    # Updates event column to include discipline
    event_df = full_df.copy()
    event_df['event'] = event_df['discipline'] + ' - ' + event_df['event']    

    # Get only specific columns
    event_df = event_df[['host_country', 'game_year', 'event', 'medal_type', 'athlete_country']]

    'event_df.to_csv('../data/clean/clean_summer_df_events.csv')
    
    return(event_df)


def clean_paris_duplicates(paris_df):
    """Returns the first medal winner from each team event in the paris 2024 dataset"""
    condition = paris_df['event_type'].isin(['TEAM', 'HTEAM', 'HCOUP', 'COUP'])
    
    #Gets all team events and drops duplicates
    paris_df_filtered = paris_df[condition].drop_duplicates(
        subset=['medal_date', 'medal_type', 'medal_code', 'country_code', 'country', 
                'country_long', 'nationality_code', 'nationality', 'nationality_long'], 
        keep='first'
    )
    
    # Combines filtered team events with individual events
    paris_df_update = pd.concat([paris_df[~condition], paris_df_filtered])
    return(paris_df_update)

def clean_medal_duplicates(medals_df):
    """Returns the first medal winner from each team event in the 1896-2020 dataset"""
    condition = medals_df['participant_type'].isin(['GameTeam'])
    
    #Gets all team events and drops duplicates
    medals_df_filtered = medals_df[condition].drop_duplicates(
        subset=['discipline_title', 'slug_game', 'event_title', 'event_gender',
       'medal_type'], 
        keep='first'
    )
    
    # Combines filtered team events with individual events
    medals_df_update = pd.concat([medals_df[~condition], medals_df_filtered])
    return(medals_df_update)

def create_country_column(slug):
    for i, host_slug in enumerate(hosts_df['game_slug']):
        if slug == host_slug:
            return hosts_df['game_location'].iloc[i]

def create_year_column(slug):
    for i, host_slug in enumerate(hosts_df['game_slug']):
        if slug == host_slug:
            return hosts_df['game_year'].iloc[i]

def create_season_column(slug):
    for i, host_slug in enumerate(hosts_df['game_slug']):
        if slug == host_slug:
            return hosts_df['game_season'].iloc[i]

def clean_country_names(df):
    """ Takes 'athlete_country' column and replaces countries with consistent names """"
    
    # Dictionary of country names to change
    country_mapping = {
        'ir iran': 'iran',
        'islamic republic of iran': 'iran',
        'korea': 'south korea',
        'republic of korea': 'south korea',
        'united states': 'usa',
        'united states of america': 'usa',
        "democratic people's republic of korea": 'north korea',
        'dpr korea': 'north korea',
        'ain': 'individual neutral athletes',
        "people's republic of china": 'china',
        'czech republic': 'czechia',
        'türkiye': 'turkey',
    }
    
    # Replaces the names in the dataframe
    df['athlete_country'] = df['athlete_country'].replace(country_mapping)

    # Dictionary of country names to change
    host_country_mapping = {
        'republic of korea': 'south korea',
        'united states': 'usa',
        'australia, sweden' : 'australia'
    }

    df['host_country'] = df['host_country'].replace(host_country_mapping)
    
    return df