# content_dashboard.py
from flask import Flask, render_template_string, request, jsonify
import requests
import json
from datetime import datetime, timedelta
import feedparser
import time
from urllib.parse import urlencode
import html
import random

app = Flask(__name__)

# =============================================
# CONFIGURATION
# =============================================

YOUTUBE_API_KEY = "AIzaSyBqh7d0fynLsuI8vn9x3iLft-T9CS_-wcQ"
NEWS_API_KEY = "604abd06bfd84acd9d5c5762dd6900cf"

YOUTUBE_TOPICS = [
    "trending memes compilation",
    "viral funny videos 2024",
    "world politics news today",
    "global politics update",
    "breaking international news",
    "US politics latest",
    "Europe news today",
    "Russia Ukraine war update",
    "China news today",
    "Middle East news latest",
    "Narendra Modi latest news",
    "India news today",
    "Modi government schemes",
    "Indian politics update",
    "BJP latest news",
    "India economic news",
    "Modi speech highlights",
    "motivational speech inspiration",
    "life lessons that will change you",
    "best motivational video",
    "success mindset motivation",
    "powerful life advice",
    "morning motivation 2024",
    "how to be successful in life",
    "good human values",
    "kindness motivation",
    "inspirational stories real life",
    "humanity motivational video",
    "positive thinking motivation",
    "spiritual motivation",
    "moral stories inspirational"
]

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Viral Content Hub - Trending Dashboard</title>
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 30px;
    min-height: 100vh;
}
.container {
    max-width: 1400px;
    margin: 0 auto;
}
h1 {
    text-align: center;
    color: white;
    margin-bottom: 10px;
    font-size: 2.5rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}
.subtitle {
    text-align: center;
    color: rgba(255,255,255,0.9);
    margin-bottom: 30px;
    font-size: 1.1rem;
}
.source-tabs {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-bottom: 40px;
    flex-wrap: wrap;
}
.source-btn {
    padding: 12px 30px;
    background: rgba(255,255,255,0.2);
    color: white;
    text-decoration: none;
    border-radius: 50px;
    font-weight: bold;
    transition: all 0.3s;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.3);
    display: inline-block;
}
.source-btn.active {
    background: #ff4500;
    color: white;
    border-color: #ff4500;
}
.source-btn:hover {
    background: #ff6347;
    transform: translateY(-2px);
}
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 30px;
}
.card {
    background: white;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    transition: all 0.3s;
}
.card:hover {
    transform: translateY(-10px);
    box-shadow: 0 30px 50px rgba(0,0,0,0.2);
}
.card img {
    width: 100%;
    height: 250px;
    object-fit: cover;
    transition: transform 0.3s;
}
.card:hover img {
    transform: scale(1.05);
}
.no-image {
    height: 250px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-size: 3rem;
}
.content {
    padding: 20px;
}
.title {
    font-size: 18px;
    font-weight: bold;
    line-height: 1.4;
    margin-bottom: 15px;
    color: #333;
}
.stats {
    display: flex;
    justify-content: space-between;
    color: #777;
    font-size: 14px;
    margin-bottom: 15px;
    padding-bottom: 15px;
    border-bottom: 1px solid #eee;
    flex-wrap: wrap;
    gap: 10px;
}
.buttons {
    display: flex;
    gap: 10px;
}
.btn {
    flex: 1;
    padding: 12px;
    text-align: center;
    text-decoration: none;
    border-radius: 10px;
    font-weight: bold;
    font-size: 14px;
    transition: all 0.3s;
    cursor: pointer;
    display: inline-block;
}
.view {
    background: #ff4500;
    color: #fff;
}
.view:hover {
    background: #ff6347;
    transform: translateY(-2px);
}
.download {
    background: #f0f0f0;
    color: #333;
}
.download:hover {
    background: #e0e0e0;
    transform: translateY(-2px);
}
.error {
    background: rgba(255,0,0,0.8);
    color: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    margin: 20px;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
.card {
    animation: fadeIn 0.5s ease-out;
}
@media (max-width: 768px) {
    body { padding: 15px; }
    h1 { font-size: 1.8rem; }
    .grid { grid-template-columns: 1fr; }
}
</style>
</head>
<body>
<div class="container">
    <h1>🎯 Viral Content Hub</h1>
    <p class="subtitle">Curated trending content for creators & social media managers</p>

    <div class="source-tabs">
        <a href="/?source=reddit" class="source-btn {% if current_source == 'reddit' %}active{% endif %}">🔥 Reddit Hot</a>
        <a href="/?source=youtube" class="source-btn {% if current_source == 'youtube' %}active{% endif %}">📹 Viral Videos</a>
        <a href="/?source=trends" class="source-btn {% if current_source == 'trends' %}active{% endif %}">📈 Google Trends</a>
    </div>

    {% if current_source == 'reddit' %}
        <h1>🔥 Viral from r/{{ subreddit }}</h1>
        <p class="subtitle">Top trending posts today | High engagement content</p>
        <div class="grid">
        {% for post in reddit_posts %}
            <div class="card">
                {% if post.image %}
                    <img src="{{ post.image }}" alt="Post">
                {% else %}
                    <div class="no-image">📝 Text Post</div>
                {% endif %}
                <div class="content">
                    <div class="title">{{ post.title }}</div>
                    <div class="stats">
                        <span>⬆️ {{ post.score }} upvotes</span>
                        <span>💬 {{ post.comments }} comments</span>
                        <span>📊 {{ post.upvote_ratio }}% liked</span>
                    </div>
                    <div class="buttons">
                        <a href="{{ post.url }}" target="_blank" class="btn view">View Post</a>
                        <a href="{{ post.download_url }}" target="_blank" class="btn download">Save Media</a>
                    </div>
                </div>
            </div>
        {% endfor %}
        </div>
    {% elif current_source == 'youtube' %}
        <h1>📹 Viral Video Feed</h1>
        <p class="subtitle">High-quality trending videos with good engagement</p>
        <div class="grid">
        {% for video in youtube_videos %}
            <div class="card">
                {% if video.thumbnail %}
                    <img src="{{ video.thumbnail }}" alt="Video Thumbnail">
                {% else %}
                    <div class="no-image">🎬 No Thumbnail</div>
                {% endif %}
                <div class="content">
                    <div class="title">{{ video.title }}</div>
                    <div class="stats">
                        <span>📺 {{ video.channel }}</span>
                        <span>📅 {{ video.published_at }}</span>
                    </div>
                    <div class="buttons">
                        <a href="{{ video.url }}" target="_blank" class="btn view">Watch Video</a>
                        <a href="{{ video.thumbnail }}" target="_blank" class="btn download">Save Thumbnail</a>
                    </div>
                </div>
            </div>
        {% endfor %}
        </div>
    {% elif current_source == 'trends' %}
        <h1>📈 Google Trends</h1>
        <p class="subtitle">What's trending right now</p>
        <div class="grid">
        {% for trend in trends %}
            <div class="card">
                <div class="content">
                    <div class="title">🔍 {{ trend.title }}</div>
                    <div class="stats">
                        <span>🌍 Trending in {{ trend.geo }}</span>
                    </div>
                    <p style="color:#666; font-size:14px; margin-top:10px;">
                        {{ trend.description[:150] }}
                    </p>
                </div>
            </div>
        {% endfor %}
        </div>
    {% endif %}
</div>
</body>
</html>
"""

def fetch_reddit_posts(subreddit='memes', limit=20):
    """Fetch Reddit posts"""
    url = f"https://www.reddit.com/r/{subreddit}/top.json?t=day&limit={limit}"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; TrendingDashboard/1.0)"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            posts = []
            for child in data['data']['children']:
                item = child['data']
                image = ''
                if 'preview' in item and 'images' in item['preview']:
                    image = item['preview']['images'][0]['source']['url']
                    image = html.unescape(image)
                
                posts.append({
                    'title': html.escape(item.get('title', 'Untitled')),
                    'score': f"{item.get('score', 0):,}",
                    'comments': f"{item.get('num_comments', 0):,}",
                    'url': f"https://www.reddit.com{item.get('permalink', '')}",
                    'image': image,
                    'download_url': image or f"https://www.reddit.com{item.get('permalink', '')}",
                    'upvote_ratio': round(item.get('upvote_ratio', 0) * 100)
                })
            return posts
    except Exception as e:
        print(f"Error fetching Reddit: {e}")
    return []

def fetch_youtube_videos():
    """Fetch YouTube videos"""
    if not YOUTUBE_API_KEY:
        return []
    
    all_videos = {}
    published_after = (datetime.now() - timedelta(hours=24)).isoformat() + 'Z'
    
    for query in YOUTUBE_TOPICS[:10]:  # Limit to 10 topics to avoid rate limiting
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "type": "video",
            "order": "viewCount",
            "regionCode": "IN",
            "maxResults": 3,
            "publishedAfter": published_after,
            "videoDuration": "short",
            "q": query,
            "key": YOUTUBE_API_KEY
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for item in data.get('items', []):
                    video_id = item.get('id', {}).get('videoId')
                    if video_id and video_id not in all_videos:
                        all_videos[video_id] = item
            time.sleep(0.1)
        except Exception as e:
            print(f"Error fetching YouTube: {e}")
    
    # Filter and process videos
    videos = []
    for item in all_videos.values():
        title = item.get('snippet', {}).get('title', '')
        # Filter low quality
        bad_keywords = ['tutorial', 'lesson', 'course', 'teaching', 'educational', 'how to']
        is_low_quality = any(kw in title.lower() for kw in bad_keywords)
        
        if not is_low_quality and len(title) > 10:
            video_id = item.get('id', {}).get('videoId')
            snippet = item.get('snippet', {})
            thumbnail = snippet.get('thumbnails', {}).get('high', {}).get('url') or \
                       snippet.get('thumbnails', {}).get('medium', {}).get('url') or ''
            
            videos.append({
                'title': html.escape(title[:100]),
                'thumbnail': thumbnail,
                'url': f"https://www.youtube.com/watch?v={video_id}",
                'channel': html.escape(snippet.get('channelTitle', '')),
                'published_at': datetime.strptime(snippet.get('publishedAt', datetime.now().isoformat()), '%Y-%m-%dT%H:%M:%SZ').strftime('%b %d, %Y')
            })
    
    return videos[:20]

def fetch_google_trends():
    """Fetch Google Trends"""
    feeds = {
        'US': 'https://trends.google.com/trending/rss?geo=US',
        'GB': 'https://trends.google.com/trending/rss?geo=GB',
        'IN': 'https://trends.google.com/trending/rss?geo=IN'
    }
    
    all_trends = []
    seen_titles = set()
    
    for geo, feed_url in feeds.items():
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:10]:
                if entry.title not in seen_titles:
                    seen_titles.add(entry.title)
                    all_trends.append({
                        'title': html.escape(entry.title),
                        'geo': geo,
                        'description': html.escape(entry.description if hasattr(entry, 'description') else '')
                    })
        except Exception as e:
            print(f"Error fetching trends for {geo}: {e}")
    
    return all_trends[:20]

@app.route('/')
def index():
    """Main route"""
    current_source = request.args.get('source', 'reddit')
    subreddit = 'memes'
    
    context = {
        'current_source': current_source,  # Changed from 'source' to 'current_source'
        'subreddit': subreddit,
        'reddit_posts': [],
        'youtube_videos': [],
        'trends': []
    }
    
    if current_source == 'reddit':
        context['reddit_posts'] = fetch_reddit_posts(subreddit)
    elif current_source == 'youtube':
        context['youtube_videos'] = fetch_youtube_videos()
    elif current_source == 'trends':
        context['trends'] = fetch_google_trends()
    
    return render_template_string(HTML_TEMPLATE, **context)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/reddit')
def api_reddit():
    """API endpoint for Reddit data"""
    posts = fetch_reddit_posts()
    return jsonify(posts)

@app.route('/api/youtube')
def api_youtube():
    """API endpoint for YouTube data"""
    videos = fetch_youtube_videos()
    return jsonify(videos)

@app.route('/api/trends')
def api_trends():
    """API endpoint for Google Trends data"""
    trends = fetch_google_trends()
    return jsonify(trends)

if __name__ == '__main__':
    print("=" * 50)
    print("🎯 Content Dashboard Starting...")
    print("=" * 50)
    print(f"📊 YouTube API Key: {'✓ Set' if YOUTUBE_API_KEY else '✗ Missing'}")
    print(f"🌐 Server running on: http://localhost:5002")
    print(f"📱 Dashboard URL: http://localhost:5002/?source=reddit")
    print("=" * 50)
    print("Press CTRL+C to stop the server\n")
    
    app.run(host='0.0.0.0', port=5002, debug=False)