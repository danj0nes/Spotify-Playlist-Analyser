import pandas as pd
import spotipy

def csv_playlist(sp):
    """
    Create a new Spotify playlist and add songs from a CSV file.
    
    Args:
        sp (spotipy.Spotify): An authenticated Spotify API object.
    """
    try:
        df = pd.read_csv('playlist.csv', parse_dates=['DateAdded'])  # Read the CSV file into a DataFrame
    except FileNotFoundError:
        print(f"File 'playlist.csv' not found.\nCreate a Playlist CSV File first")
        return
    
    playlist_name = input('Enter the name of the new playlist: ')
    # Create a new playlist
    playlist = sp.user_playlist_create(sp.username, playlist_name, public=True)

    # Add songs to the new playlist
    sp.playlist_add_items(playlist['id'], df['ID'].tolist())

    print(f'Playlist "{playlist_name}" created and songs added successfully!')


def choose_make_playlist(sp):
    """
    Display a menu for choosing actions related to playlist creation from a CSV file.
    
    Args:
        sp (spotipy.Spotify): An authenticated Spotify API object.
    """
    while True:
        print(
            "Pick Function" +
            "\n0 - Exit to main menu" +
            "\n1 - Make Playlist from CSV file"
        )
        try:
            user_input = int(input("Enter Your Choice: "))
            # Make Playlist from CSV file
            if user_input == 1:
                csv_playlist(sp)
            # Exit the console
            elif user_input == 0:
                return
            else:
                # User enters an integer that is not a valid option
                print("Invalid Input")
        except ValueError:
            print("Invalid Input")


class PlaylistMaker:
    def __init__(self, spotifyObject):
        """
        Initializes a PlaylistMaker instance with a Spotify API object.
        
        Args:
            spotifyObject (spotipy.Spotify): An authenticated Spotify API object.
        """
        self.spotifyObject = spotifyObject  # Store the Spotify API object in the instance

    def make_playlist(self):
        """
        Calls the choose_make_playlist function to initiate the process of creating a playlist from a CSV file.
        """
        choose_make_playlist(self.spotifyObject)  # Call the choose_make_playlist function with the stored Spotify API object
