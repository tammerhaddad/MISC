import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from gtts import gTTS
from tqdm import tqdm
from pydub import AudioSegment
import time
from collections import deque
from datetime import datetime, timedelta

# Initialize a deque to keep track of request timestamps
request_times = deque()

def rate_limited_request():
  global request_times
  now = datetime.now()
  # Remove timestamps older than one hour
  while request_times and now - request_times[0] > timedelta(hours=1):
    request_times.popleft()
  if len(request_times) >= 100:
    # Calculate the time to wait until the next request can be made
    wait_time = (request_times[0] + timedelta(hours=1) - now).total_seconds()
    print(f"Rate limit reached. Waiting for {wait_time} seconds.")
    time.sleep(wait_time)
  request_times.append(now)

def extract_text_from_epub(file_path):
  book = epub.read_epub(file_path)
  text = []
  items = list(book.get_items())
  for item in tqdm(items, desc="Extracting text", unit="item"):
    if item.get_type() == ebooklib.ITEM_DOCUMENT:
      soup = BeautifulSoup(item.get_body_content(), 'html.parser')
      text.append(soup.get_text())
  return ' '.join(text)

def split_text(text, max_length=5000):
  words = text.split()
  chunks = []
  current_chunk = []
  current_length = 0
  for word in words:
    if current_length + len(word) + 1 > max_length:
      chunks.append(' '.join(current_chunk))
      current_chunk = []
      current_length = 0
    current_chunk.append(word)
    current_length += len(word) + 1
  if current_chunk:
    chunks.append(' '.join(current_chunk))
  return chunks

def text_to_speech(text, output_file):
  rate_limited_request()
  tts = gTTS(text, lang='en')
  tts.save(output_file)

def merge_audio_files(audio_files, output_file):
  combined = AudioSegment.empty()
  for file in audio_files:
    combined += AudioSegment.from_mp3(file)
  combined.export(output_file, format="mp3")

def epub_to_audiobook(epub_file, output_audio_file):
  text = extract_text_from_epub(epub_file)
  chunks = split_text(text)
  audio_files = []
  for i, chunk in enumerate(tqdm(chunks, desc="Processing chunks", unit="chunk")):
    chunk_file = f"epubToMp3Chunks/chunk_{i}.mp3"
    try:
      with tqdm(total=1, desc=f"Converting chunk {i} to speech", unit="request") as pbar:
        text_to_speech(chunk, chunk_file)
        pbar.update(1)
      audio_files.append(chunk_file)
    except Exception as e:
      print(f"Error: {e}. Failed to process chunk {i}.")
      return
    print("Chunk", i, "done")
  merge_audio_files(audio_files, output_audio_file)

# Example usage
epub_file = r"C:\Users\tamme\OneDrive\Desktop\Life Reset Series (Shemer Kuznits).epub"
output_audio_file = r"C:\Users\tamme\OneDrive\Desktop\Life Reset Series (Shemer Kuznits).mp3"
epub_to_audiobook(epub_file, output_audio_file)