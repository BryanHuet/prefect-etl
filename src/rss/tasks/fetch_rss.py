from prefect import task
import feedparser
from datetime import datetime

@task
def fetch_rss_feed(feed_url):
    """Récupère et analyse un flux RSS"""
    feed = feedparser.parse(feed_url)
    articles = []

    for entry in feed.entries:
        article = {
            'title': entry.title,
            'link': entry.link,
            'description': entry.get('description', ''),
            'content': entry.get('content', [{'value': ''}])[0]['value'],
            'published_at': entry.get('published', datetime.now().isoformat()),
        }
        articles.append(article)

    return articles