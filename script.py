from googleapiclient.discovery import build
import re
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("API")
VIDEO_ID = "M7AinOxULrU"
KEYWORD = "2:08"

def fetch_comment_threads(api_key, video_id, keyword):
    youtube = build('youtube', 'v3', developerKey=api_key)
    threads = []  # Stores threads (top comment + replies)
    
    try:
        # Fetch comment threads INCLUDING replies
        request = youtube.commentThreads().list(
            part="snippet,replies",  # Include replies
            videoId=video_id,
            textFormat="plainText",
            maxResults=100
        )
        
        while request:
            response = request.execute()
            for item in response['items']:
                top_comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                
                # Check if top comment matches keyword
                if re.search(keyword, top_comment, re.IGNORECASE):
                    thread = {
                        "top_comment": top_comment,
                        "replies": []
                    }
                    
                    # Extract replies if they exist
                    if 'replies' in item:
                        for reply in item['replies']['comments']:
                            reply_text = reply['snippet']['textDisplay']
                            thread['replies'].append(reply_text)
                    
                    threads.append(thread)
            
            # Paginate to next page of comment threads
            request = youtube.commentThreads().list_next(request, response)
        
        return threads
    
    except Exception as e:
        print(f"Error: {e}")
        return []

# Run the script
threads = fetch_comment_threads(API_KEY, VIDEO_ID, KEYWORD)

if threads:
    print(f"Threads where top comments contain '{KEYWORD}':\n")
    for idx, thread in enumerate(threads, 1):
        print(f"Thread {idx}:")
        print(f"🗨️  [TOP] {thread['top_comment']}")
        for reply_idx, reply in enumerate(thread['replies'], 1):
            print(f"    🔹 [Reply {reply_idx}] {reply}")
        print("-" * 50)
else:
    print("No matching threads found.")
