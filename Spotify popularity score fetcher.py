import requests
import pandas as pd
import time

# Load the CSV file containing Spotify track IDs
dataframe = pd.read_csv('Spotify_Song_Attributes.csv')
song_IDs = dataframe['id'].dropna().astype(str).tolist()
print(song_IDs)
print(f"{len(song_IDs)} songs found")
print("Fetching popularity scores...")

# Spotify API endpoint for fetching multiple tracks
endpoint = 'https://api.spotify.com/v1/tracks'

# Replace these with your own Client ID and Client Secret from your Spotify Developer Dashboard
CLIENT_ID = ''
CLIENT_SECRET = ''

def get_access_token(client_id, client_secret):
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch access token: {response.text}")
    
    token_info = response.json()
    return token_info.get("access_token")

access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
print("Access Token:", access_token)
 


# Headers for the API request
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Function to fetch popularity scores in batches
def fetch_popularity_scores(track_ids):
    popularity_scores = []
    batch_size = 50  # Maximum number of tracks per request

    for i in range(0, len(track_ids), batch_size):
        batch_ids = track_ids[i:i + batch_size]
        params = {
            'ids': ','.join(batch_ids)
        }
        response = requests.get(endpoint, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            for track in data['tracks']:
                if track is not None:
                    popularity_scores.append({
                        'id': track['id'],
                        'name': track['name'],
                        'popularity': track['popularity']
                    })
                else:
                    popularity_scores.append({
                        'id': None,
                        'name': None,
                        'popularity': None
                    })
        else:
            print(f"Failed to fetch data for batch starting at index {i}. Status code: {response.status_code}")
            # Optional: Implement retry logic or error handling here
            time.sleep(1)  # Wait before the next request to avoid rate limiting

    return popularity_scores

# Function to test fetching popularity scores for the first 50 tracks
def test_fetch_first_50_tracks():
    test_ids = song_IDs[:50]
    test_data = fetch_popularity_scores(test_ids)
    for track in test_data:
        print(track['popularity'])
# Uncomment the following line to run the test function
# test_fetch_first_50_tracks()

# Fetch popularity scores for all tracks
popularity_data = fetch_popularity_scores(song_IDs)

# Convert the data to a DataFrame and save to CSV
popularity_df = pd.DataFrame(popularity_data)
popularity_df.to_csv('Spotify_Popularity_Scores.csv', index=False)

print("Popularity scores have been saved to 'Spotify_Popularity_Scores.csv'")