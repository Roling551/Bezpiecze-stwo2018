DROP TABLE IF EXISTS transfer;

DROP TABLE IF EXISTS users;

CREATE TABLE users(
id INT  NOT NULL  AUTO_INCREMENT, 
login VARCHAR(50)  NOT NULL,
password VARCHAR(50) NOT NULL,
email VARCHAR(100) NOT NULL,
isAdmin BOOLEAN NOT NULL  DEFAULT FALSE,
funds DECIMAL(15,2) NOT NULL DEFAULT 0.00,
confirmed BOOLEAN NOT NULL DEFAULT FALSE,
confirmed_salt TEXT,
confirmed_sent BOOLEAN NOT NULL DEFAULT  FALSE,
reset_salt TEXT,
reset_sent BOOLEAN NOT NULL DEFAULT  FALSE,
PRIMARY KEY (id),
UNIQUE(login),
UNIQUE(email)
);

DROP TABLE IF EXISTS transfers;

CREATE TABLE transfers(
title VARCHAR(100) NOT NULL,
sender INT NOT NULL,
receiver INT NOT NULL,
amount DECIMAL(15,2),
confirmed BOOLEAN NOT NULL DEFAULT FALSE,
realised BOOLEAN NOT NULL DEFAULT FALSE,
description VARCHAR(200) NOT NULL DEFAULT '',
PRIMARY KEY (title),
FOREIGN KEY (sender) REFERENCES users(id),
FOREIGN KEY (receiver) REFERENCES users(id)
);


INSERT INTO users(login, password, email) VALUES ("user1","pass","mail@gmail.com");
UPDATE users SET funds = funds + 100.00 WHERE login = 'user1';
INSERT INTO users(login, password, email) VALUES ("userAdmin","pass","mailAdmin@gmail.com");
UPDATE users SET isAdmin = TRUE WHERE login = 'userAdmin';
INSERT INTO transfers(amount, sender, receiver) VALUES (10.0,1,2)
UPDATE users SET confirmed=TRUE WHERE email='a'