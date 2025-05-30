DELIMITER $$

-- SUPPRIMER LES PROCEDURES SI ELLES EXISTENT
DROP FUNCTION IF EXISTS `beers_bet` $$
DROP FUNCTION IF EXISTS `count_games` $$
DROP FUNCTION IF EXISTS `get_all_users` $$
DROP FUNCTION IF EXISTS `get_friends` $$
DROP FUNCTION IF EXISTS `get_loose_beer` $$
DROP FUNCTION IF EXISTS `get_token_owner_id` $$
DROP FUNCTION IF EXISTS `get_user_beer_reserve` $$
DROP FUNCTION IF EXISTS `get_user_password` $$
DROP FUNCTION IF EXISTS `get_user_title` $$
DROP FUNCTION IF EXISTS `get_win_beer` $$
DROP FUNCTION IF EXISTS `has_enough_beer` $$
DROP FUNCTION IF EXISTS `have_reset_token` $$
DROP FUNCTION IF EXISTS `is_friend` $$

-- COMPTER LES BIERES PARIEES
CREATE FUNCTION `beers_bet`(user_id INT) RETURNS INT
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE
        total_beted INT;
    SELECT SUM(beers_owed)
    INTO total_beted
    FROM transactions
    WHERE debtor_ID = user_id
       OR creditor_ID = user_id;
    RETURN IFNULL(total_beted, 0);
END$$

-- COMPTER LES PARTIES JOUEES
CREATE FUNCTION `count_games`(user_id INT) RETURNS INT
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE
        games_count INT;
    SELECT COUNT(transaction_ID)
    INTO games_count
    FROM transactions
    WHERE debtor_ID = user_id
       OR creditor_ID = user_id;
    RETURN games_count;
END$$

-- AFFICHER TOUS LES MEMBRES
CREATE FUNCTION `get_all_users`() RETURNS LONGTEXT
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE
        result LONGTEXT;
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

-- LISTER LES AMIS
CREATE FUNCTION `get_friends`(user_id INT) RETURNS LONGTEXT
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE
        result LONGTEXT;
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

-- AFFICHER LES BIERES PERDUES
CREATE FUNCTION `get_loose_beer`(user_id INT) RETURNS INT
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE
        total_beers INT;
    SELECT SUM(beers_owed)
    INTO total_beers
    FROM transactions
    WHERE debtor_ID = user_id;
    RETURN IFNULL(total_beers, 0);
END$$

-- AFFICHER LE PROPRIO D'UN TOKEN RESET
CREATE FUNCTION `get_token_owner_id`(p_token VARCHAR(255)) RETURNS TINYINT
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE
        result TINYINT;
    SELECT user_id
    INTO result
    FROM token_table
    WHERE token = p_token;
    RETURN result;
END$$

-- AFFICHER LA RESERVE DE BIERES
CREATE FUNCTION `get_user_beer_reserve`(uid INT) RETURNS INT
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE
        result INT;
    SELECT reserve_biere
    INTO result
    FROM utilisateurs
    WHERE user_ID = uid;
    RETURN result;
END$$

-- OBTENIR LE MOT DE PASSE USER
CREATE FUNCTION `get_user_password`(username VARCHAR(100)) RETURNS VARCHAR(255)
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE
        user_pwd VARCHAR(255);
    SELECT motdepasse
    INTO user_pwd
    FROM utilisateurs
    WHERE pseudo = username
       OR mail = username;
    RETURN user_pwd;
END$$

-- AFFICHER LE TITRE D'UN USER
CREATE FUNCTION `get_user_title`(user_id INT) RETURNS VARCHAR(255)
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE
        user_title VARCHAR(255);
    SELECT levelname
    INTO user_title
    FROM niveaux
    WHERE min_bières <= (SELECT get_user_beer_reserve(user_id))
    ORDER BY min_bières DESC
    LIMIT 1;
    RETURN user_title;
END$$

-- AFFICHER LES BIERES GAGNEES
CREATE FUNCTION `get_win_beer`(user_id INT) RETURNS INT
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE
        total_beers INT;
    SELECT SUM(beers_owed)
    INTO total_beers
    FROM transactions
    WHERE creditor_ID = user_id;
    RETURN IFNULL(total_beers, 0);
END$$

-- A ASSEZ DE BIERES
CREATE FUNCTION `has_enough_beer`(uid INT, beers_count INT) RETURNS INT
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE
        beers INT;
    SELECT reserve_biere
    INTO beers
    FROM utilisateurs
    WHERE user_ID = uid;
    IF
        beers - beers_count >= 0 THEN
        RETURN 1;
    ELSE
        RETURN 0;
    END IF;
END$$

-- A UN RESET TOKEN
CREATE FUNCTION `have_reset_token`(uid INT) RETURNS TINYINT
    READS SQL DATA
    DETERMINISTIC
BEGIN
    DECLARE
        result TINYINT;
    SELECT EXISTS (SELECT 1
                   FROM token_table
                   WHERE user_id = uid)
    INTO result;
    RETURN result;
END$$

-- SONT AMIS
CREATE FUNCTION `is_friend`(user_id1 INT, user_id2 INT) RETURNS TINYINT
    READS SQL DATA
    DETERMINISTIC
BEGIN
    RETURN EXISTS (SELECT 1
                   FROM amis
                   WHERE (IDuser1 = user_id1 AND IDuser2 = user_id2)
                      OR (IDuser1 = user_id2 AND IDuser2 = user_id1));
END$$

DELIMITER ;
