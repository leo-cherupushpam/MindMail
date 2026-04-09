# 📧 Gmail Email Assistant

An AI-powered email assistant that helps you manage your Gmail inbox more efficiently using large language models.

## ✨ Features

This MVP implements six core email productivity features:

1. **💬 Conversational Q&A** - Ask questions about your emails and get contextual answers
2. **📝 Email Summarization** - Get concise summaries of email threads
3. **✉️ Draft Reply Generator** - Generate professional email replies based on your intent
4. **🧵 Thread Organization** - Organize and filter email threads by topic/date
5. **🏷️ Smart Inbox Rules** - Get automated suggestions for email categorization and labeling
6. **📅 Meeting Scheduler** - Extract meeting details (date, time, participants, agenda) from email threads

## 🏗️ Architecture

This implementation uses a **hybrid LLM approach** for optimal performance and cost efficiency:

- **SEARCH_MODEL** (`gpt-4.1-nano-2025-04-14`): Used for high-volume tasks like summarization, organization, and rule suggestion
- **DRAFTING_MODEL** (`gpt-5-nano-2025-08-07`): Used for quality-critical tasks like drafting replies and answering complex questions

## 📋 Requirements

- Python 3.8+
- Streamlit
- OpenAI API key

Install dependencies:
```bash
pip install -r requirements.txt
```

## 🔧 Setup

1. Get an OpenAI API key from [platform.openai.com](https://platform.openai.com/api-keys)
2. Set the environment variable:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
3. Run the application:
   ```bash
   streamlit run app/main.py
   ```

## 📁 Project Structure

```
gmail-email-assistant/
├── app/
│   └── main.py          # Streamlit web interface
├── services/
│   └── qa_service.py    # Core LLM functionality (6 features)
├── tests/
│   └── test_qa_service.py # Test suite
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## 🚀 Deployment

This application is ready for deployment to [Streamlit Cloud](https://streamlit.io/cloud):

1. Push this repository to GitHub
2. Connect your GitHub repository to Streamlit Cloud
3. Set the `OPENAI_API_KEY` as a secret in Streamlit Cloud settings
4. Deploy!

## 🧠 Design Decisions

### Hybrid LLM Approach
- Uses faster, cheaper models for high-volume tasks (summarization, organization)
- Uses higher-quality models for tasks requiring nuanced understanding (drafting, complex Q&A)
- Optimizes for both performance and cost efficiency

### Privacy-Focused Design
- Does not store full email bodies by default (light persistence approach)
- Processes emails in-memory for MVP demonstration
- Ready to extend with secure storage solutions

### Extensible Architecture
- Each feature is implemented as a separate, testable function
- Easy to add new email productivity features
- Clear separation between UI and business logic

## 📈 Future Enhancements

1. **Real Gmail API Integration** - Connect to actual Gmail accounts via OAuth 2.0
2. **Persistent Storage** - Store email metadata and embeddings for long-term insights
3. **User Authentication** - Multi-user support with secure session management
4. **Advanced Features** - Email scheduling, follow-up reminders, priority inbox
5. **Mobile Responsiveness** - Optimized interface for mobile devices

## 💡 Usage Examples

### Conversational Q&A
> "What did Sarah say about the budget last week?"
> 
> Returns: A contextual answer grounded in relevant email content

### Email Summarization
> "Summarize unread emails from today"
> 
> Returns: Concise summary of key topics and action items

### Draft Reply Generator
> "I need to tell the team I'll be delayed for the meeting"
> 
> Returns: Professional draft ready to send

## 📄 License

MIT License - feel free to use, modify, and distribute this project.

---

*Built with ❤️ using Streamlit and OpenAI*