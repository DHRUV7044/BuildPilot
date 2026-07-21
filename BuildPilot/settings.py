"""
Shared settings for auto_updater.py and manual_build.py
Edit these values for your project
"""

import os
from pathlib import Path
from dotenv import load_dotenv  # pip install python-dotenv
import sys
sys.dont_write_bytecode = True

# Load environment variables from key.env
env_path = Path(__file__).parent / "key.env"
load_dotenv(dotenv_path=env_path)

# ==================== PROJECT SETTINGS ====================
PROJECT_DIR = r"D:\Gigbestcopilot_app\Gigbestcopilot"
# Optional: for clone if needed
GITHUB_REPO_URL = "https://github.com/mukptl/Gigbestcopilot.git"
BRANCH = "main"  # Branch to track

# ==================== BUILD SETTINGS ====================
# Path to your .csproj or .sln file for building APK
ANDROID_CSPROJ = r"D:\Gigbestcopilot_app\Gigbestcopilot\Platforms\Gigbestcopilot.Android\Gigbestcopilot.Android.csproj"
# Or use SOLUTION_FILE if you prefer building solution
SOLUTION_FILE = r"D:\Gigbestcopilot_app\Gigbestcopilot\YourSolution.sln"

# Build configuration
BUILD_CONFIGURATION = "Release"
BUILD_TARGET = "Publish"  # or "Build"

# Where the built APK is located after build (adjust path as needed)
APK_OUTPUT_DIR = r"D:\Gigbestcopilot_app\Gigbestcopilot\Platforms\Gigbestcopilot.Android\bin\Release\net10.0-android"
APK_FILE_NAME = "com.gigbestcopilot.android-Signed.apk"  # Your actual APK filename

# ==================== CHECK INTERVAL ====================
# How often to check for updates (in seconds)
# Default: 300 seconds = 5 minutes
CHECK_INTERVAL = 3600  # 1 hour

# ==================== UPLOAD SETTINGS ====================

# --- Website Upload (HTTP POST) ---
WEBSITE_UPLOAD = {
    "enabled": False,  # Set to True to enable website upload
    "url": "https://your-website.com/api/upload-apk",  # Your website upload endpoint
    "api_key": os.getenv("WEBSITE_API_KEY", ""),  # API key for authentication
    # Optional: additional headers
    "headers": {
        "Authorization": "Bearer your-token-here"
    }
}

# --- GitHub Release Upload ---
GITHUB_RELEASE = {
    "enabled": True,
    "token": os.getenv("GITHUB_TOKEN", ""),  # GitHub PAT with repo scope
    "repo_owner": "DHRUV7044",
    "repo_name": "Gigbestcopilot",
    "release_tag_prefix": "v",  # Tags will be like v1.0.0, v1.0.1, etc.
    "release_name_template": "Release {version}",
    "release_body_template": "Automated build from commit {commit_hash}\n\nChanges:\n{commit_message}",
    "draft": False,
    "prerelease": False
}

# ==================== LOGGING ====================
LOG_FILE = r"D:\Gigbestcopilot_app\BuildPilot\BuildPilot\build_automation.log"
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR

# ==================== NOTIFICATIONS (Optional) ====================
# Send notification on success/failure
NOTIFICATIONS = {
    "enabled": False,
    "webhook_url": "",  # Discord/Slack webhook URL
    "on_success": True,
    "on_failure": True
}

# ==================== ADVANCED ====================
# Git executable path (leave empty to use system PATH)
GIT_PATH = ""  # e.g., r"C:\Program Files\Git\bin\git.exe"

# .NET executable path (leave empty to use system PATH)
DOTNET_PATH = ""  # e.g., r"C:\Program Files\dotnet\dotnet.exe"

# Timeout for commands (in seconds)
COMMAND_TIMEOUT = 600

# Keep last N builds as backup
KEEP_BACKUP_BUILDS = 5
BACKUP_DIR = r"D:\Gigbestcopilot_app\backup_builds"
