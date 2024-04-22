from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


INITIAL_URL = "https://www.billboard.com/charts/hot-100"
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = "http://example.com"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path=".cache",
        username=os.environ.get("USERNAME"),
    )
)


user_id = sp.current_user()['id']

user_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
url = f"{INITIAL_URL}/{user_date}"

response = requests.get(url, verify=False)
music_web_page = response.text

soup = BeautifulSoup(music_web_page, "html.parser")
music_tags = soup.select("li ul li h3")
# print(music_tags.text.strip())
music_texts = [tag.getText().strip() for tag in music_tags]

song_uris = []
year = user_date.split("-")[0]

for song in music_texts:
    result = sp.search(f"track:{song} year:{year}", type="track")
    try:
        uri = result['tracks']['items'][0]['uri']
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped")

playlist_id = sp.user_playlist_create(user=user_id, name=f"{user_date} Billboard 100", public=False)

result = sp.playlist_add_items(playlist_id=playlist_id['id'], items=song_uris)

