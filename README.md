# BuildPilot

A modular, lightweight build automation utility written in Python for Windows, designed to automate local and remote software build pipelines.

## Features
- **Pipeline Automation**: Integrates Git pulling, .NET compiling, artifact packing, and backup rotation.
- **Multi-Platform Support**: Built to compile C# .NET MAUI projects for Android, Windows, and Linux.
- **Backups Rotation Manager**: Automatically backs up binaries to a local backup directory (`backup_builds/`), preserving a configurable window of the last $N$ builds.
- **Upload Routing Providers**: Supports publishing built binaries (e.g. Android APKs) via HTTP POST endpoints or as GitHub releases using environment-configured access tokens.
- **System Webhooks**: Sends notifications to Discord or Slack detailing compilation results.

## Execution Flows
- **`auto_updater.py`**: Watches repository branches for commits and triggers updates.
- **`manual_build.py`**: Force-triggers the pipeline (Git pull -> Build -> Upload -> Notification) immediately.
- **`settings.py`**: Configuration dictionary mapping MSBuild paths, APK output destinations, and API tokens.\n