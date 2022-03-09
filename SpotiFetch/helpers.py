import spotipy
from spotipy.oauth2 import SpotifyOAuth

def create_spotify(scope):
 
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    return spotify

def get_current_user_info(spotify_obj):
    
    current_user = spotify_obj.current_user()
    return current_user['display_name']

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

def get_user_recently_played(spotify_obj):
    
    recently_played = spotify_obj.current_user_recently_played(limit=1)

    return {'artist_name' : recently_played['items'][0]['track']['artists'][0]['name'],
            'track_name' : recently_played['items'][0]['track']['name']
    }

def get_user_top_artist(spotify_obj, term = 'short_term'):

    top_artists = spotify_obj.current_user_top_artists(limit=1, time_range=term)

    return top_artists['items'][0]['name']

def get_user_top_track(spotify_obj, term = 'short_term'):

    top_tracks = spotify_obj.current_user_top_tracks(limit=1, time_range=term)
    return {'artist_name' : top_tracks['items'][0]['artists'][0]['name'],
            'track_name' : top_tracks['items'][0]['name']
    }
