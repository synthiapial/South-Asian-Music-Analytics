import requests
import base64
import pandas as pd
import time

# Step 0: Credentials
client_id = '11f256c42af14cb997db7411ab530517'
client_secret = 'e533218e970b489e81a71097afb25c1c'

# Step 1: Get access token
auth_str = f"{client_id}:{client_secret}"
auth_bytes = auth_str.encode("utf-8")
auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

auth_url = "https://accounts.spotify.com/api/token"
auth_headers = {
    "Authorization": f"Basic {auth_base64}"
}
auth_data = {
    "grant_type": "client_credentials"
}

response = requests.post(auth_url, headers=auth_headers, data=auth_data)
access_token = response.json()["access_token"]

# Step 2: Search for Bollywood tracks
search_url = "https://api.spotify.com/v1/search"
headers = {
    "Authorization": f"Bearer {access_token}"
}
params = {
    "q": "Arijit Singh",
    "type": "track",
    "limit": 20

}
response = requests.get(search_url, headers=headers, params=params)
tracks = response.json()["tracks"]["items"]

# Step 3: Extract track info
track_data = []

for track in tracks:
    track_info = {
        "track_id": track["id"],
        "track_name": track["name"],
        "artist": track["artists"][0]["name"],
        "popularity": track["popularity"],
        "release_date": track["album"]["release_date"]
    }

    # Step 4: Get audio features for this track
    feature_url = f"https://api.spotify.com/v1/audio-features/{track['id']}"
    feature_response = requests.get(feature_url, headers=headers)
    if feature_response.status_code == 200:
        feature = feature_response.json()
        for key in ["danceability", "energy", "valence", "tempo"]:
            track_info[key] = feature.get(key)
    else:
        print(f"Failed to get features for track ID {track['id']}")
        for key in ["danceability", "energy", "valence", "tempo"]:
            track_info[key] = None

    track_data.append(track_info)
    time.sleep(0.2)  # Be respectful of API limits

# Step 5: Save to CSV
df = pd.DataFrame(track_data)
df.to_csv("spotify_bollywood_tracks.csv", index=False)
print("Data saved to spotify_bollywood_tracks.csv")