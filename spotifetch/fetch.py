import spotifetch.helpers as helpers
from spotifetch.colors import colors
import random

# Escape sequence to end colored output
ENDCOLOR = "\033[0m"

def fetch_profile(colors, spotify_obj, term='short_term', all_artists=False):
    
    user = helpers.get_current_user_info(spotify_obj)

    '''
    Currently Playing is handled differently than any of the others since
    it's the only function that returns a None value
    '''
    current = helpers.get_currently_playing_stats(spotify_obj)
    if current is None:
        current = "NO CURRENTLY PLAYING TRACK"
    else:
        current = f"{current['track_name']} - {', '.join(current['artists']) if all_artists else current['artists'][0]}"

    recent = helpers.get_user_recently_played(spotify_obj)
    track = helpers.get_user_top_tracks(spotify_obj, term)[0]
    artist = helpers.get_user_top_artists(spotify_obj, term)[0]
    
    return f"{colors['colorOne']}USER{ENDCOLOR}            {colors['fg']}{user}{ENDCOLOR}", \
           f"{colors['colorTwo']}NOW PLAYING{ENDCOLOR}     {colors['fg']}{current}{ENDCOLOR}", \
           f"{colors['colorThree']}RECENT TRACK{ENDCOLOR}    {colors['fg']}{recent['track_name']} - {', '.join(recent['artists']) if all_artists else recent['artists'][0]}{ENDCOLOR}", \
           f"{colors['colorFour']}TOP TRACK{ENDCOLOR}       {colors['fg']}{track['track_name']} - {', '.join(track['artists']) if all_artists else track['artists'][0]}{ENDCOLOR}", \
           f"{colors['colorFive']}TOP ARTIST{ENDCOLOR}      {colors['fg']}{artist}{ENDCOLOR}"

def fetch_top_tracks(colors, spotify_obj, term='short_term', all_artists=False):

    top_tracks = helpers.get_user_top_tracks(spotify_obj, term)

    return f"{colors['colorOne']}{top_tracks[0]['track_name']} - {', '.join(top_tracks[0]['artists']) if all_artists else top_tracks[0]['artists'][0]}{ENDCOLOR}", \
           f"{colors['colorTwo']}{top_tracks[1]['track_name']} - {', '.join(top_tracks[1]['artists']) if all_artists else top_tracks[1]['artists'][0]}{ENDCOLOR}", \
           f"{colors['colorThree']}{top_tracks[2]['track_name']} - {', '.join(top_tracks[2]['artists']) if all_artists else top_tracks[2]['artists'][0]}{ENDCOLOR}", \
           f"{colors['colorFour']}{top_tracks[3]['track_name']} - {', '.join(top_tracks[3]['artists']) if all_artists else top_tracks[3]['artists'][0]}{ENDCOLOR}", \
           f"{colors['colorFive']}{top_tracks[4]['track_name']} - {', '.join(top_tracks[4]['artists']) if all_artists else top_tracks[4]['artists'][0]}{ENDCOLOR}" 

def fetch_top_artists(colors, spotify_obj, term='short_term'):

    top_artists = helpers.get_user_top_artists(spotify_obj, term)

    return f"{colors['colorOne']}{top_artists[0]}{ENDCOLOR}", \
           f"{colors['colorTwo']}{top_artists[1]}{ENDCOLOR}", \
           f"{colors['colorThree']}{top_artists[2]}{ENDCOLOR}", \
           f"{colors['colorFour']}{top_artists[3]}{ENDCOLOR}", \
           f"{colors['colorFive']}{top_artists[4]}{ENDCOLOR}" 

def main(colorscheme="catppuccin", random_color=True, category='profile', term='short_term', art=True, all_artists=False, pywal=True):
    Spotipy = helpers.create_spotify("user-read-currently-playing user-top-read user-read-recently-played user-read-private")

    # Setting up the colors
    colorscheme = colorscheme.lower()
    if colorscheme in colors.keys():
        theme = colors[colorscheme]
    else:
        theme = colors['catppuccin']
    
    # The only reason why this is done afterwards is to have a backup theme in case one can't be properly generated
    if art:
        theme = helpers.generate_colors(helpers.generate_url(category, Spotipy, term), theme)
    elif pywal:
        theme = helpers.fetch_pywal(theme)
    
    # Converting the colors to term color format
    helpers.term_colorify(theme)

    # Picking random colors for the outline
    if not random_color:
        logo_color = theme['colorFour']
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

    art = f"      {logo_color}______{ENDCOLOR}" \
          f"\n   {logo_color};;        ;;{ENDCOLOR}" \
          f"\n {logo_color};;            ;;{ENDCOLOR}      {field_one}" \
          f"\n{logo_color};;{ENDCOLOR}   {theme['colorTwo']}_..**.._{ENDCOLOR}   {logo_color};;{ENDCOLOR}     {field_two}" \
          f"\n{logo_color};;{ENDCOLOR}   {theme['colorThree']}_..**.._{ENDCOLOR}   {logo_color};;{ENDCOLOR}     {field_three}" \
          f"\n{logo_color};;{ENDCOLOR}   {theme['colorFour']}_..**.._{ENDCOLOR}   {logo_color};;{ENDCOLOR}     {field_four}" \
          f"\n {logo_color};;            ;;{ENDCOLOR}      {field_five}" \
          f"\n   {logo_color};;        ;;{ENDCOLOR}" \
          f"\n      {logo_color}------{ENDCOLOR}" \
    
    print(art)

if __name__ == "__main__":
    main()
