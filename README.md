# Spotify Playlist Analysis with Python

Welcome to the Spotify API Playlist project! This project aims to help you analyze and manipulate your Spotify playlists using Python and the Spotify Web API.

## Table of Contents

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Spotify API Playlist Project is a Python-based tool that allows you to perform various tasks on your Spotify playlists. These tasks include analyzing song data, creating new playlists, reordering tracks based on specific criteria, and more.

Aspiring data analysts like myself can use this project to practice Python programming, interact with the Spotify Web API, and analyze the contents of Spotify playlists. The project uses the `spotipy` library to authenticate and communicate with the Spotify API, `matplotlib`  library to plot the song data and the `pandas` library to manage and manipulate data.

## Requirements

- Python 3.x
- Spotipy library (`pip install spotipy`)
- Matplotlib library (`pip install matplotlib`)
- Pandas library (`pip install pandas`)
- NumPy library (`pip install numpy`)
  
## Features

- Authenticate with the Spotify API using OAuth 2.0 for secure access.
- Choose a playlist from your own Spotify account for analysis.
- Retrieve track details such as track name, artist(s), and date added.
- Create a CSV file containing the extracted track details.
- Customize the analysis and further process the data using Python's data manipulation capabilities.

## Installation

1. Clone the repository to your local machine:

   ```sh
   git clone https://github.com/danj0nes/SpotifyAPI-Playlist-Project.git
   cd SpotifyAPI-Playlist-Project
   ```
2. Install the required libraries using the commands mentioned above.

3. Create a Spotify developer account and set up your app to obtain the client ID and client secret.
   
4. Create a text file within the directory called key.txt
```
[clientID]
[clientSecret]
```

## Usage

1. Run the main script using `python SpotifyAPI.py`.
2. Follow the prompts to authenticate with the Spotify API.
3. Follow the on-screen instructions to perform different tasks such as analyzing playlists, creating new playlists, and reordering tracks.

## Features

- Analyze playlist data including song attributes, artists, and dates added.
- Create new playlists and add songs to them.
- Reorder tracks in a playlist based on specific criteria like "uplifting," "energy," etc.
- Visualize playlist data using graphs and charts.

## Project Structure

The project follows a structured organization:

SpotifyAPI-Playlist-Project/
<br>├── SpotifyAPI.py
<br>├── playlist_analysis.py
<br>├── playlist_maker.py
<br>├── playlist_csv_manager.pp
<br>├── playlist.csv
<br>├── key.txt
<br>├── README.md
<br>└── LICENSE

## Contributing

Contributions to this project are welcome! Feel free to open issues or submit pull requests for improvements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).
