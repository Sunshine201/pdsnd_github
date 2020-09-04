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
    # Getting user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please put in the desired city for evaluation - 'Chicago', 'New York City' or 'Washington':\n")
        if city.lower() not in CITY_DATA:
            print("The city '{}' you selected is not available.".format(city.title()))
        else:
            print("You selected:", city)
            city = city.lower()
            break

    # Getting user input for month (all, january, february, ... , june)
    monthlist = ['january','february','march','april','may','june','all']
    while True:
        month = input("Please select your desired month from the list (January, February, March, April, May, June) or 'all' for all months.\n")
        if month.lower() in monthlist:
            print("Here we go! You selected: ", month.title())
            month = month.lower()
            break
        else:
            print("Incorrect data input, please try again!")

    # Getting user input for day of week (all, monday, tuesday, ... sunday)
    daylist = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

    while True:
        day = input("Please provide the day of the week you would like to have more information on (Monday - Sunday), or type 'all':\n")
        if day.lower() in daylist:
            print("Here we go! You selected: ", day.title())
            day = day.lower()
            break
        else:
            print("Incorrect data input, please try again!")

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
    #create DataFrame according to the city input
    df = pd.read_csv(CITY_DATA[city])

    #converting the data format for 'Start Time' to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #adding columns for 'month' and 'day' to DataFrame for further processing
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name

    #filter by month
    if month!='all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        #filter by month
        df = df[df['month'] == month]

     #filter by weekday
    if day!='all':
        #day.title() used to adjust format of day
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""


    # For converting results to Month Name and Day Name
    monthlist = ['January','February','March','April','May','June']
    daylist = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    popular_month = df['Start Time'].dt.month.mode()[0]
    #Conversion to Month Name:
    popular_month_name = monthlist[popular_month-1]
    print('Most Popular month:', popular_month_name)

    # Display the most common day of week
    popular_day = df['Start Time'].dt.weekday.mode()[0]
    #Conversion to Day Name:
    popular_day_name = daylist[popular_day-1]
    print('Most Popular day:', popular_day_name)

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print("Most common Start Station is: ",start_station)

    # Display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print("Most common End Station is: ",end_station)

    # Display most frequent combination of start station and end station trip
    start_end_combination = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    #.to_string to not display dtype.
    print("\nThe most common trip combination of Start and End Station is:\n", start_end_combination.to_string())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time is: {} seconds".format(total_travel_time))

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time is: {} seconds".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    #to_frame() to not display the information name and dtype
    print("User Types: \n", user_types.to_frame())

    # Washington.csv does not contain 'gender' or 'birth year' information; additional if clause to avoid running into KeyErrors
    # Display counts of gender
    if 'Gender' in df.columns:
        gender_types = df['Gender'].value_counts()
        #to_frame() to not display the information name and dtype
        print("\nGender Types:\n", gender_types.to_frame())
    else:
        print("\nThere are no Gender Types to display.\n")


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        yob_earliest = df['Birth Year'].min()
        yob_recent = df['Birth Year'].max()
        yob_common = df['Birth Year'].mode()[0]
        #convert to int for better reading in print out
        print("\nEarliest year of birth:", int(yob_earliest))
        print("Most recent year of birth:", int(yob_recent))
        print("Most common year of birth:", int(yob_common))
    else:
        print("\nThere is no Birth Year information to display.\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    #user input for raw data display of 5 additional lines
        i = 0
        while True:
            display_rawdata = input("\nWould you like to display 5 more lines of raw data? Enter yes or no.\n").lower()

            if display_rawdata == 'yes':
                five_rows = df.iloc[:i+5]
                print(five_rows)
                i+=5
            #for any user input besides 'yes' or 'no':
            elif display_rawdata != 'no':
                print("Non valid input, please try again!")
            else:
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)


        restart = input("\nWould you like to restart? Enter 'yes' to restart or any other input to terminate.\n")
        if restart.lower() != 'yes':
            print("You are leaving the program. Goodbye.\n")
            break



if __name__ == "__main__":
	main()
