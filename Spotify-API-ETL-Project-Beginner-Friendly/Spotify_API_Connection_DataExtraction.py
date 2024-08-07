#  Import neccesory Libraries
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

# create .env file in same directory
# Load .env file
load_dotenv()

# fetching your credentials from .env file 
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Function to get access token
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        # in above line give space after Basic #Imp
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

# Function to get authorization header
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}
    # in above line give space after Bearer #Imp


# Function to search for an artist by name
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print(f"No artist with name '{artist_name}' exists...")
        return None
    return json_result[0]

# Function to get top songs by artist ID
def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

# Function to save data to a JSON file
def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    token = get_token()

    # List of artist names (MODIFICATION: Added a list of artists)
    artists = ["ACDC", "Adele", "Drake", "Taylor Swift", "The Beatles", "Eminem", "Beyoncé", "Kanye West", "Rihanna", "Ed Sheeran","Sabrina Carpenter","Ariana Grande" ,"Justin Bieber" ,"Billie Eilish" ,"Imagine Dragons" ,"Salena Gomez" ,"Bebe Rexhda"]

    # Create a new directory for the JSON files (MODIFICATION: Create a new directory)
    output_dir = "artist_songs"
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through the list of artists (MODIFICATION: Loop through each artist)
    for artist in artists:
        result = search_for_artist(token, artist)
        if result:
            artist_id = result["id"]
            songs = get_songs_by_artist(token, artist_id)
            # MODIFICATION: Save each artist's top 10 songs to a JSON file
            filename = os.path.join(output_dir, f"{artist}_top_10_songs.json")
            save_to_json(songs, filename)
            print(f"Saved top 10 songs of {artist} to {filename}")

if __name__ == "__main__":
    main()
