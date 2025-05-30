DELIMITER $$

-- SUPPRIMER LES PROCEDURES SI ELLES EXISTENT
DROP PROCEDURE IF EXISTS `add_friend` $$
DROP PROCEDURE IF EXISTS `add_transaction` $$
DROP PROCEDURE IF EXISTS `add_user` $$
DROP PROCEDURE IF EXISTS `delete_friend` $$
DROP PROCEDURE IF EXISTS `do_beer_transaction` $$
DROP PROCEDURE IF EXISTS `token_reset` $$
DROP PROCEDURE IF EXISTS `update_password_by_token` $$

-- AJOUTER DES AMIS
CREATE PROCEDURE `add_friend`(IN `user_id1` INT, IN `user_id2` INT)
BEGIN
    IF NOT is_friend(user_id1, user_id2) THEN
        INSERT INTO amis (IDuser1, IDuser2)
        VALUES (user_id1, user_id2);
    END IF;
END $$

-- CREER UNE TRANSACTION
CREATE PROCEDURE `add_transaction`(
    IN looser_uid INT,
    IN winner_uid INT,
    IN beers_owed INT
)
BEGIN
    INSERT INTO transactions(debtor_ID, creditor_ID, beers_owed)
    VALUES (looser_uid, winner_uid, beers_owed);
END $$

-- FAIRE UNE TRANSACTION DE BIERE
CREATE PROCEDURE `do_beer_transaction`(IN `w_uid` INT, IN `l_uid` INT, IN `beer` INT)
BEGIN
    UPDATE utilisateurs
    SET reserve_biere = reserve_biere - beer
    WHERE user_ID = l_uid;

    UPDATE utilisateurs
    SET biere_gagnee = biere_gagnee + beer
    WHERE user_ID = w_uid;
END $$

-- AJOUTER UN UTILISATEUR
CREATE PROCEDURE `add_user`(
    IN `name` VARCHAR(100),
    IN `first_name` VARCHAR(100),
    IN `username` VARCHAR(100),
    IN `email` VARCHAR(255),
    IN `picture` VARCHAR(255),
    IN `hashed_password` VARCHAR(255),
    IN `bio` TEXT
)
BEGIN
    INSERT INTO utilisateurs (nom, prenom, pseudo, mail, image, motdepasse, biographie)
    VALUES (name, first_name, username, email, picture, hashed_password, bio);
END $$

-- SUPPRIMER UN AMI
CREATE PROCEDURE `delete_friend`(IN `user_id1` INT, IN `user_id2` INT)
BEGIN
    IF is_friend(user_id1, user_id2) THEN
        DELETE
        FROM amis
        WHERE (IDuser1 = user_id1 AND IDuser2 = user_id2)
           OR (IDuser1 = user_id2 AND IDuser2 = user_id1);
    END IF;
END $$

-- RESET TOKEN
CREATE PROCEDURE token_reset(
    IN p_user INT,
    IN p_token VARCHAR(255)
)
BEGIN
    INSERT INTO token_table (user_id, token, created_at)
    VALUES (p_user, p_token, CURRENT_TIMESTAMP);
END $$

-- UPDATE MOT DE PASSE PAR TOKEN
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
END $$

DELIMITER ;
