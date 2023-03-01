import pandas as pd
# import data visualization libraries
import matplotlib.pyplot as plt
import seaborn as sns
# import plotly libraries
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

data_folder = r'C:\Users\saket\Downloads\Compressed\spotify data\MyData'

# import data
df = pd.read_json(r'C:\Users\saket\Downloads\Compressed\spotify data\MyData\song_details.json')


album = df.album
# convert the album column to a dataframe
album = pd.DataFrame(df['album'].tolist())['images']
image = pd.DataFrame(album.tolist())[0]
image = pd.DataFrame(image)


# remove unnecessary columns
df = df.drop(['album', 'artists', 'available_markets', 'disc_number', 'duration_ms', 'explicit', 'external_ids', 'external_urls', 'href', 'id', 'is_local', 'preview_url', 'track_number', 'type', 'uri'], axis=1)
df
image[0][1]



he = '''{'height': 640,
 'url': 'https://i.scdn.co/image/ab67616d0000b2735fa6dc9fc261344044c301a9',
 'width': 640}'''

# convert he to dataframe
import pandas as pd
import numpy as np

df = pd.DataFrame(he, columns=['height', 'url', 'width'])