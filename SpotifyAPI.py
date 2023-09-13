import spotipy
from playlist_analysis import PlaylistAnalyser
from playlist_csv_manager import PlaylistCSVManager
from playlist_maker import PlaylistMaker

# Read the sensitive information from a file
def read_credentials(filename):
    """
    Reads sensitive credentials from a file.
    
    Args:
        filename (str): The name of the file containing credentials.
    Returns:
        tuple: A tuple containing clientID, and clientSecret.
    """
    # Open the specified file in read mode
    with open(filename, 'r') as file:
        # Read all lines from the file
        lines = file.readlines()
        
        # Extract and strip the clientID, and clientSecret from lines
        clientID = lines[0].strip()
        clientSecret = lines[1].strip()
    
    # Return the extracted credentials as a tuple
    return clientID, clientSecret


# Creates an authenticated Spotify API object
def get_spotifyObject(clientID, clientSecret, redirect_uri):
    """
    Creates an authenticated Spotify API object using OAuth 2.0.
    
    Returns:
        spotipy.Spotify: An authenticated Spotify API object.
    """
    # Create a SpotifyOAuth object for authentication
    auth_manager = spotipy.SpotifyOAuth(
        clientID,   
        clientSecret,   
        redirect_uri   
    )
    
    # Create a Spotify API object using the authentication manager
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    return sp  # Return the authenticated Spotify API object


def menu():
    """
    Displays a main menu for the user to choose from different options.
    """
    # Assuming 'key.txt' is in the same directory as your script
    filename = 'key.txt'
    clientID, clientSecret = read_credentials(filename)
    redirect_uri = 'http://localhost:3000'

    spotifyObject = get_spotifyObject(clientID, clientSecret, redirect_uri)

    while True:  # Continue displaying the menu until the user chooses to exit
        print(
            "Welcome to the project," + 
            "\n0 - Exit the console" +
            "\n1 - Playlist CSV Analysis" +
            "\n2 - Create Playlist CSV file" +
            "\n3 - Make Playlist"
        )
        try:
            user_input = int(input("Enter Your Choice: "))  # Read the user's choice as an integer

            # Playlist CSV Analysis
            if user_input == 1:
                analyser = PlaylistAnalyser()  # Instantiate PlaylistAnalyser
                analyser.analyse()  # Call the analyse method to perform the analysis
            # Create Playlist CSV File
            elif user_input == 2:
                # Instantiate PlaylistCSVManager and call create_playlist_csv method
                csvManager = PlaylistCSVManager(spotifyObject)
                csvManager.create_playlist_csv()
            # Make Playlist
            elif user_input == 3:
                # Instantiate PlaylistMaker and call make_playlist method
                playlistMaker = PlaylistMaker(spotifyObject)
                playlistMaker.make_playlist()
            # Exit the console
            elif user_input == 0:
                print("Goodbye")
                return  # Exit the function and terminate the loop
            else:
                # User enters an integer that is not a valid option
                print("Invalid Input")
        except ValueError:
            # Error handling when input is in an invalid format (not an integer)
            print("Invalid Input")

    

#start main menu 
menu()