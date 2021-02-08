import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) time_filter - filter by month, day, both, or 'none" to appy no time filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=input("Would you like to see data for Chicago, New York City, or Washington?").title()

    # time filter types
    time_filter=input("Would you like to filter the data by month, day, both, or not at all? Type \"none\" for no time filter.").lower()

    if time_filter == "month":
        # get user input for month (all, january, february, ... , june)
        month=input("Which month? January, February, March, April, May, June?").lower()
        day="all"
    if time_filter == "day":
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day=input("Which day? (e.g., Sunday)").lower()
        month="all"
    if time_filter=="both":
        month=input("Which month? January, February, March, April, May, or June?").lower()
        day=input("Which day? (e.g., Sunday)").lower()
    if time_filter=="none":
        month="all"
        day="all"

    print('-'*40)
    return city, month, day, time_filter


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['mon'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != "all":
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['mon'] == month]

    # filter by day of week if applicable
    if day != "all":
        days = ['sunday','monday','tuesday','webdnesday','thursday','friday','saturday']
        day = days.index(day)+1
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == int(day)]


    return df



def time_stats(df,time_filter):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if time_filter == "day" or time_filter == "none":
        df['mon']=df['Start Time'].dt.month
        popular_month=df['mon'].mode()[0]
        print('Most common month: ',popular_month)

    # display the most common day of week
    if time_filter == "month" or time_filter == "none":
        df['day_of_week']=df['Start Time'].dt.dayofweek
        popular_day_of_week=df['day_of_week'].mode()[0]
        print('Most common day of week: ',popular_day_of_week)

    # display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    popular_hour=df['hour'].mode()[0]
    print('Most common start hour: ',popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start=df['Start Station'].mode()[0]
    print('Most common start station: ',popular_start)

    # display most commonly used end station
    popular_end=df['End Station'].mode()[0]
    print('Most common end station: ',popular_end)

    # display most frequent combination of start station and end station trip
    df['Trip']=df['Start Station']+" to "+df['End Station']
    popular_trip=df['Trip'].mode()[0]
    print('Most frequent combination of start station and end station trip: ',popular_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()


    # display total travel time
    sum_duration=df['Trip Duration'].sum()
    print('Total travel time: ',sum_duration)

    # display mean travel time
    mean_duration=df['Trip Duration'].mean()
    print('Average travel time: ',mean_duration)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User types:\n',user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('Counts of gender:\n', gender_counts)
    else:
        print('Gender information: Not available for the selected city.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode())
        print('Year of birth: \nEarliest year of birth: ',earliest_year,
              '\nMost recent year of birth: ',recent_year,
              '\nMost common year of birth: ',common_year)
    else:
        print('Year of birth: Not available for the selected city.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Asks if the user would like to see indivitual trip data.
    Returns:
        Displays 5 raws of data each time the user types "yes" until there is no more data."""

    #Display the first 5 rows of data if requested
    r_stop=0
    individual_trip="yes"

    while individual_trip=="yes":

        #Get user input for individual trip data
        individual_trip=input("Would you like to view individual trip data? Type \"yes\" or \"no\".").lower()

        # 5 rows each time requested
        r_start=r_stop
        r_stop+=5

        print(df.shape)

        if r_stop < df.shape[0]:
            trip_data=df.iloc[r_start:r_stop]
            print("Displying row {} to row {}.".format(r_start,r_stop))
            print(trip_data)
            print("Rows left: ",df.shape[0]-r_stop)

        if r_stop >= df.shape[0]:
            trip_data=df.iloc[r_start:]
            print("Displaying row{} to row {}.".format(r_start,df.shape[0]))
            print(trip_data)
            print("You've seen all {} available data.".format(df.shape[0]))
            break


    print('-'*40)


def main():
    while True:
        city, month, day, time_filter = get_filters()
        df = load_data(city, month, day)

        time_stats(df,time_filter)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter "yes" or "no".\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
