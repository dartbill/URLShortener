DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
  id serial PRIMARY KEY,
  url varchar(500) NOT NULL,
  short_url varchar(50) NOT NULL
);
