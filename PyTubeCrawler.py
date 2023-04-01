import requests
from googleapiclient.discovery import build 
from bs4 import BeautifulSoup

class Channel:
    
    def __init__(self, channel_url, api_key, api_service_name="youtube", api_version="v3"):
        """
        Initialize the Channel class with a channel URL, API key, API service name, and API version.
        """
        self.channel_url = channel_url.split("@")[-1]
        self.api_key = api_key
        self.api_service_name = api_service_name
        self.api_version = api_version
        self.youtube = build(api_service_name, api_version, developerKey=self.api_key)  # Build the YouTube Data API v3 service client

    def get_playlist_id(self):
        """
        Get the "uploads" playlist ID for the channel.
        """
        url = f"https://www.youtube.com/@{self.channel_url}"  # Construct the channel URL
        response = requests.get(url)  # Make a GET request to the channel URL
        html_content = response.text  # Get the HTML content of the response
        soup = BeautifulSoup(html_content, 'html.parser')  # Parse the HTML content using BeautifulSoup

        # Find the channel ID from the HTML content using BeautifulSoup
        channel_id = soup.find("link", attrs={"rel" : "canonical"})["href"].split("/")[-1]

        # Call the channels().list() method of the YouTube Data API v3 service client to get the channel details
        request = self.youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=channel_id
        )
        response = request.execute()

        # Get the "uploads" playlist ID from the channel details
        playlistId = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        self.playlistId = playlistId 
        return self.playlistId

    def get_video_ids(self):
        """
        Get a list of video IDs for all the videos in the "uploads" playlist.
        """
        playlistId = self.get_playlist_id()

        video_ids = []  # Initialize an empty list to store the video IDs

        # Call the playlistItems().list() method of the YouTube Data API v3 service client to get the first page of playlist items
        request = self.youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlistId,
            maxResults=50
        )
        response = request.execute()

        # Add the video IDs from the first page of playlist items to the video_ids list
        for item in response["items"]:
            video_ids.append(item["contentDetails"]["videoId"])

        # Keep getting more pages of playlist items and adding their video IDs to the video_ids list until there are no more pages
        next_page_token = response.get('nextPageToken')
        while next_page_token is not None:
            request = self.youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=self.playlistId,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response["items"]:
                video_ids.append(item["contentDetails"]["videoId"])

            next_page_token = response.get('nextPageToken')

        self.video_ids = video_ids
        return self.video_ids

    def get_video_details(self):
        """
        Get a list of dictionaries containing the details of all the videos in the "uploads" playlist.
        """
        video_ids = self.get_video_ids()

        all_video_info = []  # Initialize an empty list to store the details of all the videos

        # Get the details of up to 50 videos at a time using the videos().list() method of the YouTube Data API v3 service client
        for i in range(0, len(video_ids), 50):
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=",".join(video_ids[i:i+50])
            )
            response = request.execute()

            # Extract the details we want to keep from each video and store them in a dictionary
            for video in response["items"]:
                stats_to_keep = {"snippet": ["channelTitle", "title", "publishedAt"],
                                 "statistics": ["viewCount", "likeCount", "favoriteCount", "commentCount"],
                                 "contentDetails": ["duration", "definition"]
                                }
                video_info = {}
                video_info["video_id"] = video["id"]

                for key in stats_to_keep.keys():
                    for value in stats_to_keep[key]:
                        try:
                            video_info[value] = video[key][value]
                        except:
                            video_info[value] = None

                all_video_info.append(video_info)

        return all_video_info  # Return the list of dictionaries containing the details of all the videos
