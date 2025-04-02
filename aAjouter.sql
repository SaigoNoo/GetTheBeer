-- Je sais que c'est pas tout a fait comme ca dans la db mais c'est une base


CREATE FUNCTION is_friend(id INT, friend_id INT) RETURNS INT AS $$
DECLARE 
    friend_count INT;
BEGIN
    SELECT COUNT(*) INTO friend_count 
    FROM friends 
    WHERE (user_id = id AND friend_id = friend_id) 
       OR (user_id = friend_id AND friend_id = id);
    
    RETURN friend_count;
END;



CREATE PROCEDURE add_friend(user_id INT, friend_id INT) AS $$
BEGIN
    INSERT INTO friends (user_id, friend_id) VALUES (user_id, friend_id), (friend_id, user_id);
END;


CREATE PROCEDURE delete_friend(IN user_id INT, IN friend_id INT)
BEGIN
    DELETE FROM friends WHERE (user_id = user_id AND friend_id = friend_id) 
                           OR (user_id = friend_id AND friend_id = user_id);
END;



CREATE FUNCTION get_user_password(username TEXT) RETURNS TEXT AS $$
DECLARE 
    user_pass TEXT;
BEGIN
    SELECT password INTO user_pass FROM users WHERE users.username = username;
    RETURN user_pswd;
END;



CREATE FUNCTION is_friend(id INT, friend_id INT) RETURNS INT AS $$
DECLARE 
    friend_count INT;
BEGIN
    SELECT COUNT(*) INTO friend_count FROM friends WHERE (user_id = id AND friend_id = friend_id) OR (user_id = friend_id AND friend_id = id);
    RETURN friend_count;
END;