# MailMind Setup Guide

## Prerequisites

- Python 3.8+
- OpenAI API key
- Modern web browser

## Setup Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set OpenAI API Key

```bash
export OPENAI_API_KEY=sk-your-api-key-here
```

### 3. Start the Server

```bash
uvicorn app.api:app --reload
```

The app will be available at `http://localhost:8000`

### 4. Open in Browser

Navigate to http://localhost:8000 and start exploring:
- Browse sample email threads
- Ask AI questions about emails
- Generate draft replies
- Summarize conversations
- Compose new emails with AI assistance

## Environment Variables

- `OPENAI_API_KEY` — Your OpenAI API key (required)
- `FASTAPI_ENV` — Environment (development/production, optional)
- `PORT` — Server port (default: 8000, optional)

## Troubleshooting

**"OPENAI_API_KEY not found"**
- Set the environment variable: `export OPENAI_API_KEY=sk-...`
- Check with: `echo $OPENAI_API_KEY`

**"Port 8000 already in use"**
- Run on a different port: `uvicorn app.api:app --reload --port 8001`

**"OpenAI API error"**
- Verify your API key is valid
- Check your OpenAI account has available credits
- Ensure you have access to gpt-4o and gpt-4o-mini models

## Security Notes

- Never commit your OpenAI API key to git
- Store API key in environment variables only
- `.env` file should be in `.gitignore`
- Rotate API keys periodically for production use
