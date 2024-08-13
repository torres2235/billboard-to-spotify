import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

SPOTIPY_CLIENT_ID = "e8a035016a614ae5a593d40d45351590"
SPOTIPY_CLIENT_SECRET = "06a7f4e36f5048338731968fdffbea07"
SPOTIPY_REDIRECT_URI = "https://example.com/"
ACCESS_TOKEN = "BQDcgCs0WMx5-HFz6FVti4R6ZG3ujKsFm6Ev0nFC3thp3HG6yjRfhzs5vHyg5OfY6fqqW2xhU-PLcqGSDDX-sCYLdmm1rj7Y7ca5hhZ3TDUNlbKRTO5xJE98RIuV5GebogZCYZpyKHNEGCKI0HheC7BWLVWLRqzVMhtTr3V3goEFt8W6vbcHnJhVeUMxFNy2LypHbZMn1SpH_aaZqpE"

time_frame = input("Which year would you like to travel to? Input in YYYY-MM-DD: ")

url = f"https://www.billboard.com/charts/hot-100/2000-08-12"

response = requests.get(url=url)
billboard_html = BeautifulSoup(response.text, "html.parser")

song_list = [song.getText().strip() for song in billboard_html.select("h3#title-of-a-story.c-title.a-no-trucate.a-font-primary-bold-s")]
print(song_list)


spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="playlist-modify-private",
    )
)
#spotify.get_access_token()

user_id = spotify.current_user()["id"]

song_uris = []
year = time_frame.split("-")[0]
for song in song_list:
    result = spotify.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlists = spotify.user_playlists(user_id)["items"]

playlist_id = ""
for item in playlists:
    if item["name"] == f"{time_frame} Billboard 100":
        playlist_id = item["id"]

# pprint(playlists)
# print(playlist_id)

if playlist_id != "":
    spotify.playlist_replace_items(user_id, playlist_id, song_uris)
else:
    new_playlist = spotify.user_playlist_create(user=user_id, name=f"{time_frame} Billboard 100", description=f"Billboard Top 100 tracks from the date {time_frame}", public=False)
    spotify.playlist_add_items(playlist_id=new_playlist["id"], items=song_uris)
