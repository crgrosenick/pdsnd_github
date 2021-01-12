import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Global month and day name lists to reference
month_names = {'january':1,'february':2,'march':3,'april':4,'may':5,'june':6}

day_names = {'monday':0,'tuesday':1,'wednesday':2,'thursday':3,'friday':4,\
             'saturday':5,'sunday':6}

def get_filters():
    """
    Asks user to specify specific cities, months, and days to analyze.
    If the user types in an invalid city, month, or day, it will loop until
    a valid input is received.

    Returns:
        (list of str) city - names of the city to analyze
        (list of str) month - names of the month to filter by, or "all" to apply no month filter
        (list of str) day - names of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hey there! Let\'s explore some US bikeshare data! We have data for Chicago,')
    print('Washington, and New York City between January and June.')
    print()

    ##### CITY #####
    # TO DO: get user input for city (chicago, new york city, washington).
    #HINT: Use a while loop to handle invalid inputs
    print('First, let\'s pick cities to look at. We have data for '\
          'Chicago, Washington, and New York')

    cities = input('City. Separate your choices with a comma, or write \'All\' to '\
             'view data for all cities: ').lower().replace(', ',',').strip().split(',')

    #nested loop to make sure someone enters an appropriate city
    if 'all' in cities:
        cities = ['chicago','washington','new york city']
    else:
        for city in cities:
            new_city = city
            while new_city not in CITY_DATA:
                new_city = input('Sorry, it doesn\'t look like we have data for \'{}\'.'\
                           ' Please choose either Chicago, Washington, or New York '\
                           'City: '.format(city.title())).lower()
            cities[cities.index(city)] = new_city.strip()

    ##### MONTH ######
    # TO DO: get user input for month (all, january, february, ... , june)
    print()
    print('If you are interested in analyzing specific months (between January'\
         ' and June), please write them here.')
    months = input('Separate your choices with a comma, or write \'All\' to view'\
                  ' data for all months: ').lower().replace(', ',',').split(',')

    #and another prompt if they don't enter a valid month or 'no'
    if 'all' in months:
        months = list(month_names.values())
    else:
        for month in months:
            new_month = month
            while new_month not in month_names:
                new_month = input('Sorry, it doesn\'t look like we have data for \'{}\'.'\
                                   ' Please choose another month: '\
                              .format(month.title())).lower()
            months[months.index(month)] = month_names[new_month]

    ##### DAY #####
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    print()
    print('If you are interested in analyzing specific days of the week, please write them here.')
    days = input('Separate your choices with a comma, or write \'All\' to view'\
                  ' data for all days of the week: ').lower().replace(', ',',').split(',')

    #and another prompt if they don't enter a valid month or 'no'
    if 'all' in days:
        days = list(day_names.values())
    else:
        for day in days:
            new_day = day
            while new_day not in day_names:
                new_day = input('{} isn\'t a day. Please enter a valid day: '\
                              .format(day.title())).lower()
            days[days.index(day)] = day_names[new_day]

    # dedupe
    cities = list(set(cities))
    months = list(set(months))
    days = list(set(days))

    print()
    print('='*40)
    return cities, months, days


def load_data(cities, months, days):
    """
    Loads data for the specified cities and filters by month and day if applicable.

    Args:
        (list of str) city - names of the city to analyze
        (list of str) month - names of the month to filter by, or "all" to apply no month filter
        (list of str) day - names of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Initialize dataframe to append each file as its called
    df = pd.DataFrame()
    # Loop through selected cities, read file, and append to dataframe
    for city in cities:
        temp_data = pd.DataFrame(pd.read_csv(CITY_DATA[city]))
        temp_data['City'] = city.title()
        df = df.append(temp_data)

    # convert start and end date to datetime (just to knock 2 birds w/ 1 stone)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # create columns for month name and day name for each entry
    df['Month'] = df['Start Time'].dt.month
    df['Week Day'] = df['Start Time'].dt.weekday

    # filter data that is only in the months list
    if len(months)!=12:
        df = df[df['Month'].isin(months)]

    #filter data that is only in the days list
    if len(days)!=7:
        df = df[df['Week Day'].isin(days)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print()
    common_month = [key for key, value in month_names.items() if value == df['Month'].mode()[0]]
    print('Riders most commonly rode in: {}'\
          .format(common_month[0].title()))

    # TO DO: display the most common day of week
    common_day = [key for key, value in day_names.items() if value == df['Week Day'].mode()[0]]
    print('Riders most commonly rode on: {}'\
          .format(common_day[0].title()))

    # TO DO: display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    common_hour = df['Hour'].mode()[0]

    # Adding an A.M./P.M. to aid in understandability
    if common_hour >= 12:
        if common_hour > 13:
            common_hour -= 12
        suffix = 'P.M.'
    else:
        suffix = 'A.M.'

    print('Riders most commonly started at: {} {}'.format(common_hour,suffix))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print()
    print('='*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print()
    print('Riders most often started at: {}'.format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print('Riders most often ended at: {}'.format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    df['Trip Stations'] = df['Start Station'] + ' --> ' + df['End Station']
    print('Riders most common trip was: {}'.format(df['Trip Stations'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print()
    print('='*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['Trip Mins'] = df['Trip Duration']/60
    df['Trip Hours'] = df['Trip Duration']/3600

    # TO DO: display total travel time
    print('Riders travelled for a total of: {} hours'\
          .format(round(df['Trip Hours'].sum(),1)))

    # TO DO: display mean travel time
    print('Riders travelled for an average of: {} minutes'\
          .format(round(df['Trip Mins'].mean(),1)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print()
    print('='*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('We\'re now going to take a look at few other statistics. We\'ll look ')
    print('at the count of User Type, Gender, and Basic Age Demographics.')

    # TO DO: Display counts of user types
    try:
        print()
        print('User Type:')
        print('-'*10)
        print(df['User Type'].value_counts())
    except:
        print('Sorry, no User Type data available.')

    # TO DO: Display counts of gender
    try:
        print()
        print('Gender:')
        print('-'*10)
        print(df['Gender'].value_counts())
    except:
        print('Sorry, no Gender data available.')

    # TO DO: Display earliest, most recent, and most common year of birth
    ## NOTE: I'm going to change this to age, since that's easier to understand
    print()
    print('Age Demographics:')
    print('-'*20)
    try:
        df['Age'] = dt.datetime.now().year - df['Birth Year']

        print('Oldest Rider: {}'.format(round(df['Age'].max()),0))
        print('Youngest Rider: {}'.format(round(df['Age'].min()),0))
        print('Most Common Age: {}'.format(round(df['Age'].mode()[0]),0))
    except:
        print('Sorry, no Age data available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print()
    print('='*40)

def display_raw_data(df_raw):
    """ Asks the user if they want to see the raw data, and displays raw data
       5 rows at a time until the user decides to stop """

    df_raw = df_raw.drop(['Month','Week Day'],axis = 1)
    df_raw = df_raw.reset_index(drop=True)

    print()
    print('Now that you\'ve seen some statistics, are you interested in viewing some'\
          ' of the raw data? We\'ll display it 5 rows at a time.')
    display = input('Please enter \'Yes\' or \'No\' if you\'d like to see the raw data: ')


    start = 0
    while display.lower() == 'yes' or display.lower() == 'y':
        print(df_raw.loc[start:start+4])
        display = input('Continue? (\'Yes\' or \'No\'): ')
        start += 5



def main():
    while True:
        print()
        cities, months, days = get_filters()
        df = load_data(cities, months, days)
        df_raw = df.copy()

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df_raw)

        restart = input('\nWould you like to keep exploring the data? Enter \'Yes\''\
                        ' or \'No\'.\n')
        if restart.lower() != 'yes':
            break

        print()

if __name__ == "__main__":
	main()
