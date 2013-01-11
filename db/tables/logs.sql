CREATE TABLE logs (
        id              serial PRIMARY KEY,
	link		integer NOT NULL references links(id),
	ip		text,
	redirect	text,
	browser		text,
	created_at      timestamp DEFAULT current_timestamp
);
