from prefect import task, get_run_logger
from google import genai
from utils.utils import  get_db_connection, get_sql_file
import os
def is_one_word(texte: str) -> bool:
    texte = texte.strip()

    # Diviser le texte en mots
    mots = texte.split()

    # Vérifie si le texte contient entre 1 et 5 mots
    return 1 <= len(mots) <= 5 and all(mot.isalpha() for mot in mots)


@task
def get_article_without_category():
    conn = get_db_connection(True)

    cursor = conn.cursor()
    cursor.execute(
        get_sql_file('rss/data/queries/select/article_without_category.sql')
    )
    articles = cursor.fetchall()

    conn.commit()
    conn.close()
    return articles

@task
def find_category(article_id, title, description):
    logger = get_run_logger()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        get_sql_file('rss/data/queries/select/category_names.sql')
    )
    categories = cursor.fetchall()
    categories = ", ".join(cat[0] for cat in categories)

    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

    query = "Using the title : \"" + title + "\" and the description \""+description+"\", select the most relevant category from "+categories+" if one matches over 90%; otherwise, create a new one. Translated it in french and return only the category nothing else."

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=(query)
    )

    category = response.text
    logger.info(category)
    if is_one_word(category):
        cursor.execute(
            get_sql_file('rss/data/queries/select/category_id.sql'),
            (category,)
        )
        category_id = cursor.fetchone()
        logger.info('from select '+str(category_id))

        if category_id == '' or category_id == None:
            cursor.execute(
                get_sql_file('rss/data/queries/insert/category.sql'),
                (category,)
            )
            category_id = cursor.lastrowid
            logger.info('from insert '+str(category_id))
        else:
            category_id = category_id[0]

        logger.info(category_id)
        cursor.execute(
            get_sql_file('rss/data/queries/insert/article_category.sql'),
            (article_id, category_id)
        )

    conn.commit()
    conn.close()