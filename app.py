# Import necessary modules
from PyTubeCrawler import Channel
import csv

# Set API key and channel URL
API_KEY = "YOUR_API_KEY" # Set the API Key
CHANNEL_URL = "https://www.youtube.com/@SampleUser" # Set the channel url

# Display a message to indicate that the data acquisition process has started
print("The data acquisition process has been initiated.")

# Create a Channel object with the specified channel URL and API key
channel = Channel(CHANNEL_URL, API_KEY)

# Call the get_video_details method of the Channel object to retrieve details of all videos in the channel
videos = channel.get_video_details()

# Write the video details to a CSV file with the channel URL as the filename
with open(f"{channel.channel_url}.csv", mode="w", encoding="utf-8", newline="") as file:
    # Create a CSV writer object and write the header row containing the keys of the dictionary
    writer = csv.writer(file)
    writer.writerow(list(videos[0].keys()))

    # Iterate over the list of video dictionaries and write each dictionary as a row in the CSV file
    for video in videos:
        line = []
        for key in video.keys():
            line.append(video[key])
        writer.writerow(line)

# Display a message indicating the number of videos that were written to the CSV file
print(f"The data of {len(videos)} videos were written to the {channel.channel_url}.csv file.")
