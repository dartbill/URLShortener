DROP TABLE IF EXISTS cars;

CREATE TABLE cars (
  id serial PRIMARY KEY,
  name varchar(50) NOT NULL,
  model varchar(50) NOT NULL,
  doors int NOT NULL
);
