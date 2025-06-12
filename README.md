# AI News Summarizer & Sentiment Analyzer

🔍 Search latest news by topic  
🧠 Summarized with HuggingFace Transformers  
😊 Sentiment tagged with VADER

## Features
- Topic-based news search
- Text summarization with BART
- Sentiment analysis: Positive / Neutral / Negative
- Clean, responsive web interface
- Live news integration (with API key)

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-news-analyzer.git
cd ai-news-analyzer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Create a `.env` file
   - Add your NewsAPI key: `NEWS_API_KEY=your_api_key_here`

5. Run the application:
```bash
python app.py
```

6. Open your browser and visit: `http://localhost:5000`

## Deployment to Render

1. Push your code to a GitHub repository

2. Go to [Render Dashboard](https://dashboard.render.com/)

3. Click "New" and select "Web Service"

4. Connect your GitHub repository

5. Configure the deployment:
   - Name: `ai-news-analyzer` (or your preferred name)
   - Region: Choose the one closest to your users
   - Branch: `main` (or your preferred branch)
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

6. Add environment variables:
   - `PYTHON_VERSION`: 3.9.0
   - `NEWS_API_KEY`: your_newsapi_key_here

7. Click "Create Web Service"

## Environment Variables

- `NEWS_API_KEY`: Your NewsAPI.org API key (required for live news)
- `PYTHON_VERSION`: Python version (3.9.0 recommended)

## Tech Stack

- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript
- AI: HuggingFace Transformers (BART), VADER Sentiment Analysis
- Deployment: Render, Gunicorn

## License

MIT
