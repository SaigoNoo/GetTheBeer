-- Je sais que c'est pas tout a fait comme ca dans la db mais c'est une base


CREATE FUNCTION is_friend(user_id1 INT, user_id2 INT) RETURNS BOOLEAN   --celle la est écrite avec chatgpt, à vérifier son fonctionnement
BEGIN
    DECLARE friend_count INT;
    SELECT COUNT(*) INTO friend_count FROM amis
    WHERE (userid1 = user_id1 AND userid2 = user_id2)
       OR (userid1 = user_id2 AND userid2 = user_id1);
    RETURN friend_count > 0;
END;


CREATE PROCEDURE add_friend(user_id1 INT, user_id2 INT)
BEGIN
    IF NOT (SELECT is_friend(user_id1, user_id2)) THEN
        INSERT INTO amis (userid1, userid2) VALUES (user_id1, user_id2);
    END IF;
END;


CREATE PROCEDURE delete_friend(user_id1 INT, user_id2 INT)
BEGIN
    DELETE FROM amis 
    WHERE (userid1 = user_id1 AND userid2 = user_id2)
       OR (userid1 = user_id2 AND userid2 = user_id1);
END;


CREATE FUNCTION get_user_password(username VARCHAR) RETURNS VARCHAR
BEGIN
    DECLARE user_pwd VARCHAR(255);
    SELECT mdp INTO user_pwd FROM utilisateurs WHERE pseudo = username;
    RETURN user_pwd;
END;


CREATE FUNCTION get_user_beers(user_id INT) RETURNS INT
BEGIN
    DECLARE total_beers INT;
    SELECT COALESCE(SUM(bieres), 0) INTO total_beers FROM jeux WHERE gagnant = user_id;
    RETURN total_beers;
END;


CREATE FUNCTION get_user_title(user_id INT) RETURNS VARCHAR
BEGIN
    DECLARE user_title VARCHAR(255);
    SELECT levelname INTO user_title
    FROM niveaux 
    WHERE min_bières <= (SELECT get_user_beers(user_id))
    ORDER BY min_bières DESC 
    LIMIT 1;
    RETURN user_title;
END;