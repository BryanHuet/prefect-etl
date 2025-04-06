INSERT INTO article (source_id, title, link, description, content, published_at)
VALUES (?, ?, ?, ?, ?, ?)
ON CONFLICT(link) DO NOTHING