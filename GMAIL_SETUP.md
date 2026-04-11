# Gmail Setup Guide

## Prerequisites

- Google account with Gmail
- Google Cloud account

## Setup Steps

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click "Create Project"
3. Name: "Gmail Email Assistant" (or your preference)
4. Click "Create"

### 2. Enable Gmail API

1. In Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click "Enable"

### 3. Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Choose "Desktop application"
4. Click "Create"
5. Download the JSON file
6. Save as `client_secret.json` in the project root

### 4. Run the App

```bash
streamlit run app/main.py
```

1. Click "Authenticate with Gmail"
2. Sign in with your Google account
3. Grant permission for the app to read emails
4. App fetches and caches your emails

## File Locations

- `credentials.json` — OAuth tokens (auto-created, git-ignored)
- `cached_emails.json` — Cached email threads (git-ignored)
- `client_secret.json` — OAuth credentials from Google Cloud (git-ignored)

## Troubleshooting

**"client_secret.json not found"**
- Ensure you downloaded the credentials file from Google Cloud Console
- Place it in the project root directory

**"Permission denied"**
- Check that the Gmail API is enabled in Google Cloud Console
- Try logging out and re-authenticating

**"No emails found"**
- Check that your Gmail inbox has messages
- Try clicking "Refresh Emails"

## Security Notes

- Never commit `client_secret.json` or `credentials.json` to git
- Both files are in `.gitignore`
- Delete `credentials.json` before sharing the project
- OAuth tokens are automatically refreshed
