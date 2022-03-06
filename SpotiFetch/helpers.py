import spotipy
from spotipy.oauth2 import SpotifyOAuth

def create_spotify(scope):
 
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    return spotify

def get_currently_playing_stats(spotify_obj):
    
    currently_playing = spotify_obj.current_user_playing_track()
    
    if currently_playing is not None:
        return {'artist_name' : currently_playing['item']['artists'][0]['name'],
                'album_name' : currently_playing['item']['album']['name'],
                'track_name' : currently_playing['item']['name'],
                'track_progress' : currently_playing['progress_ms'],
                'track_duration' : currently_playing['item']['duration_ms'] 
        }

    return None

def get_user_stats():
    pass
