from SpotiFetch.helpers import *
from SpotiFetch.colors import colors
import random
from rich import print

def main(random_color=False):
    Spotipy = create_spotify("user-read-currently-playing user-top-read user-read-recently-played user-read-private")
    
    current_user = get_current_user_info(Spotipy)

    '''
    Now Playing is handled differently than any of the others since
    it's the only function that returns a None value
    '''
    now_playing = get_currently_playing_stats(Spotipy)
    if now_playing is None:
        now_playing = "Now currently playing track"
    else:
        now_playing = f"{now_playing['track_name']} - {now_playing['artist_name']}"

    recently_played = get_user_recently_played(Spotipy)
    top_track = get_user_top_track(Spotipy)
    top_artist = get_user_top_artist(Spotipy)
    
    theme = colors['catppuccin']

    if not random_color:
        logo_color = theme['colorFour']
    elif random_color:
        logo_color = random.choice([theme.values()]) 

    new_art = f"      [logo_color]______[/logo_color]" \
              f"\n   [logo_color];;        ;;[/logo_color]" \
              f"\n [logo_color];;            ;;[/logo_color]      [logo_color]USER[/logo_color]            {current_user}" \
              f"\n[logo_color];;   _..**.._   ;;[/logo_color]     [blue]NOW PLAYING[/blue]     {now_playing}" \
              f"\n[logo_color];;   _..**.._   ;;[/logo_color]     [magenta]RECENT TRACK[/magenta]    {recently_played['track_name']} - {recently_played['artist_name']}" \
              f"\n[logo_color];;   _..**.._   ;;[/logo_color]     [yellow]TOP TRACK[/yellow]       {top_track['track_name']} - {top_track['artist_name']}" \
              f"\n [logo_color];;            ;;[/logo_color]      [cyan]TOP ARTIST[/cyan]      {top_artist}" \
              f"\n   [logo_color];;        ;;[/logo_color]" \
              f"\n      [logo_color]------[/logo_color]" \

    print(new_art)

if __name__ == "__main__":
    main()
