-- Je sais que c'est pas tout à fait comme ça dans la DB mais c'est une base

DELIMITER //

DROP FUNCTION IF EXISTS is_friend;
//
CREATE FUNCTION is_friend(user_id1 INT, user_id2 INT) RETURNS BOOLEAN
DETERMINISTIC
BEGIN
    DECLARE friend_count INT;
    SELECT COUNT(*) INTO friend_count FROM amis
    WHERE (IDuser1 = user_id1 AND IDuser2 = user_id2)
       OR (IDuser1 = user_id2 AND IDuser2 = user_id1);
    RETURN friend_count > 0;
END;
//

DROP FUNCTION IF EXISTS get_all_users;
//
CREATE FUNCTION get_all_users() RETURNS JSON
DETERMINISTIC
BEGIN
    RETURN (
        SELECT JSON_ARRAYAGG(
            JSON_OBJECT(
                'user_ID', u.user_ID,
                'nom', u.nom,
                'prenom', u.prenom,
                'pseudo', u.pseudo,
                'mail', u.mail,
                'image', u.image,
                'biographie', u.biographie,
                'titre', t.title_name
            )
        )
        FROM utilisateurs u
        JOIN niveaux n ON u.ID_level = n.ID_level
        JOIN titre t ON n.title_ID = t.title_ID
    );
END;
//

DROP PROCEDURE IF EXISTS add_friend;
//
CREATE PROCEDURE add_friend(user_id1 INT, user_id2 INT)
BEGIN
    IF NOT (SELECT is_friend(user_id1, user_id2)) THEN
        INSERT INTO amis (IDuser1, IDuser2) VALUES (user_id1, user_id2);
    END IF;
END;
//

DROP PROCEDURE IF EXISTS delete_friend;
//
CREATE PROCEDURE delete_friend(user_id1 INT, user_id2 INT)
BEGIN
    DELETE FROM amis 
    WHERE (IDuser1 = user_id1 AND IDuser2 = user_id2)
       OR (IDuser1 = user_id2 AND IDuser2 = user_id1);
END;
//

DROP FUNCTION IF EXISTS get_user_password;
//
CREATE FUNCTION get_user_password(username VARCHAR(255)) RETURNS VARCHAR(255)
DETERMINISTIC
BEGIN
    DECLARE user_pwd VARCHAR(255);
    SELECT motdepasse INTO user_pwd FROM utilisateurs WHERE pseudo = username;
    RETURN user_pwd;
END;
//

DROP FUNCTION IF EXISTS get_user_beers;
//
CREATE FUNCTION get_user_beers(user_id INT) RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE total_beers INT;
    SELECT COALESCE(SUM(biere_gagnee), 0) INTO total_beers FROM utilisateurs WHERE user_ID = user_id;
    RETURN total_beers;
END;
//

DROP FUNCTION IF EXISTS get_user_title;
//
CREATE FUNCTION get_user_title(user_id INT) RETURNS VARCHAR(255)
DETERMINISTIC
BEGIN
    DECLARE user_title VARCHAR(255);
    SELECT t.title_name INTO user_title
    FROM utilisateurs u
    JOIN niveaux n ON u.ID_level = n.ID_level
    JOIN titre t ON n.title_ID = t.title_ID
    WHERE u.user_ID = user_id;
    RETURN user_title;
END;
//

DELIMITER ;
