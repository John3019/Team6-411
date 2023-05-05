DROP DATABASE IF EXISTS spotafriend;
CREATE DATABASE spotafriend;
USE spotafriend;

CREATE TABLE User (
  id VARCHAR(255) PRIMARY KEY,
  token VARCHAR(255),
  top_song VARCHAR(255),
  top_artist VARCHAR(255),
  last_login DATE,
  quote TEXT
);

SELECT * FROM User;

b4b4eicve0rnv3gnnsduw0md9