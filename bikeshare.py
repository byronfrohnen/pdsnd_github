import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities=['chicago','new york city','washington']
months=['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December','All']
days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = str(input("Would you like to see data from Chicago or New York City. \n" )).lower()

        if city not in cities:
            print("Please enter one of the two cities provided.")

        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = str(input("Which month would you like to focus on? If you do not want to filter, type all. \n")).title()

        if month not in months:
            print("Please enter a valid month or type all.")

        else:
            break


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input("What day of the week would you like to evaluate? Type in the day.\n")).title()

        if day not in days:
            print("Please enter a day of the week.")
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

    # convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # create new columns for month and day
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month
    if month != 'All':
        month = months.index(month)
        df = df[df['month'] == month]

    # filter by day
    if day != 'All':
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    mode_month = df['month'].mode()[0]
    print("The most common month is: {}".format(months[mode_month-1]))

    # TO DO: display the most common day of week
    print("The most common day of the week is: {}".format(df['day_of_week'].mode()[0]))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common start hour is: {}".format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most commonly used start station is: {}".format(df['Start Station'].mode()[0]))


    # TO DO: display most commonly used end station
    print("The most commonly used end station is: {}".format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    combination = (df['Start Station'] + ' to ' + df['End Station']).mode()[0]
    print("The most frequent combination of start station and end station trip is: {}".format(combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    m_total, s_total = divmod(df['Trip Duration'].sum(), 60)
    h_total, m_total = divmod(m_total, 60)
    print ("The total travel time is: ", h_total,' hours, ', m_total,' minutes, and ', s_total,' seconds.')

    # TO DO: display mean travel time
    m_mean, s_mean = divmod(df['Trip Duration'].mean(), 60)
    h_mean, m_mean = divmod(m_mean, 60)
    print ("The mean travel time is: ", h_mean,' hours, ', m_mean,' minutes, and ', s_mean,' seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("The user can be broken down into \n{}".format(df['User Type'].value_counts()))

    # TO DO: Display counts of gender
    if('Gender' not in df):
        print("Unfortunately, gender data is not available for Washington")
    else:
        print("The genders are \n{}".format(df['Gender'].value_counts()))

    # TO DO: Display earliest, most recent, and most common year of birth
    if ('Birth Year' not in df):
        print("Unfortunately, birth year data is not available for Washington.")
    else:
        print("The earliest birth year is: {}".format(df['Birth Year'].min()))
        print("The most recent birth year is: {}".format(df['Birth Year'].max()))
        print("The most common birth year is: {}".format(df['Birth Year'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        while True:
            start = 0
            view = str(input("\nDo you want to view the data? Enter yes or no.\n"))
            if view != "yes":
                break
            while view == "yes":
                n = int(input("Enter the number of rows to view: \n"))
                n = start + n
                print(df[start:n])
                data = str(input("Do you want to view more rows? Enter yes or no.\n"))
                if data == "yes":
                    print(df[start:n*2]) # doubles the amount of rows shown if user chooses yes
                    break
                elif data != "yes":
                    break
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
