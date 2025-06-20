# 🤖 Instagram Auto Poster Bot

This Python script automates the process of posting **photos** and **videos (Reels)** to your Instagram account. It reads media from sequentially numbered folders (`1/`, `2/`, etc.), uploads them with the provided captions, and waits **10 hours** before posting the next batch.

---

## 🚀 Features

| Feature                     | Description                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| 📂 Folder-based Automation  | Media files are posted from folders `1/` to `10/` in order                 |
| 🖼️ Image + Video Support     | Supports `.jpg`, `.jpeg`, `.png`, `.mp4` files (Reels or image posts)      |
| 📝 Caption Support           | Uses `caption.txt` inside each folder for custom captions                  |
| ⏰ Auto Wait 10 Hours        | Automatically waits 10 hours before the next post                          |
| 🔐 Session Caching           | Saves login session (`instagram_session.json`) to skip login each time     |
| 🧾 Logging                   | All activity is logged in `instagram_poster.log` for review                |
| ✅ Skips Posted Folders      | Keeps track of posted folders in `posted_folders.txt`                      |
| 📛 Error Handling            | Handles failed logins or upload errors gracefully                          |

---

## 📁 Folder Structure

Create your project directory like this:
## 📁 Project Folder Structure

```
instagram-auto-poster/
│
├── instagram_poster.py         # Main script
├── posted_folders.txt          # Auto-created to track posted folders
├── instagram_session.json      # Auto-created after first login
│
├── 1/
│   ├── image1.jpg
│   ├── video1.mp4
│   └── caption.txt             # (optional) Caption for post
│
├── 2/
│   ├── another_image.png
│   └── caption.txt
│
├── 3/
│   └── clip.mp4
```





> You can create up to 10 folders (`1/` to `10/`). The script checks them in order.

---

## 📦 Installation

### 🔧 1. Install Dependencies

Make sure you have Python 3.7+ installed. Then install required packages:

```bash
pip install instagrapi
