import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

def added_at_graph(df):
    df['DateAdded'] = pd.to_datetime(df['DateAdded'])
    
    # Calculate the number of bars for each frequency (months, weeks, and days)
    songs_added_count_days = df.groupby(pd.Grouper(key='DateAdded', freq='1D')).size()

    # Calculate the cumulative sum of songs added
    cumulative_songs_added = songs_added_count_days.cumsum()

    plt.figure(figsize=(12, 6))
    plt.plot(cumulative_songs_added.index, cumulative_songs_added.values)  # Plot the cumulative line graph
    
    plt.xlabel('Date Added (Days)')
    plt.ylabel('Cumulative Number of Songs Added')
    plt.title('Cumulative Songs Added Over Time')
    
    # Format x-axis labels with the chosen frequency format using DateFormatter
    plt.gca().xaxis.set_major_formatter(DateFormatter('%d-%b-%Y'))
    
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.grid(True)  # Add grid lines to the plot
    
    plt.tight_layout()  # Adjust the layout to prevent overlapping elements
    plt.show()  # Show the plot

def composite_graph(df):
    plt.figure(figsize=(10, 6))
    # Plot the line graph
    plt.plot(range(1, df.shape[0] + 1), df['Composite Value'], marker='o', linestyle='-', color='b')

    # Add labels and title
    plt.xlabel('Song Number')
    plt.ylabel('Composite Value')
    plt.title('Composite Value vs. Song Number')

    plt.grid(True)
    plt.tight_layout()
    plt.show()

def artist_pie_chart(df):
    # Group by artist and count the occurrences
    artist_counts = df['Artist'].value_counts()

    # Plotting
    plt.figure(figsize=(10, 8))
    plt.pie(artist_counts, labels=artist_counts.index, autopct='%1.0f', startangle=140)
    plt.title('Artist Distribution')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.tight_layout()
    plt.show()

def analyze_dataframe(df):
    # Display general information about the DataFrame
    print("DataFrame Info:")
    print(df.info())
    print("\n")

    # Display basic statistics about the composite value column
    print("\nComposite Value Statistics:")
    print(df['Composite Value'].describe())
    print("\n")

    # Display the number of unique songs and artists
    num_unique_songs = df['Name'].nunique()
    num_unique_artists = df['Artist'].nunique()
    print(f"\nNumber of Unique Songs: {num_unique_songs}")
    print(f"Number of Unique Artists: {num_unique_artists}")
    print("\n")

    # Display the earliest and latest dates in the 'Date Added' column
    earliest_date = df['Date Added'].min()
    latest_date = df['Date Added'].max()
    print(f"\nEarliest Date Added: {earliest_date}")
    print(f"Latest Date Added: {latest_date}")
    print("\n")

    # Display the song with the highest and lowest composite value
    max_composite_song = df.loc[df['Composite Value'].idxmax()]
    min_composite_song = df.loc[df['Composite Value'].idxmin()]
    print(f"\nSong with Highest Composite Value:")
    print(max_composite_song[['Name', 'Artist', 'Composite Value']])
    print(f"\nSong with Lowest Composite Value:")
    print(min_composite_song[['Name', 'Artist', 'Composite Value']])
    print("\n")

    # Composite value statistics
    composite_mean = df['Composite Value'].mean()
    composite_median = df['Composite Value'].median()
    composite_std = df['Composite Value'].std()
    print(f"Composite Value Mean: {composite_mean:.3f}")
    print(f"Composite Value Median: {composite_median:.3f}")
    print(f"Composite Value Standard Deviation: {composite_std:.3f}")
    print("\n")

def choose_equation():
    """
    Prompts the user to choose an equation number.
    
    Returns:
        int: The selected equation number.
    """
    print(
        "Pick Equation" +
        "\n1 - positive straight line" +
        "\n2 - negative straight line" +
        "\n3 - positive parabola" +
        "\n4 - negative parabola" +
        "\n5 - positive cubic" +
        "\n6 - negative cubic"
    )
    while True:
        try:
            user_input = int(input("Enter Your Choice: "))
            if user_input > 0 and user_input < 7:
                return user_input
            else:
                print("Invalid Input")

        except ValueError:
            print("Invalid Input")



def rearrange_to_shape(df, equation_number):
    """
    Rearranges the rows of the DataFrame based on the provided equation number.
    
    Args:
        df (pd.DataFrame): The DataFrame containing song data.
        equation_number (int): The equation number for shaping the data.
        
    Returns:
        pd.DataFrame: The DataFrame with rows rearranged.
    """
    def equation_y(x, equation_number, t):
        """
        Calculates the y value using the specified equation number.
        
        Args:
            x (float): The x value.
            equation_number (int): The equation number.
            t (int): The number of playlist tracks.
            
        Returns:
            float: The calculated y value.
        """
        x_over_t = x / t
        if equation_number == 1:
            return x_over_t
        elif equation_number == 2:
            return (-x_over_t) + 1
        elif equation_number == 3:
            return 4 * pow(x_over_t, 2) - 4 * x_over_t + 1
        elif equation_number == 4:
            return -4 * pow(x_over_t, 2) + 4 * x_over_t
        elif equation_number == 5:
            return 9 * pow(x_over_t, 3) - (27/2) * pow(x_over_t, 2) + (11/2) * x_over_t
        else:  # (equation_number == 6):
            return -9 * pow(x_over_t, 3) + (27/2) * pow(x_over_t, 2) - (11/2) * x_over_t + 1
    
    # Generate values for the equation
    a = [equation_y(x + 1, equation_number, len(df)) for x in df['Composite Value'].index]
    b = df['Composite Value'].values

    # Step 1: Sort list a in increasing order while keeping track of original positions
    a_with_original_positions = [(value, index) for index, value in enumerate(a)]
    sorted_a = sorted(a_with_original_positions)
    a_original_position = [index for _, index in sorted_a]

    # Step 2: Sort list b in increasing order while keeping track of original positions
    b_with_original_positions = [(value, index) for index, value in enumerate(b)]
    sorted_b = sorted(b_with_original_positions)
    b_original_position = [index for _, index in sorted_b]

    # Step 3: Match elements in sorted list b to their corresponding elements in sorted list a
    # Step 4: Sort new list using index of list a and create the target positions list

    a_with_original_position_and_b_original_position = list(zip(a_original_position, b_original_position))
    b_in_original_positions_with_target = sorted(a_with_original_position_and_b_original_position)
    targeted_positions = [target for _, target in b_in_original_positions_with_target]

    # Use the best permutation to reorder your data
    reordered_df = df.iloc[targeted_positions]

    return reordered_df


def choose_analysis(df):
    """
    Presents a menu for various analysis options on the playlist DataFrame.
    
    Args:
        df (pd.DataFrame): The DataFrame containing playlist data.
    """
    while True:
        print(
            "Pick Function"
            "\n0 - Exit to main menu" +
            "\n1 - Display date added graph" +
            "\n2 - Display composite 'uplifting' graph" +
            "\n3 - Rearrange playlist csv in an 'uplifting' shape" +
            "\n4 - Display dataframe stats"
            "\n5 - Display Artist pie chart"
        )
        try:
            user_input = int(input("Enter Your Choice: "))
            # Display date added graph
            if user_input == 1:
                added_at_graph(df)
            # Display composite 'uplifting' graph
            elif user_input == 2:
                composite_graph(df)
            # Rearrange playlist to 'uplifting' shape
            elif user_input == 3:
                equation_number = choose_equation()  # Call function to choose equation
                df = rearrange_to_shape(df, equation_number)  # Rearrange DataFrame
                df.to_csv('playlist.csv', index=False)  # Save rearranged DataFrame to CSV
            elif user_input == 4:
                analyze_dataframe(df)  # Analyze and display DataFrame stats
            elif user_input == 5:
                artist_pie_chart(df)  # Display Artist pie chart
            # Exit the console
            elif user_input == 0:
                return
            else:
                # User enters an integer that is not a valid option
                print("Invalid Input")

        except ValueError as e:
            # Error handling when input is in an invalid format (not an integer)
            print(e)


class PlaylistAnalyser:
    def analyse(self):
        """
        Initiates the analysis process for a playlist CSV file.
        """
        try:
            df = pd.read_csv('playlist.csv',  parse_dates=['DateAdded'])  # Read the CSV file into a DataFrame
        except FileNotFoundError:
            print(f"File '{'playlist.csv'}' not found.\nCreate a Playlist CSV File first")
            return
        
        choose_analysis(df)  # Call the choose_analysis function with the DataFrame

        
        
        
        
        

        
