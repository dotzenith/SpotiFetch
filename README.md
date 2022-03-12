<h2 align="center"> ━━━━━━  ❖  ━━━━━━ </h2>

<!-- BADGES -->
<div align="center">
   <p></p>
   
   <img src="https://img.shields.io/github/stars/zenithds/SpotiFetch?color=F8BD96&labelColor=302D41&style=for-the-badge">   

   <img src="https://img.shields.io/github/forks/zenithds/SpotiFetch?color=DDB6F2&labelColor=302D41&style=for-the-badge">   

   <img src="https://img.shields.io/github/repo-size/zenithds/SpotiFetch?color=ABE9B3&labelColor=302D41&style=for-the-badge">
   
   <img src="https://badges.pufler.dev/visits/zenithds/SpotiFetch?style=for-the-badge&color=96CDFB&logoColor=white&labelColor=302D41"/>
   <br>
</div>

<p/>

---

### ❖ Information 

  SpotiFetch is a simple fetch tool to display info about your Spotify profile 

  <!-- <img src="assets/lovesay.gif" alt="lovesay gif"> -->

---

### ❖ Requirements

Register a free app on the Spotify developer dashboard [here](https://developer.spotify.com/dashboard/)

Set `http://127.0.0.1:9090` as the redirect URI

Put the following in your `.bashrc` or `.zshrc` or the equivalent for your shell
```sh
export SPOTIPY_CLIENT_ID='insert-your-spotify-client-id-here'
export SPOTIPY_CLIENT_SECRET='insert-your-spotify-client-secret-here'
export SPOTIPY_REDIRECT_URI='http://127.0.0.1:9090'
```

---

### ❖ Installation

> Install from pip
```sh
$ pip3 install spotifetch
```

> Install from source
- First, install [poetry](https://python-poetry.org/)
```sh
$ git clone https://github.com/ZenithDS/SpotiFetch.git
$ cd SpotiFetch
$ poetry build
$ pip3 install ./dist/SpotiFetch-0.2.0.tar.gz
```

### ❖ Usage 

If the instructions in the Requirements section are followed properly, SpotiFetch will ask you to log in 
and give permissions to fetch stats the first time it's used. Login is not required after the first use. 

```
Usage: spotifetch [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  profile      Fetch stats for the user profile
  top-artists  Fetch user's top artists
  top-tracks   Fetch user's top tracks
```


SpotiFetch can be used like any other fetch tool

```sh
$ spotifetch profile      # fetches profile stats
$ spotifetch top-artists  # fetches your top five artists
$ spotifetch top-tracks   # fetches your top five songs
```

The top artists and tracks depends on the time-frame. By default, SpotiFetch fetches your top artists in the short term, but
mid term, and long term are also available using the `--term`/`-t` option.

```sh
$ spotifetch top-artists -t short # fetches top artists in the short term
$ spotifetch top-artists -t mid   # fetches top artists in the mid term
$ spotifetch top-artists -t long  # fetches top artists in the long term
```

The `--term`/`-t` option is available for all three of the commands 


SpotiFetch can also be used with a variety of different color schemes.

> SpotiFetch uses [catppuccin](https://github.com/catppuccin) as it's default color scheme, but a different one can be specified using the `--color`/`-c` option. 

For example:
```sh
$ spotifetch profile         # uses catppuccin
$ spotifetch profile -c nord # uses nord 
```

The `--color`/`-c` option is available for all three of the commands as well

Supported color schemes as of now: 
- [catppuccin](https://github.com/catppuccin)
- [nord](https://github.com/arcticicestudio/nord)
- [dracula](https://github.com/dracula/dracula-theme)
- [gruvbox](https://github.com/morhetz/gruvbox)
- [onedark](https://github.com/joshdick/onedark.vim)
- [tokyonight](https://github.com/folke/tokyonight.nvim)
- [rose pine](https://rosepinetheme.com/)
- [ayu](https://github.com/ayu-theme)
- [palenight](https://github.com/drewtempelmeyer/palenight.vim)
- [gogh](https://github.com/Mayccoll/Gogh)


SpotiFetch also supports `--random`/`-r` option to print the spotify ascii art with a random color instead of the default green

```sh
$ spotifetch profile     # prints green spotify art
$ spotifetch profile -r  # prints spotify art with random color
```

The `--random`/`-r` option is also available for all three of the commands

---

### ❖ About SpotiFetch

SpotiFetch is the direct result of browsing too many unix subreddits and general interest in cli tools. The ascii art for spotify is a WIP and contributions to the logo are welcomed and encouraged! 

---

### ❖ What's New? 
0.2.0 - Added dynamically generated themes

---

<div align="center">

   <img src="https://img.shields.io/static/v1.svg?label=License&message=MIT&color=F5E0DC&labelColor=302D41&style=for-the-badge">

</div>

