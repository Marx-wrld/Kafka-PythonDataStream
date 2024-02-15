import json
import logging
import sys
import requests
from config import config

def fetch_playlist_items_page(google_api_key, youtube_playlist_id, page_token=None):
    response = requests.get("https://www.googleapis.com/youtube/v3/playlistItems", params={
        "key": google_api_key,
        "playlistId": youtube_playlist_id,
        "part": "contentDetails",
    })
    payload = json.loads(response.text)
    
    logging.debug("Fetched %d items", len(payload["items"]))
    
    return payload

def main():
    logging.info("START") 
    
    google_api_key = config["google_api_key"]
    youtube_playlist_id = config["youtube_playlist_id"]
    
    fetch_playlist_items_page(google_api_key, youtube_playlist_id, page_token=None)
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())