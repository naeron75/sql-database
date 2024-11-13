CREATE DATABASE IF NOT EXISTS summer_olympics;

USE summer_olympics;

DROP TABLE IF EXISTS medalists;

CREATE TABLE medalists (
id INT AUTO_INCREMENT PRIMARY KEY,
medal_type VARCHAR(10),
athlete_country VARCHAR(50),
host_country VARCHAR(20),
game_year INT
);