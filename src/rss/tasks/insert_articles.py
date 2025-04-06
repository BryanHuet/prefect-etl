from prefect import task
from utils.utils import  get_db_connection, get_sql_file

@task
def insert_articles_to_db(articles, feed_url):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        get_sql_file('rss/data/queries/select/source_id.sql'), (feed_url,)
    )
    feed_id = cursor.fetchone()

    if feed_id is None:
        cursor.execute(
            get_sql_file('rss/data/queries/insert/source.sql'), (feed_url.split('/')[2], feed_url)
        )
        feed_id = cursor.lastrowid
    else:
        feed_id = feed_id[0]

    for article in articles:
        cursor.execute(
            get_sql_file('rss/data/queries/insert/article.sql'),
            (feed_id, article['title'], article['link'], article['description'], article['content'], article['published_at'])
        )

    conn.commit()
    conn.close()