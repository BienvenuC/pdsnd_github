import time, datetime
import pandas as pd


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
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    #city_list the city_list
    valid_input_city = ['chicago', 'new york city', 'washington','1','2','3']
    response1 = ""
    while response1 not in valid_input_city :
        response1 = str(input("What city would you like to get data from?\n1: Chicago\n2: New york City \n3: Washington \n")).lower()
            
        if response1 not in valid_input_city :
            print('Invalid city\n')
        elif response1 in ['1','2','3']:
            city = valid_input_city[int(response1)-1]
        else:
            city = response1
    # get user input for month (all, january, february, ... , june)
    valid_input_month = ['january', 'february', 'march','april', 'may', 'june','july',\
              'august','september','october','november','december','all',\
                  '1','2','3','4','5','6','7','8','9','10','11','12']
    response2 = ""
    month = ""
    while response2 not in valid_input_month :
        response2 = str(input("What month would you like to get data from?\n1: january\n2: february\n...\nall: all months\n")).lower()
        if response2 not in valid_input_month :
            print('Invalid month\n')
        elif response2 in ['1','2','3','4','5','6','7','8','9','10','11','12']:
            month = valid_input_month[int(response2)-1]
        else:
            month = response2
    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_input_day = ['monday', 'tuesday', 'wednesday','thursday', 'friday', 'saturday','sunday','all',\
                       '1','2','3','4','5','6','7']
    response3 = ""
    day = ""
    while response3 not in valid_input_day :
        response3 = str(input("What day would you like to get data from?\n1: monday\n2: tuesday\n...\nall: all days\n")).lower()
        if response3 not in valid_input_day :
            print('Invalid day\n')
        elif response3 in ['1','2','3','4','5','6','7']:
            day = valid_input_day[int(response3)-1]
        else:
            day = response3

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    pop_month = df['month'].mode()[0]
    count_pop_month = df['month'].value_counts().max()
    print('    Most Frequent month:', pop_month,'  Count: ',count_pop_month)

    # display the most common day of week
    pop_day = df['day_of_week'].mode()[0]
    count_pop_day = df['day_of_week'].value_counts().max()
    print('    Most Frequent day:', pop_day,'  Count: ',count_pop_day)

    # display the most common start hour
    pop_hour = df['hour'].mode()[0]
    count_pop_hour = df['hour'].value_counts().max()
    print('    Most Frequent Start Hour:', pop_hour,'  Count: ',count_pop_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display Number of unique stations
    unique_start_st = df['Start Station'].nunique()
    unique_end_st = df['End Station'].nunique()
    print("    There are {} unique start stations and {} unique end stations".format(unique_start_st, unique_end_st))

    # display most commonly used start station
    pop_start_station = df['Start Station'].mode()[0]
    count_start_st = df['Start Station'].value_counts()[0]
    print('    Most commonly used start station:', pop_start_station, '  Count: ',count_start_st)

    # display most commonly used end station
    pop_end_station = df['End Station'].mode()[0]
    count_end_st = df['End Station'].value_counts()[0]
    print('    Most commonly used end station:', pop_end_station, '  Count: ',count_end_st)

    #most frequent combination of start station and end station trip
    # df1 is the dataframe grouped by Start and End station
    df1= df.groupby(by=['Start Station','End Station']).size().reset_index(name="Count_st_end")
    df1[df1["Count_st_end"] == max(df1["Count_st_end"])]
    pop_start_end_station = (df1[df1["Count_st_end"] == max(df1["Count_st_end"])].reset_index().loc[:,'Start Station'][0],\
                                 df1[df1["Count_st_end"] == max(df1["Count_st_end"])].reset_index().loc[:,'End Station'][0],\
                                 df1[df1["Count_st_end"] == max(df1["Count_st_end"])].reset_index().loc[:,'Count_st_end'][0])
    # display most frequent combination of start station and end station trip
    print("    Most frequent combination of start station and end station trip: \n     \
    {} - {}. Count: {}".format(pop_start_end_station[0],pop_start_end_station[1],pop_start_end_station[2]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    # Convert total_travel_time to days, hours, minutes and seconds.
    print('    Total travel time: ',str(datetime.timedelta(seconds = int(total_travel_time))))

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    # Convert mean_travel_time to days, hours, minutes and seconds.
    print('    Mean travel time: ',str(datetime.timedelta(seconds = int(mean_travel_time))))
    
    # display max travel time and related info 
    max_travel_time = df["Trip Duration"].max()
    df_max_travel_time = df[df["Trip Duration"] == max_travel_time]
    print('    Maximum travel time: ',str(datetime.timedelta(seconds = int(max_travel_time))))
    print("         Start Station: ", df_max_travel_time.reset_index().loc[:,'Start Station'][0])
    print("         End Station: ", df_max_travel_time.reset_index().loc[:,'End Station'][0])
    print("         Month: ", df_max_travel_time.reset_index().loc[:,'month'][0])
    print("         Day: ", df_max_travel_time.reset_index().loc[:,'day_of_week'][0])
    
    # display min travel time and related info
    min_travel_time = df["Trip Duration"].min()
    df_min_travel_time = df[df["Trip Duration"] == min_travel_time]
    print('    Minimum travel time: ',str(datetime.timedelta(seconds = int(min_travel_time))))
    print("         Start Station: ", df_min_travel_time.reset_index().loc[:,'Start Station'][0])
    print("         End Station: ", df_min_travel_time.reset_index().loc[:,'End Station'][0])
    print("         Month: ", df_min_travel_time.reset_index().loc[:,'month'][0])
    print("         Day: ", df_min_travel_time.reset_index().loc[:,'day_of_week'][0])
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_type = df['User Type'].value_counts()
    for i in range(len(count_user_type)):
        print("    ", count_user_type.keys()[i],": ",count_user_type[i])

    # Display counts of gender
    if 'Gender' in df.columns:
        count_gender = df['Gender'].value_counts()
    
        for i in range(len(count_gender)):
            print("    ", count_gender.keys()[i],": ",count_gender[i])
    
    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        earliest_year_birth = df['Birth Year'].min()
        most_recent_year_birth = df['Birth Year'].max()
        most_common_year_birth = df['Birth Year'].mode()[0]
        print("    Earliest year of birth: {}\n    Most recent year of birth: {}\n    Most common year of birth: {}"\
             .format(earliest_year_birth,most_recent_year_birth,most_common_year_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def get_stat():
    """Ask user to specify the type of statistics he'd like to view."""
    valid_input_stat = ['time_stats', 'station_stats', 'trip_duration_stats','user_stats','all',\
                       '1','2','3','4']
    response = ""
    stat = ""
    while response not in valid_input_stat :
        response = str(input("What statistics would you like to view? \n1: time_stats\n2: station_stats\n3: trip_duration_stats \n4: user_stats \nall: all statistics\n")).lower()
        if response not in valid_input_stat :
            print('Invalid input\n')
        elif response in ['1','2','3','4','5']:
            stat = valid_input_stat[int(response)-1]
        else:
            stat = response
    return(stat)

def display_5_lines(df,start_view):
    
    """ Displays five lines of raw data 
    Args:
         df: the dataframe we want to display
         start_view: The index where we'd to begin display """
    
    while True:
        response = input('\nWould you like to view 5 lines of raw data? Enter yes or no.\n')
        if response.lower() == 'yes':
            try:
                # For a better display of raw data
                print('    ' + '*'*40)
                print("    DISPLAYING 5 LINES OF RAW DATA")
                print('    '+ '*'*40)
                print(df.loc[start_view:,:].head())
                start_view = df.index[start_view + 5]
            except:
                print ('\n We have reached the last row, no more data to display')
                break
        else:
            break

    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        start_view = 0
        while True:
            stat = get_stat()
            print('*'*80)
            print("DISPLAYING STATISTICS FOR CITY = {}, MONTH = {}, DAY = {}\n".format(city,month,day))
            print('*'*80)
            if stat == 'time_stats':
                time_stats(df)
            elif stat == 'station_stats':
                station_stats(df)
            elif stat == 'trip_duration_stats':
                trip_duration_stats(df)
            elif stat == 'user_stats':
                user_stats(df)
            elif stat == 'all':
                time_stats(df)
                station_stats(df)
                trip_duration_stats(df)
                user_stats(df)
                break
            other_stat = input('\nWould you like to view other statistics? Enter yes or no.\n')
            if other_stat.lower() != 'yes':
                break
        # We initialise start_view at the begining of dataframe
        start_view = df.index[0]
        display_5_lines(df,start_view)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
