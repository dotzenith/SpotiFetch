import typer
import spotifetch.fetch as fetch

app = typer.Typer(add_completion=False)

@app.command()
def profile(
    term : str = typer.Option('short', "--term", "-t", help="The timeline for the top tracks/artists; short, mid, long"),         
    color: str = typer.Option('catppuccin', "--color", "-c", help="Supported color schemes: catppuccin, dracula, nord, gruvbox, onedark, tokyonight, rosepine, ayu, palenight, and gogh"), 
    random: bool = typer.Option(False, "--no-random", "-n", help="Do not use a random color for the spotify ascii art"),
    art: bool = typer.Option(False, help="Use the cover art of the recently played song as the colorscheme"),
    all_artists: bool = typer.Option(False, "--all-artists", "-a", help="Display all artists for the tracks"),
    pywal: bool = typer.Option(False, help="Use pywal colors")
):
    """
    Fetch stats for the user profile
    """

    if term == 'mid':
        term = 'medium_term'
    elif term == 'long':
        term = 'long_term'
    else:
        term = 'short_term'

    fetch.main(color, not(random), 'profile', term, art, all_artists, pywal)

@app.command('top-tracks')
def top_tracks(
    term : str = typer.Option('short', "--term", "-t", help="The timeline for the top tracks/artists; short, mid, long"),         
    color: str = typer.Option('catppuccin', "--color", "-c", help="Supported color schemes: catppuccin, dracula, nord, gruvbox, onedark, tokyonight, rosepine, ayu, palenight, and gogh"), 
    random: bool = typer.Option(False, "--no-random", "-n", help="Do not use a random color for the spotify ascii art"),
    art: bool = typer.Option(False, help="Use the cover art of the top played song as the colorscheme"),
    all_artists: bool = typer.Option(False, "--all-artists", "-a", help="Display all artists for the tracks"),
    pywal: bool = typer.Option(False, help="Use pywal colors")
):
    """
    Fetch user's top tracks 
    """

    term = term.lower()
    if term == 'mid':
        term = 'medium_term'
    elif term == 'long':
        term = 'long_term'
    else:
        term = 'short_term'

    fetch.main(color, not(random), 'top_tracks', term, art, all_artists, pywal)

@app.command('top-artists')
def top_artists(
    term : str = typer.Option('short', "--term", "-t", help="The timeline for the top tracks/artists; short, mid, long"),         
    color: str = typer.Option('catppuccin', "--color", "-c", help="Supported color schemes: catppuccin, dracula, nord, gruvbox, onedark, tokyonight, rosepine, ayu, palenight, and gogh"), 
    random: bool = typer.Option(False, "--no-random", "-n", help="Do not use a random color for the spotify ascii art"),
    art: bool = typer.Option(False, help="Use the profile art of the top played artist as the colorscheme"),
    pywal: bool = typer.Option(False, help="Use pywal colors")
):
    """
    Fetch user's top artists
    """

    term = term.lower()
    if term == 'mid':
        term = 'medium_term'
    elif term == 'long':
        term = 'long_term'
    else:
        term = 'short_term'

    fetch.main(color, not(random), 'top_artists', term, art, False, pywal)

def main():
    app()
