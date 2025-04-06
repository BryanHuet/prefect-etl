from prefect import flow,get_run_logger
from tasks.find_category import find_category, get_article_without_category
import time
from prefect.schedules import Cron

@flow
def rss_category_create():
    logger = get_run_logger()
    articles = get_article_without_category()
    if len(articles) == 0:
        logger.info('Every article have a category')
    for article in articles:
        article=dict(article)
        find_category(article['id'], article['title'], article['description'])

if __name__ == "__main__":
    rss_category_create()
    rss_category_create.serve(
        name="category_flow",
        schedules=[
            Cron(
                "*/15 * * * *",
            )
        ]
    )
