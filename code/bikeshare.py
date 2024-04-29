import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = {'chicago': 'chicago.csv','new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

DAY_DATA = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    
    """
    Asks user to specify a city, month, and day of week to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city.
    name_of_city = ''
    while name_of_city not in CITY_DATA:
        name_of_city = input('Please choose a city you want to analyze bikeshare data from (Chicago, New York City or Washington): ').lower()
        print('You chose {}'.format(name_of_city))
        if name_of_city in CITY_DATA:
            city = CITY_DATA[name_of_city]
        else:
            print('Hmm... I couldn\'t find the city. Please choose between Chicago, New York City or Washington and check your spelling.')
    
    # Get user input for month.
    name_of_month = ''
    while name_of_month not in MONTH_DATA:
        name_of_month = input('Please choose month to analyze bikeshare data from (january, february, march, april, may, june or all): ').lower()
        print('You chose {}'.format(name_of_month))
        if name_of_month in MONTH_DATA:
            month = name_of_month
        else:
            print('Hmm... I couldn\'t find the month. Please choose between january, february, march, april, may, june or all.')
    
    # Get user input for day of week.
    name_of_day = ''
    while name_of_day not in DAY_DATA:
        name_of_day = input('Please choose what day of week to analyze (monday, tuesday, etc., - or just enter "all": ').lower()
        print('You chose {}'.format(name_of_day))
        if name_of_day in DAY_DATA:
            day = name_of_day
        else:
            print('Hmm... I couldn\'t find the day of week you chose. Please try again (monday, tuesday, etc., - or "all": ')
    
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
    # Loading data file into a DataFrame.
    df = pd.read_csv(city)
    
    # Converting the column 'Start Time' to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extracting month and day of week from 'Start Time' to create new columns.
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    
    # Filter by month if applicable.
    if month != 'all':
        # Using the index of the months list to get the corresponding month.
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # Filter by month to create the new column.
        df = df[df['month'] == month]

    # Filtering by day of week if applicable.
    if day != 'all':
        # Filter by day of week to create the new DataFrame.
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Displaying the most common month.
    common_month = df['month'].mode()[0]
    name_of_month = calendar.month_name[common_month]
    print('The most common month is {}'.format(name_of_month))

    # Displaying the most common day of week.
    common_day_of_week = df['day_of_week'].mode()[0]
    print('The most common day of week is {}'.format(common_day_of_week))
    
    # Displaying the most common start hour.
    common_hour = df['hour'].mode()[0]
    print('The most common start hour is the {}th hour'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displaying most commonly used start station.
    start_station = df['Start Station'].mode()[0]
    common_start_station = df['Start Station'].value_counts()[0]
    print('The most commonly used start station is {}, \n with count:{}'.format(start_station, common_start_station))

    # Displaying most commonly used end station.
    end_station = df['End Station'].mode()[0]
    common_end_station = df['End Station'].value_counts()[0]
    print('The most commonly used end station is {}, \n with count:{}'.format(end_station, common_end_station))

    # Displaying most frequent combination of start- and end station trip.
    df['muses'] = (df['Start Station'] + "||" + df['End Station']).value_counts().idxmax()
    pop_station = df['muses'].mode()[0]
    freqtrips = (df['Start Station'] + "||" + df['End Station']).value_counts()[0]
    print('The most frequent combination of start station and end station trip is {}, \n with count:{}'.format(pop_station, freqtrips))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Displaying total travel time.
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time is {}'.format(total_travel_time))

    # Displaying mean travel time.
    avg_travel_time = df['Trip Duration'].mean()
    print('The Average total travel time is {}'.format(avg_travel_time))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displaying counts of user types.
    user_types_count = df['User Type'].value_counts()
    print('Counts of User Types are:\n{}'.format(user_types_count))
    
    # Displaying counts of gender.
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('Counts of Gender are:\n{}'.format(gender_count))

    # Displaying earliest, most recent, and most common year of birth.
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common_birthyear = int(df['Birth Year'].mode()[0])
        print('The earliest year of birth is: {}'.format(earliest))
        print('The most recent year of birth is: {}'.format(most_recent))
        print('The most common year of birth is: {}'.format(most_common_birthyear))
    if 'Birth Year' not in df.columns and 'Gender' not in df.columns:
        print('\n\nNo gender or birth year data found')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(city):
    """Shows raw data when user requests it."""
    print('\nRaw data is available for viewing.\n')
    showing_raw_data = input('Would you like to see the next 5 rows of raw data? Please enter yes or no. \n').lower()
    while showing_raw_data != 'yes'and showing_raw_data != 'no':
        showing_raw_data =input('Invalid Input!, Do you want to see the raw data? Type yes or no\n').lower()
    while showing_raw_data == 'yes':
        try:
            chunksize=5
            for row in pd.read_csv(city, chunksize = chunksize):
                pd.set_option('display.max_columns',200)
                print(row) 
                # Repeating prompt.
                showing_raw_data = input('Would you like to see the next 5 rows of raw data? Please enter yes or no. \n').lower()
                if showing_raw_data != 'yes':
                     print('Thank you')
                     break

            break
        except KeyboardInterrupt:
            print('Thank you.')
            break
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()