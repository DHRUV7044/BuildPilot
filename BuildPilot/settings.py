"""
Shared settings for auto_updater.py and manual_build.py
Edit these values for your project
"""

import os
from pathlib import Path

# ==================== PROJECT SETTINGS ====================
PROJECT_DIR = r"D:\Gigbestcopilot_app\Gigbestcopilot"
GITHUB_REPO_URL = "https://github.com/yourusername/yourrepo.git"  # Optional: for clone if needed
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
APK_FILE_NAME = "com.yourcompany.yourapp.apk"  # Your actual APK filename

# ==================== CHECK INTERVAL ====================
# How often to check for updates (in seconds)
# Default: 300 seconds = 5 minutes
CHECK_INTERVAL = 300

# ==================== UPLOAD SETTINGS ====================

# --- Website Upload (HTTP POST) ---
WEBSITE_UPLOAD = {
    "enabled": True,
    "url": "https://your-website.com/api/upload-apk",  # Your website upload endpoint
    "api_key": "your-api-key-here",  # API key for authentication
    # Optional: additional headers
    "headers": {
        "Authorization": "Bearer your-token-here"
    }
}

# --- GitHub Release Upload ---
GITHUB_RELEASE = {
    "enabled": True,
    "token": "ghp_your_github_personal_access_token",  # GitHub PAT with repo scope
    "repo_owner": "yourusername",
    "repo_name": "yourrepo",
    "release_tag_prefix": "v",  # Tags will be like v1.0.0, v1.0.1, etc.
    "release_name_template": "Release {version}",
    "release_body_template": "Automated build from commit {commit_hash}\n\nChanges:\n{commit_message}",
    "draft": False,
    "prerelease": False
}

# ==================== LOGGING ====================
LOG_FILE = r"D:\Gigbestcopilot_app\Gigbestcopilot\build_automation.log"
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
COMMAND_TIMEOUT = 300

# Keep last N builds as backup
KEEP_BACKUP_BUILDS = 5
BACKUP_DIR = r"D:\Gigbestcopilot_app\Gigbestcopilot\BuildBackups"