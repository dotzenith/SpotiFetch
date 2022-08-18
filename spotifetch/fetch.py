from typing import Any
import spotipy
import spotifetch.helpers as helpers
from kolorz.kolor import make_kolorz, get_all_colorschemes
import random

def fetch_profile(colors: Any, spotify_obj: spotipy.client.Spotify, 
                  term: str = 'short_term', all_artists: bool = False) -> tuple[str, str, str, str, str]:
    """
    Fetches data for the signed-in user's profile and formats it with colors
    """

    user = helpers.get_current_user_info(spotify_obj)

    # Currently Playing is handled differently than any of the others since
    # it's the only function that returns a None value
    current = helpers.get_currently_playing_stats(spotify_obj)
    if current is None:
        current = "NO CURRENTLY PLAYING TRACK"
    else:
        current = f"{current['track_name']} - {', '.join(current['artists']) if all_artists else current['artists'][0]}"

    recent = helpers.get_user_recently_played(spotify_obj)
    track = helpers.get_user_top_tracks(spotify_obj, term)[0]
    artist = helpers.get_user_top_artists(spotify_obj, term)[0]
    
    return f"{colors.color1}USER{colors.end}            {colors.white}{user}{colors.end}", \
           f"{colors.color2}NOW PLAYING{colors.end}     {colors.white}{current}{colors.end}", \
           f"{colors.color3}RECENT TRACK{colors.end}    {colors.white}{recent['track_name']} - {', '.join(recent['artists']) if all_artists else recent['artists'][0]}{colors.end}", \
           f"{colors.color4}TOP TRACK{colors.end}       {colors.white}{track['track_name']} - {', '.join(track['artists']) if all_artists else track['artists'][0]}{colors.end}", \
           f"{colors.color5}TOP ARTIST{colors.end}      {colors.white}{artist}{colors.end}"

def fetch_top_tracks(colors: Any, spotify_obj: spotipy.client.Spotify, 
                     term: str = 'short_term', all_artists: bool = False) -> tuple[str, str, str, str, str]:
    """
    Fetches top tracks for the signed-in user and formats it with colors
    """
    
    top_tracks = helpers.get_user_top_tracks(spotify_obj, term)

    return f"{colors.color1}{top_tracks[0]['track_name']} - {', '.join(top_tracks[0]['artists']) if all_artists else top_tracks[0]['artists'][0]}{colors.end}", \
           f"{colors.color2}{top_tracks[1]['track_name']} - {', '.join(top_tracks[1]['artists']) if all_artists else top_tracks[1]['artists'][0]}{colors.end}", \
           f"{colors.color3}{top_tracks[2]['track_name']} - {', '.join(top_tracks[2]['artists']) if all_artists else top_tracks[2]['artists'][0]}{colors.end}", \
           f"{colors.color4}{top_tracks[3]['track_name']} - {', '.join(top_tracks[3]['artists']) if all_artists else top_tracks[3]['artists'][0]}{colors.end}", \
           f"{colors.color5}{top_tracks[4]['track_name']} - {', '.join(top_tracks[4]['artists']) if all_artists else top_tracks[4]['artists'][0]}{colors.end}" 

def fetch_top_artists(colors: Any, spotify_obj: spotipy.client.Spotify, term: str = 'short_term') -> tuple[str, str, str, str, str]:
    """
    Fetches top artists for the signed-in user and formats it with colors
    """

    top_artists = helpers.get_user_top_artists(spotify_obj, term)

    return f"{colors.color1}{top_artists[0]}{colors.end}", \
           f"{colors.color2}{top_artists[1]}{colors.end}", \
           f"{colors.color3}{top_artists[2]}{colors.end}", \
           f"{colors.color4}{top_artists[3]}{colors.end}", \
           f"{colors.color5}{top_artists[4]}{colors.end}" 

def main(colorscheme: str = "catppuccin mocha", random_color: bool = True, category: str = 'profile', 
         term: str = 'short_term', art: bool = True, all_artists: bool = False, pywal: bool = True) -> None:
    """
    The big ol main function to put everything together and print the output
    """

    Spotipy = helpers.create_spotify("user-read-currently-playing user-top-read user-read-recently-played user-read-private")

    # Setting up the colors
    colorscheme = colorscheme.lower()
    if colorscheme in get_all_colorschemes():
        theme = make_kolorz(colorscheme, num_colors = True)
    else:
        theme = make_kolorz('catppuccin mocha', num_colors = True)
    
    # The only reason why this is done afterwards is to have a backup theme in case one can't be properly generated
    if art:
        theme = helpers.generate_colors(helpers.generate_image_url(category, Spotipy, term), theme)
    elif pywal:
        theme = helpers.fetch_pywal(theme)
    
    # Picking random colors for the outline
    if not random_color:
        logo_color = theme.color3
    else:
        val_list = list(theme.values())
        val_list.pop(5)
        logo_color = random.choice(val_list)

    if category == 'top_tracks':
        field_one, field_two, field_three, field_four, field_five = fetch_top_tracks(theme, Spotipy, term, all_artists)
    elif category == 'top_artists':
        field_one, field_two, field_three, field_four, field_five = fetch_top_artists(theme, Spotipy, term)
    else : 
        field_one, field_two, field_three, field_four, field_five = fetch_profile(theme, Spotipy, term, all_artists)

    output_art = f"      {logo_color}______{theme.end}" \
                 f"\n   {logo_color};;        ;;{theme.end}" \
                 f"\n {logo_color};;            ;;{theme.end}      {field_one}" \
                 f"\n{logo_color};;{theme.end}   {theme.color2}_..**.._{theme.end}   {logo_color};;{theme.end}     {field_two}" \
                 f"\n{logo_color};;{theme.end}   {theme.color3}_..**.._{theme.end}   {logo_color};;{theme.end}     {field_three}" \
                 f"\n{logo_color};;{theme.end}   {theme.color4}_..**.._{theme.end}   {logo_color};;{theme.end}     {field_four}" \
                 f"\n {logo_color};;            ;;{theme.end}      {field_five}" \
                 f"\n   {logo_color};;        ;;{theme.end}" \
                 f"\n      {logo_color}------{theme.end}" \
    
    print(output_art)

if __name__ == "__main__":
    main()
