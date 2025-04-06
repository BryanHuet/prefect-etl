 SELECT article.*
 FROM article
 LEFT JOIN article_category
 ON article.id = article_category.article_id
 WHERE article_category.article_id IS NULL
 ORDER by article.id
 LIMIT 10;