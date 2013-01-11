CREATE TABLE links (
	id              serial PRIMARY KEY,
	hash		VARCHAR(10) UNIQUE,
	link		text UNIQUE,
        created_at      timestamp DEFAULT current_timestamp
);
