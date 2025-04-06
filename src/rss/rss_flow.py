from prefect import flow
from tasks.create_tables import create_tables
from tasks.fetch_rss import fetch_rss_feed
from tasks.insert_articles import insert_articles_to_db
from prefect.schedules import Cron
import time


@flow
def rss_to_db_flow(feed_urls):
    create_tables()
    time.sleep(1)
    """Récupère les articles de plusieurs flux RSS et les insère dans la base de données"""
    for feed_url in feed_urls:
        articles = fetch_rss_feed(feed_url)
        insert_articles_to_db(articles, feed_url)


if __name__ == "__main__":
    feed_urls = [
        'https://www.lefigaro.fr/rss/figaro_actualites.xml',
        'https://www.lemonde.fr/rss/une.xml',
        'https://www.mediapart.fr/journal/podcast/chronique/rss',
        'https://www.francetvinfo.fr/titres.rss'
    ]

    rss_to_db_flow.serve(
        name="rss_flow",
        schedules=[
            Cron(
                "0 */2 * * *",
                parameters={
                    "feed_urls": feed_urls
                }
            )
        ]
    )
