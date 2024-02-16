import json
import logging
from pprint import pformat
import sys
import requests
from config import config
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.schema_registry_client import SchemaRegistryClient
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.avro import AvroSerializer
from confluent_kafka import SerializingProducer

def fetch_playlist_items_page(google_api_key, youtube_playlist_id, page_token=None): # function to fetch playlist items from youtube playlists page 
    response = requests.get("https://www.googleapis.com/youtube/v3/playlistItems", params={ # query parameters for playlist id, google api key, and page token
        "key": google_api_key,
        "playlistId": youtube_playlist_id,
        "part": "contentDetails",
        "page_token": page_token,
    })
    payload = response.json()  # Parse JSON response
    
    logging.debug("Fetched %d items", len(payload['items'])) # Log the number of fetched items and return the payload
    
    return payload

def fetch_videos_page(google_api_key, video_id, page_token=None): # function to fetch videos from youtube videos page based on the video id
    response = requests.get("https://www.googleapis.com/youtube/v3/videos", params={ # query parameters for video id, google api key, and page token
        "key": google_api_key,
        "id": video_id,
        "part": "snippet,statistics",
        "page_token": page_token,
    })
    payload = json.loads(response.text) #Parse JSON response
    
    logging.debug("Fetched %d items", payload) # Log the number of fetched items and return the payload
    
    return payload 

def fetch_playlist_items(google_api_key, youtube_playlist_id, page_token=None): # function to fetch playlist items from youtube playlists
    payload = fetch_playlist_items_page(google_api_key, youtube_playlist_id, page_token) # fetch playlist items from youtube playlists page
    
    yield from payload["items"] # yield the items from the payload
    
    next_page_token = payload.get('nextPageToken') # get the next page token
    
    if next_page_token is not None: # if the next page token is not none, yield the next page token
        yield from fetch_playlist_items_page(google_api_key, youtube_playlist_id, next_page_token)
    

def fetch_videos(google_api_key, youtube_playlist_id, page_token=None): # generator function that yields video details based on the video ID
    payload = fetch_videos_page(google_api_key, youtube_playlist_id, page_token) # generator function that yields video details based on the video ID
    
    yield from payload['items'] # yield the items from the payload
    
    next_page_token = payload.get('nextPageToken') # get the next page token
    
    if next_page_token is not None: # if the next page token is not none, yield the next page token
        yield from fetch_playlist_items_page(google_api_key, youtube_playlist_id, next_page_token)


def summarize_video(video): # function to summarize the video details
    return {
        "video_id": video["id"],
        "title": video["snippet"]["title"],
        "description": video["snippet"]["description"],
        "views": int(video["statistics"].get("viewCount", 0)),
        "likes": int(video["statistics"].get("likeCount", 0)),
        "comments": int(video["statistics"].get("commentCount", 0)),
    }


def on_delivery(err, record):
    pass 

def main(): # main function
    logging.info("START") # start logging process
    
    schema_registry_client = SchemaRegistryClient(config["schema_registry"]) # create a schema registry client
    youtube_videos_value_schema = schema_registry_client.get_latest_version("youtube_videos_value") # get the latest version of the youtube videos value schema
    
    kafka_config = config['kafka'] | { # kafka configuration
        "value.serializer": AvroSerializer( 
            schema_registry_client, youtube_videos_value_schema.schema.schema_str
            ),
        "key.serializer": StringSerializer(),
    }
    producer = SerializingProducer(kafka_config) # create a serializing producer
    
    google_api_key = config["google_api_key"] # create a google api key to connect to the youtube api
    youtube_playlist_id = config["youtube_playlist_id"] # create a youtube playlist id to fetch the playlist items
    
    for video_items in fetch_playlist_items(google_api_key, youtube_playlist_id): # for loop to fetch the video items from the playlist
        print(type(video_items)) # print the video items data type
        video_id = video_items['contentDetails']['videoId'] # get the video id from the video items
        for video in fetch_videos(google_api_key, video_id): # for loop to fetch the videos based on the video id
            logging.info("Video id: %s", pformat(summarize_video(video)))
            
            producer.produce( # create a producer to produce the video details for the video based on the video id
                topic='youtube_videos',
                key=video_id,
                value={
                        "TITLE": video["snippet"]["title"],
                        "DESCRIPTION": video["snippet"]["description"],
                        "VIEWS": int(video["statistics"].get("viewCount", 0)),
                        "LIKES": int(video["statistics"].get("likeCount", 0)),
                        "COMMENTS": int(video["statistics"].get("commentCount", 0)),
                    },  
                on_delivery=on_delivery, # on_delivery is called when the message is successfully delivered or if it fails
            )
            
            producer.flush() # flush the producer to ensure that all messages are delivered
    
if __name__ == "__main__": # if the main function is called, run the main function
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())