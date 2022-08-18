from typing import Any, Optional
import spotipy
import json
import random
from PIL import Image
import requests
from io import BytesIO
import colorgram
from os import makedirs
from os.path import expanduser, exists
from appdirs import user_cache_dir
from spotipy.oauth2 import SpotifyOAuth
from kolorz.kolor import make_kolorz

def create_spotify(scope: str) -> spotipy.client.Spotify:
    '''
    create_spotify(scope) -> spotipy object

    Creates a spotify object given a scope

    :param scope - set of permissions the spotify object will have from the user account
    '''

    path = user_cache_dir("spotifetch")
    makedirs(path, exist_ok=True)
 
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_path=f"{path}/cache.txt"))
    return spotify

def get_current_user_info(spotify_obj: spotipy.client.Spotify) -> str:
    '''
    Returns the username of the authenticated user

    :param spotify_obj - a spotify object created using create_spotify. 
    
    NOTE: spotify_obj must be created with the user-read-private scope
    '''

    current_user = spotify_obj.current_user()
    return current_user['display_name'].upper()

def get_currently_playing_stats(spotify_obj: spotipy.client.Spotify) -> Optional[dict[str, Any]]:
    '''
    Returns a dictionary containing information about the authenticated user's currently playing track if a track is currently playing

    Returns None if track is currently playing

    :param spotify_obj - a spotify object created using create_spotify. 
    
    NOTE: spotify_obj must be created with the user-read-currently-playing scope
    '''
    
    currently_playing = spotify_obj.current_user_playing_track()
    
    if currently_playing is not None:

        return {'artists' : [artist['name'].upper() for artist in currently_playing['item']['artists']],
                'album_name' : currently_playing['item']['album']['name'].upper(),
                'track_name' : currently_playing['item']['name'].upper(),
                'track_progress' : currently_playing['progress_ms'],
                'track_duration' : currently_playing['item']['duration_ms'] 
        }

    return None

def get_user_recently_played(spotify_obj: spotipy.client.Spotify) -> dict[str, Any]:
    '''
    Returns a dictionary containing information about the authenticated user's recently played track

    :param spotify_obj - a spotify object created using create_spotify. 
    
    NOTE: spotify_obj must be created with the user-read-recently-played scope
    '''

    recently_played = spotify_obj.current_user_recently_played(limit=1)

    return {'artists' : [artist['name'].upper() for artist in recently_played['items'][0]['track']['artists']],
            'track_name' : recently_played['items'][0]['track']['name'].upper()
    }

def get_user_top_artists(spotify_obj: spotipy.client.Spotify, term: str = 'short_term') -> list[str]:
    '''
    Returns a list containing the authenticated user's top artists for a given time period

    :param spotify_obj - a spotify object created using create_spotify.
    :param term - the time period which the top artists should be fetched from. Can be: short_term, medium_term, or long_term
    
    NOTE: spotify_obj must be created with the user-top-read scope
    '''

    top_artists = spotify_obj.current_user_top_artists(limit=5, time_range=term)

    return [artist['name'].upper() for artist in top_artists['items']]

def get_user_top_tracks(spotify_obj: spotipy.client.Spotify, term: str = 'short_term') -> list[dict[str, Any]]:
    '''
    Returns a list containing information about the authenticated user's top tracks for a given time period

    :param spotify_obj - a spotify object created using create_spotify.
    :param term - the time period which the top tracks should be fetched from. Can be: short_term, medium_term, or long_term
    
    NOTE: spotify_obj must be created with the user-top-read scope
    '''
    
    top_tracks = spotify_obj.current_user_top_tracks(limit=5, time_range=term)

    return [{'artists' : [artist['name'].upper() for artist in track['artists']],
             'track_name' : track['name'].upper()} for track in top_tracks['items']]

def generate_image_url(category: str, spotify_obj: spotipy.client.Spotify, term: str) -> str:
    '''
    Returns a url for the cover art of a song or the profile picture of an artist given a category

    :param category - Can be: top_tracks, top_artists, or profile.  
    :param spotify_obj - a spotify object created using create_spotify.
    :param term - the time period which the top artists should be fetched from. Can be: short_term, medium_term, and long_term
    '''

    
    if category == 'top_tracks':
        top_track = spotify_obj.current_user_top_tracks(limit=1, time_range=term)
        return top_track['items'][0]['album']['images'][1]['url']
    elif category == 'top_artists':
        top_artist = spotify_obj.current_user_top_artists(limit=1, time_range=term)
        return top_artist['items'][0]['images'][1]['url']
    else : 
        recently_played = spotify_obj.current_user_recently_played(limit=1)
        return recently_played['items'][0]['track']['album']['images'][1]['url']


def hex_to_rgb(hex: str) -> tuple[int, int, int]:
    '''
    Returns a dictionary of RGB values given a color in hex

    :param hex - color value in hex
    '''

    r = hex[1:3]
    g = hex[3:5]
    b = hex[5:7]

    return (int(r, 16), int(g, 16), int(b, 16))

def generate_colors(url: str, backup_colors: dict[str, str]) -> Any:
    '''
    Returns a color scheme generated from the image url

    The return type is set to Any since it returns a pseudo dict

    :param url - image url to generate the color scheme from
    :backup_colors - a backup color scheme in case one can't be generated from the given url
    '''
    
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    pallete = colorgram.extract(img, 5)

    colors = [(color.rgb.r, color.rgb.g, color.rgb.b) for color in pallete]

    if len(colors) < 5:
        return backup_colors

    colors.append((217, 224, 238))

    generated_colors = {
                "color1": colors[1],
                "color2": colors[0],
                "color3": colors[2],
                "color4": colors[3],
                "color5": colors[4],
                "white": colors[5],
    }

    return make_kolorz(custom=generated_colors)

def fetch_pywal(backup_colors: dict[str, str]) -> Any:
    '''
    Returns a color scheme generated by pywal

    The return type is set to any since it returns a pseudo dict

    :backup_colors - a backup color scheme in case colors.json does not exist
    '''

    color_file = f"{expanduser('~')}/.cache/wal/colors.json"

    if not(exists(color_file)):
        return backup_colors

    with open(color_file) as color_file:
        colors = json.load(color_file)

    fg = colors['special']['foreground']
    bg = colors['special']['background']
    
    color_list = [color for color in colors['colors'].values()]
    
    # Removing the background color from the total selection of colors
    if bg in color_list:
        color_list.remove(bg)
    
    rand_colors = random.sample(color_list,5)
    
    generated_colors = {
                "color1": hex_to_rgb(rand_colors[0]),
                "color2": hex_to_rgb(rand_colors[1]),
                "color3": hex_to_rgb(rand_colors[2]),
                "color4": hex_to_rgb(rand_colors[3]),
                "color5": hex_to_rgb(rand_colors[4]),
                "white": hex_to_rgb(fg),
    }

    return make_kolorz(custom=generated_colors)

