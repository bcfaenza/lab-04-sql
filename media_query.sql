SELECT 
    users.username, 
    users.email, 
    posts.title, 
    posts.caption
FROM posts
JOIN users ON posts.user_id = users.user_id
WHERE posts.user_id = 1;
