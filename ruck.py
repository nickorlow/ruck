import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
from spotipy.oauth2 import SpotifyOAuth
from dotenv import dotenv_values


config = dotenv_values(".env")  


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
  client_id=config['CLIENT_ID'],
  client_secret=config['CLIENT_SECRET'],
  redirect_uri="https://localhost/spotify",
  scope="playlist-read-collaborative,playlist-modify-public,playlist-modify-private"))


playlist_id = config['PLAYLIST_ID']

allowlisted_users = config['ALLOW_LIST'].split(',')

while 1==1:
  while 1==1:
    removal_ids = []
    results =  sp.playlist(playlist_id, fields=None, market=None, additional_types=('track', ))['tracks']
    tracks = results['items']
    while results['next']:
      results = sp.next(results)
      tracks.extend(results['items'])

    print("Checking Again -----")

    for i,x in enumerate(tracks):
      track = tracks[i]
      user_id = track['added_by']['id']
      if user_id not in allowlisted_users:
        print("Removing Track: "+track['track']['name']+"\nBy:"+ user_id)
        removal_ids.append({"uri":track['track']['uri'][14:], "positions":[i]})

    if(len(removal_ids) > 100):
      removal_len = 100
    else:
      removal_len = len(removal_ids)

    sp.playlist_remove_specific_occurrences_of_items(playlist_id, removal_ids[0:removal_len], snapshot_id=None)

    if(len(removal_ids) <= 100):
      break

  print("Sleeping 5...")
  time.sleep(5)
  
