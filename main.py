
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, Image
import pandas as pd
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# create a df from the StreamingHistory.json files
folder_loc = r"C:\Users\saket\Downloads\Compressed\spotify data\MyData"
files_loc = []
dfs = []
files = os.listdir(folder_loc)
for file in files:  
    if "endsong_" in file:
        files_loc.append(folder_loc+'\\'+file)
for i in range(len(files_loc)):
    dfs.append(pd.read_json(files_loc[i]))
df = pd.concat(dfs)
# df = pd.read_json(files_loc[0])


# sort by date
df = df.sort_values("ts")

# add a column for year
df['year'] = df.ts.apply(lambda row: row.split('-')[0])

# add a column for times listened to a track
track_count = df.spotify_track_uri.value_counts()
df['times_listened'] = df.spotify_track_uri.apply(lambda track: track_count[track] if track else None)

# dataframe that contains unique spotify_track_uri all the dublicates are removed
top_listened_by_year = df.drop_duplicates(subset='spotify_track_uri')

# import cred
client_ID= clientID
client_SECRET= clientSecret   
redirect_url='http://127.0.0.1:9090'
scope = "playlist-modify-public"
username = 'rt47etgc6xpwhhhb8575rth83'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_ID, client_secret= client_SECRET, redirect_uri=redirect_url, scope=scope))


list_of_songs     = []
list_of_songs_uri = []

# splits a list into lists of 100
def split_with_no(list, No):
    lists = []
    no = 0
    listy = []
    for i in list:
        if no < 100:
            no += 1
            listy.append(i)
        else:
            lists.append(listy) 
            listy = []
            no = 0
    lists.append(listy)
    # print('len - ',len(lists))
    return lists


# gets the song uri
def song(name, artist):
    result = sp.search(q=name+" "+artist)
    try:
        return result['tracks']['items'][0]['uri']
    except:
        'some kind of error'

# adds songs to a playlist
def add_to_playlist(playlist_id, list_of_tracks):
    splity_split = split_with_no(list_of_tracks, 100)
    for hundred_lis in splity_split:
        sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=hundred_lis)

# creates a spotify playlist according to the name
def create_playlist(name):
    sp.user_playlist_create(user=username, name=name, public=True)

# gets the playlist id
def get_playlist_id(name):
    playlists = sp.user_playlists(user=username)
    for playlist in playlists['items']:
        if playlist['name'] == name:
            return playlist['id']


# gets the top listened songs by year and returns a dataframe with the song name, artist, year, times listened and the timestamp of the last time it was listened
def make_playlist_for_x_times_listened(times): # warning: this will generate lots of playlists
    listened_x_times = top_listened_by_year[top_listened_by_year.times_listened >= times].sort_values('ts').iloc[::-1]
    #reverse the listening order
    listened_x_times = listened_x_times
    for year in listened_x_times.year.unique():
        # print(listened_x_times[listened_x_times.year == year].spotify_track_uri)
        # print(listened_x_times[listened_x_times.year == year].spotify_track_uri.values)
        # print(listened_x_times[listened_x_times.year == year].spotify_track_uri.values.tolist())
        create_playlist(name=f'{year} - {times} times listened')
        playlist_id = get_playlist_id(name=f'{year} - {times} times listened')
        add_to_playlist(playlist_id=playlist_id, list_of_tracks=listened_x_times[listened_x_times.year == year].spotify_track_uri.values.tolist())

# create playlists of most played songs each year with miniumum 5 times listened
def playlist_of_most_played_songs(times=5):
    # moves played songs sorted my most to least each year 
    for year in top_listened_by_year.year.unique():
        create_playlist(name=f'{year} - {times} Most listened songs')
        playlist_id = get_playlist_id(name=f'{year} - {times} Most listened songs')
        

    #     playlist_id = get_playlist_id(name=f'{year} - {times} times listened')
    #     add_to_playlist(playlist_id=playlist_id, list_of_tracks=top_listened_by_year[top_listened_by_year.year == year].spotify_track_uri.values.tolist())

# get song genre
# def get_song_genre(song_uri):
#     song_details = sp.track(track_id=song_uri)
#     artist_details = sp.artist(artist_id=song_details['artists'][0]['id'])
#     return artist_details['genres']

# get song details
def get_song_details(song_uri):
    song_details = sp.track(track_id=song_uri)
    return song_details

# get artist details
def get_artist_details(song_details):
    artist_details = sp.artist(artist_id=song_details['artists'][0]['id'])
    return artist_details

# get song genre
def get_song_genre(song_details):
    artist_details = sp.artist(artist_id=song_details['artists'][0]['id'])
    return artist_details['genres']

# display song art with matplotlib
def display_song_cover_art(song_art):
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    img=mpimg.imread(song_art)
    imgplot = plt.imshow(img)
    plt.show()

# display song art with IPython
def display_song_cover_art(song_art):
    from IPython.display import Image
    from IPython.core.display import HTML 
    return Image(url = song_art)

top_listened_by_year = df.groupby(['year','spotify_track_uri']).agg({'ts':'count'}).rename(columns={'ts':'times_listened'}).sort_values('times_listened', ascending=False).reset_index().groupby('year').head(10)

#get song cover art
def get_song_cover_art(song_uri):
    song_details = sp.track(track_id=song_uri)
    return song_details['album']['images'][0]['url']

# display song cover art
# def display_song_cover_art(get_song_cover_art):
#     from IPython.display import Image
#     from IPython.core.display import HTML 
#     return Image(url = get_song_cover_art)


song_uri = "spotify:track:5GgD8DZFgkmTuyShnYAub7"

# get song cover art
song_art = get_song_cover_art(song_uri)

display_song_cover_art(song_art)
