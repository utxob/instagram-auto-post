import os
import time

from datetime import datetime, timedelta
from pathlib import Path
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ClientError

# Logging configuration
def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{level}] {message}"
    print(log_message)
    with open("instagram_poster.log", "a", encoding="utf-8") as log_file:
        log_file.write(log_message + "\n")

def setup_client():
    cl = Client()
    session_file = "instagram_session.json"
    
    log("Attempting to initialize Instagram client")
    
    # Try to load saved session
    if os.path.exists(session_file):
        try:
            log(f"Found existing session file: {session_file}")
            cl.load_settings(session_file)
            log("Session loaded successfully. Testing session...")
            cl.get_timeline_feed()  # Test session
            log("Session test successful. Using saved session.")
            return cl
        except (LoginRequired, ClientError) as e:
            log(f"Saved session invalid: {str(e)}", "WARNING")
            log("Proceeding with manual login")
    
    # Manual login
    log("No valid session found. Starting manual login process")
    print("\n" + "="*50)
    print("Instagram Login Required")
    print("="*50)
    username = input("Please enter your Instagram username: ")
    password = input("Please enter your Instagram password: ")
    print("="*50 + "\n")
    
    try:
        log(f"Attempting login for user: {username}")
        cl.login(username, password)
        cl.dump_settings(session_file)
        log("Login successful. Session saved for future use.")
        return cl
    except Exception as e:
        log(f"Login failed: {str(e)}", "ERROR")
        return None

def get_next_folder(base_path="."):
    log("Checking for next folder to post...")
    posted_folders = set()
    if os.path.exists("posted_folders.txt"):
        with open("posted_folders.txt", "r") as f:
            posted_folders = set(f.read().splitlines())
        log(f"Found {len(posted_folders)} previously posted folders")
    
    for i in range(1, 11):
        folder = str(i)
        folder_path = os.path.join(base_path, folder)
        if folder not in posted_folders:
            if os.path.exists(folder_path):
                log(f"Found unposted folder: {folder}")
                return folder
            else:
                log(f"Folder {folder} not found in directory", "WARNING")
    
    log("No more unposted folders found")
    return None

def mark_folder_as_posted(folder):
    with open("posted_folders.txt", "a") as f:
        f.write(f"{folder}\n")
    log(f"Marked folder {folder} as posted")

def get_media_files(folder_path):
    log(f"Scanning folder {folder_path} for media files")
    media_files = []
    
    # Find all media files in the folder
    for file in os.listdir(folder_path):
        file_lower = file.lower()
        if file_lower.endswith(('.jpg', '.jpeg', '.png', '.mp4')):
            media_files.append(os.path.join(folder_path, file))
    
    # Sort files to maintain consistent order
    media_files.sort()
    
    if not media_files:
        log("No media files found in folder", "WARNING")
    
    return media_files

def get_caption(folder_path):
    caption = ""
    caption_path = os.path.join(folder_path, "caption.txt")
    if os.path.exists(caption_path):
        with open(caption_path, "r", encoding="utf-8") as f:
            caption = f.read().strip()
        log(f"Found caption with {len(caption)} characters")
    else:
        log("No caption.txt file found in folder", "WARNING")
    return caption

def post_media(cl, media_path, caption):
    try:
        is_video = media_path.lower().endswith('.mp4')
        media_type = "video (Reel)" if is_video else "image (Post)"
        log(f"Detected media type: {media_type}")
        
        log(f"Starting upload process for {media_path}...")
        if is_video:
            log("Uploading video as Reel...")
            media = cl.clip_upload(media_path, caption=caption)
        else:
            log("Uploading image as post...")
            media = cl.photo_upload(media_path, caption=caption)
        
        log(f"Upload successful! Media ID: {media.id}")
        log(f"Post details: Type={media_type}, Caption length={len(caption)}")
        return True
    except Exception as e:
        log(f"Error during upload: {str(e)}", "ERROR")
        return False

def wait_for_next_post():
    next_post_time = datetime.now() + timedelta(hours=10)
    next_post_str = next_post_time.strftime("%Y-%m-%d %H:%M:%S")
    log(f"Waiting until {next_post_str} for next post check...")
    
    print("\n" + "="*50)
    print(f"Next Post Check at: {next_post_str}")
    print("="*50 + "\n")
    
    # Countdown timer
    for remaining in range(10*60*60, 0, -1):
        hours, remainder = divmod(remaining, 3600)
        minutes, seconds = divmod(remainder, 60)
        countdown = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        print(f"Time until next post check: {countdown}", end="\r")
        time.sleep(1)
    print("\n")

def process_folder(cl, folder):
    folder_path = os.path.join(".", folder)
    log(f"Processing folder: {folder_path}")
    
    # Get all media files and caption for the folder
    media_files = get_media_files(folder_path)
    caption = get_caption(folder_path)
    
    if not media_files:
        log(f"No media files found in {folder}. Marking as posted.", "WARNING")
        mark_folder_as_posted(folder)
        return False
    
    # Post all media files in the folder
    success = True
    for media_path in media_files:
        if not post_media(cl, media_path, caption):
            success = False
            break
    
    if success:
        mark_folder_as_posted(folder)
        return True
    return False

def main():
    print("\n" + "="*50)
    print("Instagram Auto-Poster Script")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50 + "\n")
    
    log("Script started")
    
    cl = setup_client()
    if not cl:
        log("Failed to initialize Instagram client. Exiting.", "ERROR")
        return
    
    log("Client initialized successfully")
    
    while True:
        folder = get_next_folder()
        if not folder:
            log("No more unposted folders found. Script completed successfully.")
            break
        
        success = process_folder(cl, folder)
        
        if not success:
            log(f"Failed to post folder {folder}. Marking as posted to skip in future.", "WARNING")
            mark_folder_as_posted(folder)
        
        # Only wait if there might be more folders to process
        if get_next_folder():
            log("Waiting 10 hours before processing next folder...")
            wait_for_next_post()
        else:
            log("No more folders to process. Script completed.")
            break

if __name__ == "__main__":
    main()