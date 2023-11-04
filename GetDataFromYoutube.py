import requests
import pandas as pd
import json
# init data
channel_id = input("Enter your channel ID: ")
api_key = input("Enter your api_key: ")
url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&key={api_key}&id={channel_id}'
channel_info = requests.get(url)
json_data = json.loads(channel_info.text)
json_data
# show channel datas
channel_subcribers = int(json_data['items'][0]['statistics']['subscriberCount'])
channel_videos = int(json_data['items'][0]['statistics']['videoCount'])
channel_views = int(json_data['items'][0]['statistics']['viewCount'])
print('Total subcribers = ', channel_subcribers)
print('Total videos = ', channel_videos)
print('Total views = ', channel_views)
# read datas from searching request
limit = 10
video_ids = []
for i in range(limit):
    url1 = f'https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_id}&part=snippet&type=video&maxResults=20'
    data = json.loads(requests.get(url1).text)
for item in data['items']:
    video_id = str(item['id']['videoId'])
    video_ids.append(video_id)
# create DataFrame to save data
data_df = pd.DataFrame(columns=['video_id', 'channel_id', 'published_date', 'video_title', 'likes', 'views', 'comment_count'])
for i, video_id in enumerate(video_ids):
    url = f'https://www.googleapis.com/youtube/v3/videos?key={api_key}&id={video_id}&part=statistics,snippet'
    data = json.loads(requests.get(url).text)
    channel_id = data['items'][0]['snippet']['channelId']
    published_date = data['items'][0]['snippet']['publishedAt']
    video_title = data['items'][0]['snippet']['title']
    likes = data['items'][0]['statistics']['likeCount']
    views = data['items'][0]['statistics']['viewCount']
    comment_count = data['items'][0]['statistics']['commentCount']
    row = [video_id,channel_id,published_date,video_title,likes,views,comment_count]
    data_df.loc[i] = row
# write file to csv
data_df.to_csv('crawl_youtube_channel.csv', index=False)
print("Now you can read list 20 or fewer videos of your channel in crawl_youtube_channel.csv file")