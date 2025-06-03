from typing import List, Dict
import os
from dotenv import load_dotenv


load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

OWNER_ID = int(os.getenv("OWNER_ID", 7500269454))

# Database Configuration
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Channel Configuration 
DB_CHANNEL_ID = int(os.getenv("DB_CHANNEL_ID"))
FORCE_SUB_CHANNEL = int(os.getenv("FORCE_SUB_CHANNEL")) # First force sub channel
FORCE_SUB_CHANNEL_2 = int(os.getenv("FORCE_SUB_CHANNEL_2", 0)) # Second force sub channel, defaults to 0 if not set
FORCE_SUB_CHANNEL_3 = int(os.getenv("FORCE_SUB_CHANNEL_3", 0))
FORCE_SUB_CHANNEL_4 = int(os.getenv("FORCE_SUB_CHANNEL_4", 0))

# Add a second channel link
CHANNEL_LINK = os.getenv("CHANNEL_LINK") # First channel link
CHANNEL_LINK_2 = os.getenv("CHANNEL_LINK_2", "") # Second channel link
CHANNEL_LINK_3 = os.getenv("CHANNEL_LINK_3", "") 
CHANNEL_LINK_4 = os.getenv("CHANNEL_LINK_4", "") 

#start photo 
START_PHOTO = os.getenv("START_PHOTO", "") #start photo for bot

# Bot Information
BOT_USERNAME = os.getenv("BOT_USERNAME")
BOT_NAME = os.getenv("BOT_NAME")
BOT_VERSION = "1.6"

# Privacy Mode Configuration and codexbotz delete time
PRIVACY_MODE = os.getenv("PRIVACY_MODE", "off").lower() == "on"
AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", 30))

# Your InShort URL Api Key Here
LS_API_KEY = os.getenv("LS_API_KEY")
if not LS_API_KEY:
    print("⚠️ Arey InshortURL.com se API leke dal .env mein!")

# Links
CHANNEL_LINK = os.getenv("CHANNEL_LINK")
DEVELOPER_LINK = os.getenv("DEVELOPER_LINK")
SUPPORT_LINK = os.getenv("SUPPORT_LINK")

# For Koyeb/render 
WEB_SERVER = bool(os.getenv("WEB_SERVER", True)) # make it True if deploying on koyeb/render else False
PING_URL = os.getenv("PING_URL") # add your koyeb/render's public url
PING_TIME = int(os.getenv("PING_TIME")) # Add time_out in seconds

# Admin IDs - Convert space-separated string to list of integers
ADMIN_IDS: List[int] = [
    int(admin_id.strip())
    for admin_id in os.getenv("ADMIN_IDS", "").split()
    if admin_id.strip().isdigit()
]

# File size limit (2GB in bytes)
MAX_FILE_SIZE = 2000 * 1024 * 1024

# Supported file types and extensions
SUPPORTED_TYPES = [
    "document",
    "video",
    "audio",
    "photo",
    "voice",
    "video_note",
    "animation"
]

SUPPORTED_EXTENSIONS = [
    # Documents
    "pdf", "txt", "doc", "docx", "xls", "xlsx", "ppt", "pptx",
    # Programming Files
    "py", "js", "html", "css", "json", "xml", "yaml", "yml",
    # Archives
    "zip", "rar", "7z", "tar", "gz", "bz2",
    # Media Files
    "mp4", "mp3", "m4a", "wav", "avi", "mkv", "flv", "mov",
    "webm", "3gp", "m4v", "ogg", "opus",
    # Images
    "jpg", "jpeg", "png", "gif", "webp", "bmp", "ico",
    # Applications
    "apk", "exe", "msi", "deb", "rpm",
    # Other
    "txt", "text", "log", "csv", "md", "srt", "sub"
]

SUPPORTED_MIME_TYPES = [
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/zip",
    "application/x-rar-compressed",
    "application/x-7z-compressed",
    "video/mp4",
    "audio/mpeg",
    "audio/mp4",
    "image/jpeg",
    "image/png",
    "image/gif",
    "application/vnd.android.package-archive",
    "application/x-executable",
]

class Messages:
    START_TEXT = """
🎉 **Welcome to {bot_name}!** 🎉

Hello {user_mention}! I'm your secure file sharing assistant.

🔐 **Key Features:**
• Secure File Sharing
• Unique Download Links
• Multiple File Types Support
• Real-time Tracking

👨‍💻 Contact @Priyaverma2004 for support

Use /help to see available commands!
"""

    HELP_TEXT = """
📚 **Available Commands**

👥 **User Commands:**  
• `/start` – Start the bot  
• `/help` – Show this help menu  
• `/about` – Get bot details  
• `/short [url]` – Shorten a link (e.g., `/short example.com`)

👑 **Admin Commands:**  
• `/upload` – Upload a file (reply to a file)  
• `/stats` – View bot statistics  
• `/bcast` – Broadcast a message to all users  
• `/auto_del` – Set auto-delete timer  

🗑️ **Auto-Delete System:**  
• Files are auto-deleted after a set time  
• Use `/auto_del` to modify the timer  

📦 **Batch System:**  
• `/batch` – Group files into one link  
• Forward files, then reply with `/batch`

❓ **Need Help?** Contact [@Priyaverma2004](https://t.me/Priyaverma2004?text=Hello+😊)
"""

    ABOUT_TEXT = """
ℹ️ **About {bot_name}**

**Version:** `{version}`
**Owner:** @Priyaverma2004
**Language:** Python
**Framework:** Pyrogram


**Features:**
• Secure File Sharing
• Force Subscribe
• Admin Controls
• Real-time Stats
• Multiple File Types
• Enhanced Security
• Automatic File Type Detection


Made with ❤️ by @Priyaverma2004
"""

    FILE_TEXT = """
📁 **File Details**

**Name:** `{file_name}`
**Size:** {file_size}
**Type:** {file_type}
**Downloads:** {downloads}
**Uploaded:** {upload_time}
**By:** {uploader}

🔗 **Share Link:**
`{share_link}`
"""

    FORCE_SUB_TEXT = """
⚠️ **Access Restricted!**

Please join our channe/group to use this bot!

Click button below, then try again!
"""

class Buttons:
    def start_buttons() -> List[List[Dict[str, str]]]:
        return [
            [
                {"text": "Help 📚", "callback_data": "help"},
                {"text": "About ℹ️", "callback_data": "about"}
            ],
            [
                {"text": "Channel 📢", "url": CHANNEL_LINK},
                {"text": "❄️ Owner ❄️", "url": DEVELOPER_LINK}
            ]
        ]

    def help_buttons() -> List[List[Dict[str, str]]]:
        return [
            [
                {"text": "Home 🏠", "callback_data": "home"},
                {"text": "About ℹ️", "callback_data": "about"}
            ],
            [
                {"text": "Channel 📢", "url": CHANNEL_LINK}
            ]
        ]

    def about_buttons() -> List[List[Dict[str, str]]]:
        return [
            [
                {"text": "Home 🏠", "callback_data": "home"},
                {"text": "Help 📚", "callback_data": "help"}
            ],
            [
                {"text": "Channel 📢", "url": CHANNEL_LINK}
            ]
        ]

    def file_buttons(file_uuid: str) -> List[List[Dict[str, str]]]:
        return [
            [
                {"text": "Download 📥", "callback_data": f"download_{file_uuid}"},
                {"text": "Share 🔗", "callback_data": f"share_{file_uuid}"}
            ],
            [
                {"text": "Channel 📢", "url": CHANNEL_LINK}
            ]
        ]


class Progress:
    PROGRESS_BAR = "█"
    EMPTY_PROGRESS_BAR = "░"
    PROGRESS_TEXT = """
**{0}** {1}% 

**⚡️ Speed:** {2}/s
**💫 Done:** {3}
**💭 Total:** {4}
**⏰ Time Left:** {5}
"""
