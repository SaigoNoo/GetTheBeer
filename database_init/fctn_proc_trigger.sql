DELIMITER $$

--
-- OBTENIR LES USERS
--

DROP FUNCTION IF EXISTS get_all_users$$

CREATE FUNCTION `get_all_users`() RETURNS longtext
    DETERMINISTIC
BEGIN
    DECLARE result LONGTEXT;

    SELECT JSON_ARRAYAGG(
                   JSON_OBJECT(
                           'user_ID', user_ID,
                           'nom', nom,
                           'prenom', prenom,
                           'pseudo', pseudo,
                           'mail', mail,
                           'image', image,
                           'biographie', biographie
                       )
               )
    INTO result
    FROM utilisateurs;

    RETURN result;
END$$

--
-- RECUP LE MOT DE PASSE HASHE
--

DROP FUNCTION IF EXISTS get_user_password$$

CREATE FUNCTION get_user_password(username VARCHAR(100))
    RETURNS VARCHAR(255)
        CHARACTER SET utf8mb4
            COLLATE utf8mb4_general_ci
    DETERMINISTIC
BEGIN
    DECLARE user_pwd VARCHAR(255);

    SELECT motdepasse
    INTO user_pwd
    FROM utilisateurs
    WHERE pseudo = username
       OR mail = username;

    RETURN user_pwd;
END$$

--
-- AJOUTER UN USER DANS LA DB
--
DROP PROCEDURE IF EXISTS add_user$$

CREATE PROCEDURE `add_user`(IN `name` VARCHAR(100), IN `first_name` VARCHAR(100),
                            IN `username` VARCHAR(100), IN `email` VARCHAR(255),
                            IN `picture` VARCHAR(255), IN `hashed_password` VARCHAR(255),
                            IN `bio` TEXT)
BEGIN
    INSERT INTO utilisateurs (nom, prenom, pseudo, mail, image, motdepasse, biographie)
    VALUES (name, first_name, username, email, picture, hashed_password, bio);
END$$

--
-- RESET LE MOT DE PASSE SI LE TOKEN EST LE BON
--
DROP PROCEDURE IF EXISTS update_password_by_token$$

CREATE PROCEDURE update_password_by_token(
    IN p_token VARCHAR(255),
    IN p_nouveau_mdp VARCHAR(255)
)
BEGIN
    DECLARE v_user_id INT;

    SELECT user_id
    INTO v_user_id
    FROM token_table
    WHERE token = p_token
    LIMIT 1;

    IF v_user_id IS NOT NULL THEN
        UPDATE utilisateurs
        SET motdepasse = p_nouveau_mdp
        WHERE user_ID = v_user_id;
    END IF;
END$$

--
-- AJOUTER UNE INSTANCE DE RESET VIA TOKEN
--
DROP PROCEDURE IF EXISTS token_reset$$

CREATE PROCEDURE token_reset(
    IN p_user INT,
    IN p_token VARCHAR(255)
)
BEGIN
    INSERT INTO token_table (user_id, token, created_at)
    VALUES (p_user, p_token, CURRENT_TIMESTAMP);
END$$

--
-- MON RESET EST TOUJOURS SOUS TOKEN ?
--
DROP FUNCTION IF EXISTS have_reset_token$$

CREATE FUNCTION have_reset_token(uid INT)
    RETURNS TINYINT
    DETERMINISTIC
BEGIN
    DECLARE result TINYINT;

    SELECT EXISTS (SELECT 1
                   FROM token_table
                   WHERE user_id = uid)
    INTO result;

    RETURN result;
END$$

--
-- IMPORTANT
--
-- Activer le scheduler si ce n'est pas déjà fait
-- Événement : suppression des tokens vieux de plus de 15 minutes
DROP EVENT IF EXISTS delete_old_tokens$$

CREATE EVENT delete_old_tokens
    ON SCHEDULE EVERY 1 MINUTE
    ON COMPLETION NOT PRESERVE
    ENABLE
    DO
    DELETE
    FROM token_table
    WHERE created_at < NOW() - INTERVAL 15 MINUTE$$

--
-- SONT ILS AMIS ?
--
DROP FUNCTION IF EXISTS is_friend$$

CREATE FUNCTION `is_friend`(`user_id1` INT, `user_id2` INT) RETURNS tinyint(1)
    DETERMINISTIC
BEGIN
    RETURN EXISTS (SELECT 1
                   FROM amis
                   WHERE (IDuser1 = user_id1 AND IDuser2 = user_id2)
                      OR (IDuser1 = user_id2 AND IDuser2 = user_id1));
END$$

--
-- CREER UNE RELATION AMI
--
DROP PROCEDURE IF EXISTS add_friend$$

CREATE PROCEDURE `add_friend`(IN `user_id1` INT, IN `user_id2` INT)
BEGIN
    IF NOT is_friend(user_id1, user_id2) THEN
        INSERT INTO amis (IDuser1, IDuser2)
        VALUES (user_id1, user_id2);
    END IF;
END$$

--
-- SUPPRIMER UNE RELATION AMIS
--
DROP PROCEDURE IF EXISTS delete_friend$$

CREATE PROCEDURE `delete_friend`(IN `user_id1` INT, IN `user_id2` INT)
BEGIN
    IF is_friend(user_id1, user_id2) THEN
        DELETE
        FROM amis
        WHERE (IDuser1 = user_id1 AND IDuser2 = user_id2)
           OR (IDuser1 = user_id2 AND IDuser2 = user_id1);
    END IF;
END$$

--
-- VOIR LES BIERES DUES
--
DROP FUNCTION IF EXISTS get_user_beer_reserve$$

CREATE FUNCTION get_user_beer_reserve(uid INT)
    RETURNS INT
    NOT DETERMINISTIC
    READS SQL DATA
BEGIN
    DECLARE result INT;

    SELECT reserve_biere
    INTO result
    FROM utilisateurs
    WHERE user_ID = uid;

    RETURN result;
END$$

--
-- MODIFIER LA QTE DE BIERES D'UN USER
--

DROP PROCEDURE IF EXISTS do_beer_transaction$$

CREATE PROCEDURE do_beer_transaction(IN uid INT, IN beer INT)
BEGIN
    UPDATE utilisateurs
    SET reserve_biere = reserve_biere - beer
    WHERE user_ID = uid;
END$$

--
-- VOIR LES BEERS D'UN UTILISATEUR
--

DROP FUNCTION IF EXISTS how_many_beer$$

CREATE FUNCTION how_many_beer(uid INT)
    RETURNS INT
    DETERMINISTIC
    READS SQL DATA
BEGIN
    DECLARE beers INT;
    SELECT reserve_biere INTO beers FROM utilisateurs WHERE user_ID = uid;
    RETURN beers;
END$$
--
DROP PROCEDURE IF EXISTS add_transaction$$


CREATE PROCEDURE add_transaction(
    IN looser_uid INT,
    IN winner_uid INT,
    IN beers_owed INT
)
BEGIN
    INSERT INTO transactions(debtor_ID, creditor_ID, beers_owed)
    VALUES (looser_uid, winner_uid, beers_owed);
END$$

-- Fonction pour récupérer le total de bières gagnées par un utilisateur
DROP FUNCTION IF EXISTS get_user_beers$$

CREATE FUNCTION get_user_beers(user_id INT)
    RETURNS INT
    DETERMINISTIC
BEGIN
    DECLARE total_beers INT;

    SELECT COALESCE(SUM(bieres), 0)
    INTO total_beers
    FROM jeux
    WHERE gagnant = user_id;

    RETURN total_beers;
END$$


-- Fonction pour récupérer le titre d'un utilisateur en fonction de ses bières
DROP FUNCTION IF EXISTS get_user_title$$

CREATE FUNCTION get_user_title(user_id INT)
    RETURNS VARCHAR(255)
    DETERMINISTIC
BEGIN
    DECLARE user_title VARCHAR(255);

    SELECT levelname
    INTO user_title
    FROM niveaux
    WHERE min_bières <= (SELECT get_user_beers(user_id))
    ORDER BY min_bières DESC
    LIMIT 1;

    RETURN user_title;
END$$

-- Fonction pour savoir si il reste assez de bieres a decompter
DROP FUNCTION IF EXISTS has_enough_beer$$


CREATE FUNCTION `has_enough_beer`(`uid` INT, `beers_count` INT) RETURNS int(11)
BEGIN
    DECLARE beers INT;

    SELECT reserve_biere INTO beers FROM utilisateurs WHERE user_ID = uid;

    IF beers - beers_count >= 0 THEN
        RETURN 1;
    ELSE
        RETURN 0;
    END IF;
END$$

-- GET TOKEN OWNER ID
DROP FUNCTION IF EXISTS get_token_owner_id$$


CREATE FUNCTION `get_token_owner_id`(p_token VARCHAR(255)) RETURNS TINYINT(4)
    DETERMINISTIC
BEGIN
    DECLARE result TINYINT;

    SELECT user_id
    INTO result
    FROM token_table
    WHERE token = p_token;

    RETURN result;
END$$

-- GET TOKEN OWNER ID
DROP FUNCTION IF EXISTS get_friends$$

CREATE FUNCTION `get_friends`(user_id INT) RETURNS longtext CHARSET utf8mb4 COLLATE utf8mb4_general_ci
    DETERMINISTIC
BEGIN
    DECLARE result LONGTEXT;

    SELECT JSON_ARRAYAGG(
                   JSON_OBJECT(
                           'user_ID', utilisateurs.user_ID,
                           'nom', utilisateurs.nom,
                           'prenom', utilisateurs.prenom,
                           'pseudo', utilisateurs.pseudo,
                           'image', utilisateurs.image
                       )
               )
    INTO result
    FROM amis
             INNER JOIN utilisateurs ON amis.IDuser2 = utilisateurs.user_ID
    WHERE amis.IDuser1 = user_id;

    RETURN result;
END$$

DELIMITER ;
