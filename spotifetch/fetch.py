import spotifetch.helpers as helpers
from spotifetch.colors import colors
import random
from rich import print

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
    
    return f"[{colors['colorOne']}]USER[/{colors['colorOne']}]            [{colors['fg']}]{user}[/{colors['fg']}]", \
           f"[{colors['colorTwo']}]NOW PLAYING[/{colors['colorTwo']}]     [{colors['fg']}]{current}[/{colors['fg']}]", \
           f"[{colors['colorThree']}]RECENT TRACK[/{colors['colorThree']}]    [{colors['fg']}]{recent['track_name']} - {', '.join(recent['artists']) if all_artists else recent['artists'][0]}[/{colors['fg']}]", \
           f"[{colors['colorFour']}]TOP TRACK[/{colors['colorFour']}]       [{colors['fg']}]{track['track_name']} - {', '.join(track['artists']) if all_artists else track['artists'][0]}[/{colors['fg']}]", \
           f"[{colors['colorFive']}]TOP ARTIST[/{colors['colorFive']}]      [{colors['fg']}]{artist}[/{colors['fg']}]"

def fetch_top_tracks(colors, spotify_obj, term='short_term', all_artists=False):

    top_tracks = helpers.get_user_top_tracks(spotify_obj, term)

    return f"[{colors['colorOne']}]{top_tracks[0]['track_name']} - {', '.join(top_tracks[0]['artists']) if all_artists else top_tracks[0]['artists'][0]}[/{colors['colorOne']}]", \
           f"[{colors['colorTwo']}]{top_tracks[1]['track_name']} - {', '.join(top_tracks[1]['artists']) if all_artists else top_tracks[1]['artists'][0]}[/{colors['colorTwo']}]", \
           f"[{colors['colorThree']}]{top_tracks[2]['track_name']} - {', '.join(top_tracks[2]['artists']) if all_artists else top_tracks[2]['artists'][0]}[/{colors['colorThree']}]", \
           f"[{colors['colorFour']}]{top_tracks[3]['track_name']} - {', '.join(top_tracks[3]['artists']) if all_artists else top_tracks[3]['artists'][0]}[/{colors['colorFour']}]", \
           f"[{colors['colorFive']}]{top_tracks[4]['track_name']} - {', '.join(top_tracks[4]['artists']) if all_artists else top_tracks[4]['artists'][0]}[/{colors['colorFive']}]" 

def fetch_top_artists(colors, spotify_obj, term='short_term'):

    top_artists = helpers.get_user_top_artists(spotify_obj, term)

    return f"[{colors['colorOne']}]{top_artists[0]}[/{colors['colorOne']}]", \
           f"[{colors['colorTwo']}]{top_artists[1]}[/{colors['colorTwo']}]", \
           f"[{colors['colorThree']}]{top_artists[2]}[/{colors['colorThree']}]", \
           f"[{colors['colorFour']}]{top_artists[3]}[/{colors['colorFour']}]", \
           f"[{colors['colorFive']}]{top_artists[4]}[/{colors['colorFive']}]" 

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

    art = f"      [{logo_color}]______[/{logo_color}]" \
          f"\n   [{logo_color}];;        ;;[/{logo_color}]" \
          f"\n [{logo_color}];;            ;;[/{logo_color}]      {field_one}" \
          f"\n[{logo_color}];;[/{logo_color}]   [{theme['colorTwo']}]_..**.._[{theme['colorTwo']}]   [{logo_color}];;[/{logo_color}]     {field_two}" \
          f"\n[{logo_color}];;[/{logo_color}]   [{theme['colorThree']}]_..**.._[{theme['colorThree']}]   [{logo_color}];;[/{logo_color}]     {field_three}" \
          f"\n[{logo_color}];;[/{logo_color}]   [{theme['colorFour']}]_..**.._[{theme['colorFour']}]   [{logo_color}];;[/{logo_color}]     {field_four}" \
          f"\n [{logo_color}];;            ;;[/{logo_color}]      {field_five}" \
          f"\n   [{logo_color}];;        ;;[/{logo_color}]" \
          f"\n      [{logo_color}]------[/{logo_color}]" \
    
    print(art)

if __name__ == "__main__":
    main()
