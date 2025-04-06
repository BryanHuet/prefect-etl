from utils.utils import  get_db_connection, get_sql_file
from prefect import task

@task
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        get_sql_file('rss/data/tables/source.sql')
    )

    cursor.execute(
        get_sql_file('rss/data/tables/article.sql')
    )

    cursor.execute(
        get_sql_file('rss/data/tables/category.sql')
    )

    cursor.execute(
        get_sql_file('rss/data/tables/article_category.sql')
    )

    conn.commit()
    conn.close()