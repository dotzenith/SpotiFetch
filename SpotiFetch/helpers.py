import spotipy
from PIL import Image
import requests
from io import BytesIO
import colorgram
from os import makedirs
from appdirs import user_cache_dir
from spotipy.oauth2 import SpotifyOAuth

def create_spotify(scope):

    path = user_cache_dir("spotifetch")
    makedirs(path, exist_ok=True)
 
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_path=f"{path}/cache.txt"))
    return spotify

def get_current_user_info(spotify_obj):
    
    current_user = spotify_obj.current_user()
    return current_user['display_name'].upper()

def get_currently_playing_stats(spotify_obj):
    
    currently_playing = spotify_obj.current_user_playing_track()
    
    if currently_playing is not None:
        return {'artist_name' : currently_playing['item']['artists'][0]['name'].upper(),
                'album_name' : currently_playing['item']['album']['name'].upper(),
                'track_name' : currently_playing['item']['name'].upper(),
                'track_progress' : currently_playing['progress_ms'],
                'track_duration' : currently_playing['item']['duration_ms'] 
        }

    return None

def get_user_recently_played(spotify_obj):
    
    recently_played = spotify_obj.current_user_recently_played(limit=1)

    return {'artist_name' : recently_played['items'][0]['track']['artists'][0]['name'].upper(),
            'track_name' : recently_played['items'][0]['track']['name'].upper()
    }

def get_user_top_artists(spotify_obj, term = 'short_term'):

    top_artists = spotify_obj.current_user_top_artists(limit=5, time_range=term)

    return [artist['name'].upper() for artist in top_artists['items']]

def get_user_top_tracks(spotify_obj, term = 'short_term'):

    top_tracks = spotify_obj.current_user_top_tracks(limit=5, time_range=term)

    return [{'artist_name' : track['artists'][0]['name'].upper(),
             'track_name' : track['name'].upper()} for track in top_tracks['items']]

def generate_url(category, spotify_obj, term):
    
    if category == 'top_tracks':
        top_track = spotify_obj.current_user_top_tracks(limit=1, time_range=term)
        return top_track['items'][0]['album']['images'][1]['url']
    elif category == 'top_artists':
        top_artist = spotify_obj.current_user_top_artists(limit=1, time_range=term)
        return top_artist['items'][0]['images'][1]['url']
    else : 
        recently_played = spotify_obj.current_user_recently_played(limit=1)
        return recently_played['items'][0]['track']['album']['images'][1]['url']


def generate_colors(url, backup_colors):

    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    pallete = colorgram.extract(img, 5)

    colors = [f"#{color.rgb.r:02x}{color.rgb.g:02x}{color.rgb.b:02x}" for color in pallete]

    if len(colors) < 6:
        return backup_colors

    colors.append("#D9E0EE")

    return {
            "colorOne": colors[0],
            "colorTwo": colors[1],
            "colorThree": colors[2],
            "colorFour": colors[3],
            "colorFive": colors[4],
            "fg": colors[5],
    }
