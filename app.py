from flask import Flask, render_template, request, jsonify, send_from_directory
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')

# Initialize AI models
sentiment_analyzer = SentimentIntensityAnalyzer()
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Sample news data
with open('sample_news.json', 'r') as f:
    SAMPLE_NEWS = json.load(f)

def analyze_sentiment(text):
    scores = sentiment_analyzer.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= 0.05:
        return "😊 Positive", "positive"
    elif compound <= -0.05:
        return "😞 Negative", "negative"
    else:
        return "😐 Neutral", "neutral"

def get_summary(text):
    try:
        input_length = len(text.split())
        max_length = min(100, input_length * 0.8)
        min_length = max(20, input_length * 0.4)
        
        summary = summarizer(
            text,
            max_length=int(max_length),
            min_length=int(min_length),
            do_sample=False
        )[0]['summary_text']
        return summary
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Could not generate summary"

def fetch_live_news(topic):
    try:
        api_key = os.getenv('NEWS_API_KEY')
        if not api_key:
            raise ValueError("API key not found")
            
        url = 'https://newsapi.org/v2/everything'
        params = {
            'q': topic,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 5,
            'apiKey': api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] != 'ok':
            raise Exception(data.get('message', 'Unknown error'))
            
        return [{
            'title': article['title'],
            'description': article['description'] or article['content'] or article['title'],
            'url': article['url']
        } for article in data['articles']]
        
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html', has_api_key=bool(os.getenv('NEWS_API_KEY')))

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        text = data.get('text', '')
        
        summary = get_summary(text)
        sentiment, sentiment_class = analyze_sentiment(text)
        
        return jsonify({
            'success': True,
            'summary': summary,
            'sentiment': sentiment,
            'sentimentClass': sentiment_class
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/news', methods=['GET'])
def get_news():
    try:
        topic = request.args.get('topic', '')
        use_sample = request.args.get('sample', 'false').lower() == 'true'
        
        if use_sample or not topic:
            return jsonify({
                'success': True,
                'articles': SAMPLE_NEWS,
                'isSample': True
            })
            
        articles = fetch_live_news(topic)
        if not articles:
            raise Exception("Failed to fetch live news")
            
        return jsonify({
            'success': True,
            'articles': articles,
            'isSample': False
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'fallback': True
        })

if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, port=5000)
