import os
import spotipy
import pandas as pd
import numpy as np


def get_selected_playlist(playlists):
    """
    Displays a list of playlists and prompts the user to select one for analysis.

    Args:
        playlists (dict): A dictionary of playlists with names as keys and IDs as values.
    Returns:
        int: The index of the selected playlist (0-based) or -1 if invalid input.
    """
    print("Your playlists:")
    
    # Display the list of playlists with their corresponding numbers
    for idx, playlist_name in enumerate(playlists.keys(), start=1):
        print(f"{idx}. {playlist_name}")
    
    while True:
        # Prompt the user to enter the number of the playlist they want to analyze
        choice = input("Enter the number of the playlist you want to analyze: ")
    
        try:
            # Attempt to convert the user input to an integer
            selected_index = int(choice) - 1
        
            # Check if the selected index is within the valid range
            if 0 <= selected_index < len(playlists):
                return selected_index
            else:
                # Invalid input, ask the user again
                print("Invalid input. Please enter a valid number.")
        except ValueError:
            # If the input cannot be converted to an integer, ask the user again
            print("Invalid input. Please enter a valid number.")


def choose_playlist(spotify_object):
    """
    Allows the user to choose a playlist from their Spotify account for analysis.
    
    Args:
        spotify_object (spotipy.Spotify): An authenticated Spotify API object.
    Returns:
        str: The ID of the selected playlist for analysis.
    """
    # Retrieve the user's playlists from their Spotify account
    user_playlists = spotify_object.current_user_playlists()
    playlists = {}
    
    # Create a dictionary of playlist names and IDs
    for playlist in user_playlists['items']:
        playlists[playlist['name']] = playlist['id']

    # Get the index of the selected playlist based on user input
    selected_playlist_idx = get_selected_playlist(playlists)
    
    # Get the name and ID of the selected playlist
    selected_playlist_name = list(playlists.keys())[selected_playlist_idx]
    selected_playlist_id = playlists[selected_playlist_name]
    
    return selected_playlist_id  # Return the ID of the selected playlist


def get_feature_composite_value(spotify, track_id):
    try:
        # Make an API call to get the track features using the 'audio_features' endpoint of the Spotify API
        track_features = spotify.audio_features(track_id)
        
        # Check if track_features is not empty and contains at least one element
        if track_features and len(track_features) > 0:
            track_features = track_features[0]
            
            # Retrieve specific audio features from the track_features dictionary using get()
            energy = track_features.get('energy', 1) # least 0.0 - most 1.0
            danceability = track_features.get('danceability', 1) # least 0.0 - most 1.0
            tempo = track_features.get('tempo', 1) # bpm
            tempo = max(60, min(tempo, 140)) - 60
            tempo /= 80
            loudness = track_features.get('loudness', 1) # least -60db - most 0db
            loudness += 60
            loudness /= 60
            valence = track_features.get('valence', 1) # least 0.0 - most 1.0

            #power function
            #weighting
            #harmonic/ geometric mean
            composite_value = energy * danceability * tempo * loudness * valence
            composite_value = np.around(composite_value, 3 - int(np.floor(np.log10(abs(composite_value)))) - 1)
            
            # Return the extracted audio features
            return composite_value
        else:
            # If track_features is empty or has no elements, return None for all audio features
            print(f"Track with ID {track_id} has no track features")
            return None
    except Exception as e:
        # Handle exceptions that may occur during the API call
        print(f"Error fetching features for track with ID {track_id}: {e}")
        return None


def get_playlist_tracks(sp, playlist_id):
    """
    Retrieves all tracks from a specified Spotify playlist and extracts relevant information.
    
    Args:
        sp (spotipy.Spotify): An authenticated Spotify API object.
        playlist_id (str): The ID of the playlist to retrieve tracks from.
        
    Returns:
        list: A list of dictionaries containing track details (Name, Artist, DateAdded, Energy, Danceability, Tempo, Loudness, Valence).
    """
    tracks = []  # Initialize an empty list to store track information
    offset = 0   # Initialize the starting offset for pagination
    limit = 100  # Set the maximum number of tracks to retrieve per API call
    
    while True:
        # Retrieve tracks from the specified playlist using the Spotify API with pagination
        results = sp.playlist_tracks(playlist_id, fields='items(track(name, artists, id), added_at)', offset=offset, limit=limit)
        
        # Break the loop if there are no more tracks (i.e., the 'items' list is empty)
        if not results['items']:
            break
        
        # Extract relevant information for each track
        for item in results['items']:
            track = item['track']
            
            # Create a dictionary containing track information
            track_data = {
                'Name': track['name'],
                'Artist': ', '.join([artist['name'] for artist in track['artists']]),
                'ID': track['id'],
                'DateAdded': item['added_at'],
                'Composite Value': get_feature_composite_value(sp, track['id'])
            }
            
            # Add track data to the list of tracks
            tracks.append(track_data)
        
        offset += limit  # Increment the offset to fetch the next set of tracks in the next iteration
        
    return tracks  # Return the list of track details




def create_csv(sp, playlist_id):
    """
    Creates a CSV file containing track details from a specified Spotify playlist.
    
    Args:
        sp (spotipy.Spotify): An authenticated Spotify API object.
        playlist_id (str): The ID of the playlist to retrieve tracks from and create the CSV file.
    """
    # Retrieve tracks from the specified playlist using the get_playlist_tracks function
    tracks = get_playlist_tracks(sp, playlist_id)
    
    # Create a DataFrame from the track details
    df = pd.DataFrame(tracks)
    
    # Write the DataFrame to a CSV file named 'playlist.csv'
    df.to_csv('playlist.csv', index=False)
    
    # Print a message to indicate successful creation of the CSV file
    print("Playlist CSV file created")



class PlaylistCSVManager:
    def __init__(self, spotifyObject):
        """
        Initializes a PlaylistCSVManager instance with a Spotify API object.
        
        Args:
            spotifyObject (spotipy.Spotify): An authenticated Spotify API object.
        """
        self.spotifyObject = spotifyObject  # Store the Spotify API object in the instance
    
    def create_playlist_csv(self):
        """
        Creates a CSV file containing track details from a user-selected playlist.
        """
        # Call the choose_playlist function to allow the user to pick a playlist
        selected_playlist_id = choose_playlist(self.spotifyObject)
        
        # Call the create_csv function to create the CSV file using the selected playlist ID
        create_csv(self.spotifyObject, selected_playlist_id)
