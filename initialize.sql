DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

CREATE TABLE users(
	user_id INT PRIMARY KEY,
	username VARCHAR(30),
	email VARCHAR(40),
	age INT,
	created_at DATETIME
);

CREATE TABLE posts(
	post_id INT PRIMARY KEY,
	user_id INT,
	title VARCHAR(100),
	caption TEXT,
	posted_at DATETIME,
	FOREIGN KEY (user_id) REFERENCES users(user_id)
);

INSERT INTO users VALUES (1, 'kate', 'kate@gmail.com', 25, '2026-01-01 10:00:00');
INSERT INTO users VALUES (2, 'lily', 'lily@gmail.com', 22, '2026-01-15 10:00:00');
INSERT INTO users VALUES (3, 'jack', 'jack@gmail.com', 21, '2026-01-20 10:00:00');
INSERT INTO users VALUES (4, 'hunter', 'hunter@gmail.com', 22, '2026-02-02 10:00:00');
INSERT INTO users VALUES (5, 'aelin', 'aelin@gmail.com', 21, '2026-02-09 11:00:00');
INSERT INTO users VALUES (6, 'mary', 'mary@gmail.com', 26, '2026-02-28 10:00:00');
INSERT INTO users VALUES (7, 'aaron', 'aaron@gmail.com', 19, '2026-03-025 12:00:00');
INSERT INTO users VALUES (8, 'vivian', 'vivian@gmail.com', 20, '2026-04-04 11:00:00');
INSERT INTO users VALUES (9, 'willow', 'willow@gmail.com', 17, '2026-04-13 09:00:00');
INSERT INTO users VALUES (10, 'sarah', 'sarah@gmail.com', 18, '2026-05-17 04:00:00');

INSERT INTO posts VALUES(1, 1, 'My First Post', 'Look at my cute puppy', '2026-02-02 10:05:00');
INSERT INTO posts VALUES(2, 1, 'My Second Post', 'Here is an update on my puppy', '2026-03-02 10:05:00'); 
INSERT INTO posts VALUES(3, 2, 'First Post!', 'hi everyone', '2026-03-02 10:05:00');
INSERT INTO posts VALUES(4, 3, 'New Post', 'whats up guys', '2026-04-05 10:05:00');
INSERT INTO posts VALUES(5, 4, 'Introduction', 'my name is hunter', '2026-04-07 10:05:00');
INSERT INTO posts VALUES(6, 5, 'Hello', 'Look at this cool puzzle', '2026-05-09 10:05:00');
INSERT INTO posts VALUES(7, 6, 'Aarons post', 'this is my grandmas cat', '2026-05-12 10:05:00');
INSERT INTO posts VALUES(8, 7, 'First Post', 'Look at my cute lizard', '2026-06-14 10:05:00');
INSERT INTO posts VALUES(9, 8, 'a new post', 'I love my bunnies', '2026-06-15 10:05:00');
INSERT INTO posts VALUES(10, 9, 'post from willow', 'Look at kates cute puppy', '2026-06-20 10:05:00');
INSERT INTO posts VALUES(11, 10, 'My First Post', 'Look at aarons cute lizard', '2026-07-02 10:05:00');
