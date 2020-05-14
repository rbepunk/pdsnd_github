import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input ('Choose a city to analyze:\n Chicago, New York City, Washington\n').lower()
        if city.lower() not in ('chicago','new york city','washington'):
            print('City not available, please choose an available city.')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)

    while True:
        month = input ('Choose a month:\n all, january, february, march, april, may, june \n').lower()
        if month.lower() not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
            print ('Please choose one of the listed options.')
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input ('Choose a day of the week:\n all, sunday, monday, tuesday, wednesday, thursday, friday, saturday \n').lower()
        if day.lower() not in ('all','sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'):
            print ('Please choose one of the listed options.')
            continue
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime (df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].value_counts().keys()[0]
    print(f'common month: {common_month}')

    # display the most common day of week
    common_day = df['day_of_week'].value_counts().keys()[0]
    print(f'common day of week: {common_day}')

    # display the most common start hour
    hour = df['Start Time'].value_counts().keys()[0]
    hour_only = str(hour)[11:13]
    print (f'common hour: {hour_only}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start = df['Start Station'].value_counts().keys()[0]
    counts_start = df['Start Station'].value_counts().tolist()[0]

    print (f'The most popular start station is {pop_start} with a trip total: {counts_start}')
    # display most commonly used end station
    pop_end = df['End Station'].value_counts().keys()[0]
    counts_end = df['End Station'].value_counts().tolist()[0]

    print (f'The most popular end station is {pop_end} with a trip total: {counts_end}')
    # display most frequent combination of start station and end station trip
    df ['Combination Station'] = df ['Start Station'] + '' + df['End Station']
    pop_combination = df['Combination Station'].value_counts().keys()[0]
    counts_combination = df['Combination Station'].value_counts().tolist()[0]

    print (f'The most frequent combination is {pop_combination} with a total: {counts_combination}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    seconds = df['Trip Duration'].sum()
    minutes = seconds / 60
    hours = minutes / 60

    print (f'The total travel time is:\n seconds:{seconds:.0f}, minutes:{minutes:.0f}, hours:{hours:.0f}')
    # display mean travel time
    seconds = df['Trip Duration'].mean()
    minutes = seconds / 60
    hours = minutes / 60

    print (f'The mean travel time is:\n seconds:{seconds:.0f}, minutes:{minutes:.0f}, hours:{hours:.0f}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    users = df['User Type'].value_counts().keys()
    count_users = df['User Type'].value_counts().tolist()
    users_count = dict(zip(users,count_users))
    print(users_count)

    # Display counts of gender
    if 'Gender' in df.columns:

        genders = df['Gender'].value_counts().keys()
        count_genders = df['Gender'].value_counts().tolist()
        genders_count = dict(zip(genders,count_genders))
        print(genders_count)
    else:
        print('\nColumn Gender does not exist in dataset')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earlist,recent,common = df['Birth Year'].min(), df['Birth Year'].max(), df['Birth Year'].value_counts().keys()[0]
        print(f'Earlist: {earlist}, Recent: {recent} and Common: {common}')

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    else:
        print('\nColumn Birth Year does not exist in dataset')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        start_loc = 0
        end_loc = 5

        view_data = input('Would you like to view the data? Yes or no.\n').lower()

        if view_data == 'yes':
            print(df.iloc[0:5])
            start_loc += 0
            end_loc += 5

        elif view_data == 'no':
            break

        view_more = input('Would you like to view more data? Yes or no.').lower()

        if view_more == 'yes':
            print(df.iloc[start_loc:end_loc])
            start_loc += 5

        elif view_more == 'no':
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
