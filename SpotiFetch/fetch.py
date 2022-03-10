from SpotiFetch.helpers import *
from SpotiFetch.colors import colors
import random
from rich import print

def format_info(colors, user, now, recent, track, artist):
    
    return f"[{colors['colorOne']}]USER[/{colors['colorOne']}]            [{colors['fg']}]{user}[/{colors['fg']}]", \
           f"[{colors['colorTwo']}]NOW PLAYING[/{colors['colorTwo']}]     [{colors['fg']}]{now}[/{colors['fg']}]", \
           f"[{colors['colorThree']}]RECENT TRACK[/{colors['colorThree']}]    [{colors['fg']}]{recent['track_name']} - {recent['artist_name']}[/{colors['fg']}]", \
           f"[{colors['colorFour']}]TOP TRACK[/{colors['colorFour']}]       [{colors['fg']}]{track['track_name']} - {track['artist_name']}[/{colors['fg']}]", \
           f"[{colors['colorFive']}]TOP ARTIST[/{colors['colorFive']}]      [{colors['fg']}]{artist}[/{colors['fg']}]"

def main(colorscheme="catppuccin", random_color=True):
    Spotipy = create_spotify("user-read-currently-playing user-top-read user-read-recently-played user-read-private")
    
    current_user = get_current_user_info(Spotipy)

    '''
    Now Playing is handled differently than any of the others since
    it's the only function that returns a None value
    '''
    now_playing = get_currently_playing_stats(Spotipy)
    if now_playing is None:
        now_playing = "No currently playing track"
    else:
        now_playing = f"{now_playing['track_name']} - {now_playing['artist_name']}"

    recently_played = get_user_recently_played(Spotipy)
    top_track = get_user_top_track(Spotipy)
    top_artist = get_user_top_artist(Spotipy)
    
    theme = colors[colorscheme]
    if not random_color:
        logo_color = theme['colorFour']
    else:
        logo_color = random.choice(list(theme.values()))

    current_user, now_playing, recently_played, top_track, top_artist = format_info(theme, current_user, now_playing, recently_played, top_track, top_artist)

    new_art = f"      [{logo_color}]______[/{logo_color}]" \
              f"\n   [{logo_color}];;        ;;[/{logo_color}]" \
              f"\n [{logo_color}];;            ;;[/{logo_color}]      {current_user}" \
              f"\n[{logo_color}];;   _..**.._   ;;[/{logo_color}]     {now_playing}" \
              f"\n[{logo_color}];;   _..**.._   ;;[/{logo_color}]     {recently_played}" \
              f"\n[{logo_color}];;   _..**.._   ;;[/{logo_color}]     {top_track}" \
              f"\n [{logo_color}];;            ;;[/{logo_color}]      {top_artist}" \
              f"\n   [{logo_color}];;        ;;[/{logo_color}]" \
              f"\n      [{logo_color}]------[/{logo_color}]" \

    print(new_art)

if __name__ == "__main__":
    main()
