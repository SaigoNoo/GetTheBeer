DELIMITER
$$

-- Fonction pour récupérer tous les utilisateurs
DROP FUNCTION IF EXISTS get_all_users$$

CREATE FUNCTION get_all_users()
    RETURNS LONGTEXT
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
                           'biographie', biographie,
                           'titre', titre
                       )
               )
    INTO result
    FROM utilisateurs;

    RETURN result;
END$$

-- Fonction pour récupérer le mot de passe
DROP FUNCTION IF EXISTS get_user_password$$

CREATE FUNCTION get_user_password(username VARCHAR(100))
    RETURNS VARCHAR(255)
    DETERMINISTIC
BEGIN
    DECLARE
        user_pwd VARCHAR(255);

    SELECT motdepasse
    INTO user_pwd
    FROM utilisateurs
    WHERE pseudo = username;

    RETURN user_pwd;
END$$

-- Procédure pour ajouter un utilisateur
DROP PROCEDURE IF EXISTS add_user$$

CREATE PROCEDURE add_user(
    IN p_nom VARCHAR(100),
    IN p_prenom VARCHAR(100),
    IN p_pseudo VARCHAR(100),
    IN p_mail VARCHAR(255),
    IN p_image VARCHAR(255),
    IN p_motdepasse VARCHAR(255),
    IN p_biographie TEXT,
    IN p_titre VARCHAR(100)
)
BEGIN
    INSERT INTO utilisateurs (nom, prenom, pseudo, mail, image, motdepasse, biographie, titre)
    VALUES (p_nom, p_prenom, p_pseudo, p_mail, p_image, p_motdepasse, p_biographie, p_titre);
END$$

-- Procédure pour update un mot de passe
DROP PROCEDURE IF EXISTS update_password_by_token$$

CREATE PROCEDURE `update_password_by_token`(IN `p_token` VARCHAR(255), IN `p_nouveau_mdp` VARCHAR(255))
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
-- Procédure pour ajouter un token
DROP PROCEDURE IF EXISTS token_reset$$
CREATE PROCEDURE token_reset(
    IN p_user INT,
    IN p_token VARCHAR(255)
)
BEGIN
    INSERT INTO token_table (user_id, token, created_at)
    VALUES (p_user, p_token, CURRENT_TIMESTAMP);
END$$

-- Fonction pour check si data_reset_exist
DROP FUNCTION IF EXISTS have_reset_token$$

CREATE FUNCTION have_reset_token(uid INT) RETURNS TINYINT
BEGIN
    DECLARE
        result TINYINT;

    SELECT EXISTS (SELECT 1
                   FROM token_table
                   WHERE user_id = uid)
    INTO result;

    RETURN result;
END$$


-- Si pas déjà activé
SET GLOBAL event_scheduler = "ON";

-- Event : suppression des tokens vieux de 15 minutes
DROP EVENT IF EXISTS `delete_old_tokens`;

CREATE
    EVENT `delete_old_tokens` ON SCHEDULE EVERY 1 MINUTE ON COMPLETION NOT PRESERVE ENABLE DO
    DELETE
    FROM token_table
    WHERE created_at < NOW() - INTERVAL 15 MINUTE
DELIMITER;
