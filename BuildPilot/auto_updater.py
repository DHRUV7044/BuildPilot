"""
Auto Updater - Continuously checks GitHub repo for updates
If new commits found: pulls, builds, uploads APK to website & GitHub releases
"""

import subprocess
import time
import os
import sys
import logging
import shutil
import hashlib
from datetime import datetime
from pathlib import Path

# Import shared settings
from settings import *

# Setup logging
def setup_logging():
    log_format = "%(asctime)s [%(levelname)s] %(message)s"
    handlers = [logging.StreamHandler(sys.stdout)]
    
    if LOG_FILE:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        handlers.append(logging.FileHandler(LOG_FILE, encoding='utf-8'))
    
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper()),
        format=log_format,
        handlers=handlers
    )
    return logging.getLogger(__name__)

logger = setup_logging()


class BuildAutomation:
    def __init__(self):
        self.project_dir = Path(PROJECT_DIR)
        self.last_commit_hash = None
        self.git_cmd = GIT_PATH if GIT_PATH else "git"
        self.dotnet_cmd = DOTNET_PATH if DOTNET_PATH else "dotnet"
        self.apk_path = None
        
    def run_command(self, command, cwd=None, shell=False):
        """Execute a command and return result"""
        cmd_str = ' '.join(command) if isinstance(command, list) else command
        working_dir = cwd or str(self.project_dir)
        
        logger.debug(f"Running: {cmd_str} in {working_dir}")
        
        try:
            result = subprocess.run(
                command,
                cwd=working_dir,
                capture_output=True,
                text=True,
                shell=shell,
                timeout=COMMAND_TIMEOUT
            )
            return result
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {cmd_str}")
            return None
        except Exception as e:
            logger.error(f"Command failed: {e}")
            return None
    
    def get_latest_commit(self):
        """Get the latest commit hash from remote"""
        # Fetch latest info from remote
        result = self.run_command([self.git_cmd, "fetch", "origin", BRANCH])
        if result is None or result.returncode != 0:
            logger.error(f"Git fetch failed: {result.stderr if result else 'Timeout'}")
            return None
        
        # Get local HEAD hash
        result = self.run_command([self.git_cmd, "rev-parse", "HEAD"])
        if result is None or result.returncode != 0:
            return None
        local_hash = result.stdout.strip()
        
        # Get remote HEAD hash
        result = self.run_command([self.git_cmd, "rev-parse", f"origin/{BRANCH}"])
        if result is None or result.returncode != 0:
            return None
        remote_hash = result.stdout.strip()
        
        return local_hash, remote_hash
    
    def get_commit_info(self, commit_hash):
        """Get commit message and author for release notes"""
        result = self.run_command([
            self.git_cmd, "log", "-1", 
            "--pretty=format:%s%n%b%nAuthor: %an <%ae>%nDate: %ad",
            commit_hash
        ])
        if result and result.returncode == 0:
            return result.stdout.strip()
        return "No commit info available"
    
    def pull_latest(self):
        """Pull latest changes from GitHub"""
        logger.info("Pulling latest changes...")
        result = self.run_command([self.git_cmd, "pull", "origin", BRANCH])
        
        if result and result.returncode == 0:
            logger.info("Pull successful")
            logger.debug(result.stdout)
            return True
        else:
            logger.error(f"Pull failed: {result.stderr if result else 'Unknown error'}")
            return False
    
    def build_project(self):
        """Build the .NET MAUI/Android project"""
        logger.info("Starting build...")
        
        # Clean first
        logger.info("Cleaning previous build...")
        clean_result = self.run_command([
            self.dotnet_cmd, "clean", str(SOLUTION_FILE)
        ])
        
        # Build
        build_cmd = [
            self.dotnet_cmd, "build",
            str(ANDROID_CSPROJ),
            "-c", BUILD_CONFIGURATION,
            "-f", "net10.0-android",
            "-p:AndroidPackageFormat=apk"
        ]
        
        logger.info(f"Building: {' '.join(build_cmd)}")
        result = self.run_command(build_cmd)
        
        if result and result.returncode == 0:
            logger.info("Build successful!")
            logger.debug(result.stdout)
            return True
        else:
            logger.error(f"Build failed: {result.stderr if result else 'Unknown error'}")
            return False
    
    def find_apk(self):
        """Find the generated APK file"""
        apk_dir = Path(APK_OUTPUT_DIR)
        
        # Look for APK files
        apk_files = list(apk_dir.glob("*.apk"))
        
        if apk_files:
            # Get the most recent one
            latest_apk = max(apk_files, key=lambda p: p.stat().st_mtime)
            self.apk_path = latest_apk
            logger.info(f"Found APK: {latest_apk}")
            return True
        
        # Fallback to configured name
        configured_apk = apk_dir / APK_FILE_NAME
        if configured_apk.exists():
            self.apk_path = configured_apk
            logger.info(f"Found APK: {configured_apk}")
            return True
        
        logger.error("APK file not found!")
        return False
    
    def backup_build(self):
        """Backup the built APK"""
        if not KEEP_BACKUP_BUILDS or not self.apk_path:
            return
        
        backup_dir = Path(BACKUP_DIR)
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"build_{timestamp}_{self.apk_path.name}"
        backup_path = backup_dir / backup_name
        
        shutil.copy2(self.apk_path, backup_path)
        logger.info(f"Backup created: {backup_path}")
        
        # Clean old backups
        backups = sorted(backup_dir.glob("build_*.apk"), key=lambda p: p.stat().st_mtime)
        if len(backups) > KEEP_BACKUP_BUILDS:
            for old_backup in backups[:-KEEP_BACKUP_BUILDS]:
                old_backup.unlink()
                logger.info(f"Removed old backup: {old_backup}")
    
    def upload_to_website(self):
        """Upload APK to specified website"""
        if not WEBSITE_UPLOAD["enabled"]:
            logger.info("Website upload disabled")
            return True
        
        if not self.apk_path:
            logger.error("No APK to upload")
            return False
        
        logger.info(f"Uploading to website: {WEBSITE_UPLOAD['url']}")
        
        try:
            import requests
            
            headers = {"X-API-Key": WEBSITE_UPLOAD["api_key"]}
            headers.update(WEBSITE_UPLOAD.get("headers", {}))
            
            with open(self.apk_path, "rb") as f:
                files = {"file": (self.apk_path.name, f, "application/vnd.android.package-archive")}
                response = requests.post(
                    WEBSITE_UPLOAD["url"],
                    headers=headers,
                    files=files,
                    timeout=300
                )
            
            if response.status_code in [200, 201]:
                logger.info("Website upload successful!")
                return True
            else:
                logger.error(f"Upload failed: HTTP {response.status_code} - {response.text}")
                return False
                
        except ImportError:
            logger.error("requests library not installed. Run: pip install requests")
            return False
        except Exception as e:
            logger.error(f"Upload error: {e}")
            return False
    
    def upload_to_github_release(self, commit_hash, commit_message):
        """Upload APK to GitHub release"""
        if not GITHUB_RELEASE["enabled"]:
            logger.info("GitHub release disabled")
            return True
        
        if not self.apk_path:
            logger.error("No APK to upload")
            return False
        
        logger.info("Creating GitHub release...")
        
        try:
            import requests
            
            # Generate version from commit hash (first 7 chars) and timestamp
            short_hash = commit_hash[:7]
            version = f"{datetime.now().strftime('%Y.%m.%d')}-{short_hash}"
            tag_name = f"{GITHUB_RELEASE['release_tag_prefix']}{version}"
            
            # Create release
            release_url = f"https://api.github.com/repos/{GITHUB_RELEASE['repo_owner']}/{GITHUB_RELEASE['repo_name']}/releases"
            headers = {
                "Authorization": f"token {GITHUB_RELEASE['token']}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            release_data = {
                "tag_name": tag_name,
                "name": GITHUB_RELEASE["release_name_template"].format(version=version),
                "body": GITHUB_RELEASE["release_body_template"].format(
                    version=version,
                    commit_hash=commit_hash,
                    commit_message=commit_message
                ),
                "draft": GITHUB_RELEASE["draft"],
                "prerelease": GITHUB_RELEASE["prerelease"]
            }
            
            response = requests.post(release_url, headers=headers, json=release_data)
            
            if response.status_code == 201:
                release_info = response.json()
                upload_url = release_info["upload_url"].replace("{?name,label}", "")
                logger.info(f"Release created: {release_info['html_url']}")
            elif response.status_code == 422:
                # Release might already exist, try to get it
                logger.warning("Release may already exist, checking...")
                get_url = f"{release_url}/tags/{tag_name}"
                response = requests.get(get_url, headers=headers)
                if response.status_code == 200:
                    release_info = response.json()
                    upload_url = release_info["upload_url"].replace("{?name,label}", "")
                else:
                    logger.error(f"Failed to create/get release: {response.text}")
                    return False
            else:
                logger.error(f"Failed to create release: {response.status_code} - {response.text}")
                return False
            
            # Upload APK asset
            logger.info("Uploading APK to release...")
            asset_name = self.apk_path.name
            
            with open(self.apk_path, "rb") as f:
                headers["Content-Type"] = "application/vnd.android.package-archive"
                upload_response = requests.post(
                    upload_url,
                    headers=headers,
                    params={"name": asset_name},
                    data=f,
                    timeout=300
                )
            
            if upload_response.status_code == 201:
                logger.info("GitHub release upload successful!")
                return True
            else:
                logger.error(f"Asset upload failed: {upload_response.status_code} - {upload_response.text}")
                return False
                
        except ImportError:
            logger.error("requests library not installed. Run: pip install requests")
            return False
        except Exception as e:
            logger.error(f"GitHub release error: {e}")
            return False
    
    def send_notification(self, success, message=""):
        """Send notification to webhook (Discord/Slack)"""
        if not NOTIFICATIONS["enabled"] or not NOTIFICATIONS["webhook_url"]:
            return
        
        try:
            import requests
            
            color = 0x00FF00 if success else 0xFF0000
            status = "✅ SUCCESS" if success else "❌ FAILED"
            
            payload = {
                "embeds": [{
                    "title": f"Build Automation - {status}",
                    "description": message,
                    "color": color,
                    "timestamp": datetime.now().isoformat()
                }]
            }
            
            requests.post(NOTIFICATIONS["webhook_url"], json=payload, timeout=10)
        except Exception as e:
            logger.error(f"Notification failed: {e}")
    
    def run_full_pipeline(self):
        """Run the complete build and upload pipeline"""
        commit_info = self.get_commit_info(self.last_commit_hash) if self.last_commit_hash else ""
        
        success = True
        results = []
        
        # Pull
        if not self.pull_latest():
            success = False
            results.append("Pull: FAILED")
        else:
            results.append("Pull: OK")
        
        # Build
        if success and not self.build_project():
            success = False
            results.append("Build: FAILED")
        else:
            results.append("Build: OK")
        
        # Find APK
        if success and not self.find_apk():
            success = False
            results.append("Find APK: FAILED")
        else:
            results.append("Find APK: OK")
        
        # Backup
        if success:
            self.backup_build()
            results.append("Backup: OK")
        
        # Upload to website
        if success:
            if self.upload_to_website():
                results.append("Website Upload: OK")
            else:
                results.append("Website Upload: FAILED")
                success = False
        
        # Upload to GitHub release
        if success:
            commit_msg = self.get_commit_info(self.last_commit_hash)
            if self.upload_to_github_release(self.last_commit_hash, commit_msg):
                results.append("GitHub Release: OK")
            else:
                results.append("GitHub Release: FAILED")
                # Don't mark as full failure, release is optional
        
        # Notification
        self.send_notification(success, "\n".join(results))
        
        return success
    
    def check_and_update(self):
        """Main check loop - returns True if update was processed"""
        logger.info("Checking for updates...")
        
        hashes = self.get_latest_commit()
        if not hashes:
            logger.error("Failed to get commit info")
            return False
        
        local_hash, remote_hash = hashes
        
        logger.info(f"Local:  {local_hash[:7]}")
        logger.info(f"Remote: {remote_hash[:7]}")
        
        if local_hash == remote_hash:
            logger.info("No new commits. Project is up to date.")
            return False
        
        logger.info("New commits detected! Starting update...")
        self.last_commit_hash = remote_hash
        
        return self.run_full_pipeline()


def main():
    logger.info("=" * 50)
    logger.info("Auto Updater Started")
    logger.info(f"Project: {PROJECT_DIR}")
    logger.info(f"Check interval: {CHECK_INTERVAL} seconds")
    logger.info("=" * 50)
    
    automation = BuildAutomation()
    
    while True:
        try:
            automation.check_and_update()
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
        
        logger.info(f"Sleeping for {CHECK_INTERVAL} seconds...")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()