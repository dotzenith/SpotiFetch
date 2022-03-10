from typing import Optional
import typer
import spotifetch.fetch as fetch

app = typer.Typer(add_completion=False)

@app.command()
def profile(
    term : str = typer.Option('short', "--term", "-t", help="The timeline for the top tracks/artists; short, mid, long"),         
    color: str = typer.Option('catppuccin', "--color", "-c", help="Supported color schemes: catppuccin, dracula, nord, gruvbox, onedark, tokyonight, rosepine, ayu, palenight, and gogh"), 
    random: bool = typer.Option(False, "--random", "-r", help="Use a random color for the spotify ascii art")        
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

    fetch.main(color, random, 'profile', term)

@app.command('top-tracks')
def top_tracks(
    term : str = typer.Option('short', "--term", "-t", help="The timeline for the top tracks/artists; short, mid, long"),         
    color: str = typer.Option('catppuccin', "--color", "-c", help="Supported color schemes: catppuccin, dracula, nord, gruvbox, onedark, tokyonight, rosepine, ayu, palenight, and gogh"), 
    random: bool = typer.Option(False, "--random", "-r", help="Use a random color for the spotify ascii art")        
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

    fetch.main(color, random, 'top_tracks', term)

@app.command('top-artists')
def top_artists(
    term : str = typer.Option('short', "--term", "-t", help="The timeline for the top tracks/artists; short, mid, long"),         
    color: str = typer.Option('catppuccin', "--color", "-c", help="Supported color schemes: catppuccin, dracula, nord, gruvbox, onedark, tokyonight, rosepine, ayu, palenight, and gogh"), 
    random: bool = typer.Option(False, "--random", "-r", help="Use a random color for the spotify ascii art")        
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

    fetch.main(color, random, 'top_artists', term)

def main():
    app()
