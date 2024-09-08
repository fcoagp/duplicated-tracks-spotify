import sys
print(sys.executable)

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter

SPOTIPY_CLIENT_ID = 'your Client ID'
SPOTIPY_CLIENT_SECRET = 'Your Client Secret'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

scope = "playlist-read-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

def get_playlist_tracks(playlist_link):
    playlist_id = playlist_link.split('/')[-1].split('?')[0]
    results = sp.playlist_tracks(playlist_id)
    tracks = []

    while results:
        tracks.extend(results['items'])
        results = sp.next(results) if results['next'] else None

    return tracks

def find_repeated_songs(tracks):

    song_list = [(track['track']['name'], track['track']['artists'][0]['name']) for track in tracks]

    song_count = Counter(song_list)

    repeated_songs = {song: count for song, count in song_count.items() if count > 1}

    if repeated_songs:
        print("Duplicated songs:")
        for song, count in repeated_songs.items():
            print(f"{song[0]} by {song[1]} - {count} times")
    else:
        print("No duplicated songs.")

if __name__ == "__main__":
    playlist_link = input("Introduce your playlist's link: ")
    tracks = get_playlist_tracks(playlist_link)
    find_repeated_songs(tracks)
