import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

YOUTUBE_TRENDING_URL = 'https://www.youtube.com/feed/trending'

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver

def get_videos(driver, classname):
  print("Fetching videos...")
  driver.get(YOUTUBE_TRENDING_URL)
  print("Page title:", driver.title)
  videos = driver.find_elements(By.TAG_NAME, classname)
  return videos

def parse_video(video):
  title_tag = video.find_element(By.ID, 'video-title')
  title = title_tag.text
  video_url = title_tag.get_attribute('href')
  thumbnail_url = video.find_element(By.TAG_NAME, 'img').get_attribute('src')
  channel_name = video.find_element(By.CLASS_NAME, 'ytd-channel-name').text
  description = video.find_element(By.ID, 'description-text').text
  duration = video.find_element(By.TAG_NAME, 'ytd-thumbnail-overlay-time-status-renderer').text
  span_tags = video.find_element(By.TAG_NAME,"ytd-video-meta-block").find_elements(By.TAG_NAME, 'span')
  views = span_tags[len(span_tags)-2].text
  uploaded = span_tags[len(span_tags)-1].text

  return {
    'title': title,
    'video_url': video_url,
    'thumbnail_url': thumbnail_url,
    'channel_name': channel_name,
    'description': description,
    'duration': duration,
    'views': views,
    'uploaded': uploaded
  }

if __name__ == '__main__':
  print("Creating driver...")
  driver = get_driver()
  print("Driver Created.")
  
  classname = 'ytd-video-renderer'
  videos = get_videos(driver, classname)
  print(f'Found {len(videos)} videos.')

  print('Parsing Top 10 Videos')
  # Title, video URL, channel, duration, views, uploaded, thumbnail URL, description
  videos_data = [parse_video(video) for video in videos[:10]]
  print('Saving the data to a CSV')

  videos_df = pd.DataFrame(videos_data)
  print(videos_df)
  videos_df.to_csv('trending.csv', index=None)