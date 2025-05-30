# ----------------- Création des tables -------------------- #

CREATE TABLE titre
(
    title_ID   INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title_name VARCHAR(100)
);

CREATE TABLE niveaux
(
    ID_level   INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title_ID   INT UNSIGNED NOT NULL,
    min_bieres INT,
    FOREIGN KEY (title_ID) REFERENCES titre (title_ID) ON DELETE CASCADE
);

CREATE TABLE utilisateurs
(
    user_ID       INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nom           VARCHAR(100),
    prenom        VARCHAR(100),
    pseudo        VARCHAR(100) UNIQUE,
    mail          VARCHAR(255) UNIQUE,
    image         VARCHAR(255),
    motdepasse    VARBINARY(60),
    biographie    TEXT,
    reserve_biere INT                   DEFAULT 10,
    biere_gagnee  INT                   DEFAULT 0,
    ID_level      INT UNSIGNED NOT NULL DEFAULT 1,
    FOREIGN KEY (ID_level) REFERENCES niveaux (ID_level) ON DELETE CASCADE
);


CREATE TABLE amis
(
    IDuser1 INT UNSIGNED NOT NULL,
    IDuser2 INT UNSIGNED NOT NULL,
    PRIMARY KEY (IDuser1, IDuser2),
    FOREIGN KEY (IDuser1) REFERENCES utilisateurs (user_ID) ON DELETE CASCADE,
    FOREIGN KEY (IDuser2) REFERENCES utilisateurs (user_ID) ON DELETE CASCADE
);


CREATE TABLE transactions
(
    transaction_ID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    debtor_ID      INT UNSIGNED NOT NULL, -- The player who owes beers
    creditor_ID    INT UNSIGNED NOT NULL, -- The player who is owed beers
    beers_owed     INT          NOT NULL, -- The number of beers owed
    settled        BOOLEAN DEFAULT FALSE, -- Whether the debt has been settled
    FOREIGN KEY (debtor_ID) REFERENCES utilisateurs (user_ID) ON DELETE CASCADE,
    FOREIGN KEY (creditor_ID) REFERENCES utilisateurs (user_ID) ON DELETE CASCADE
);

CREATE TABLE token_table
(
    user_id    INT UNSIGNED,
    token      VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES utilisateurs (user_ID)
) ENGINE = InnoDB;

# ------------------ Ajout des données de base -------------------- #

INSERT INTO titre (title_name)
VALUES ('Nouveau venu');

INSERT INTO niveaux (title_ID, min_bieres)
VALUES (1, 0);

INSERT INTO utilisateurs (nom, prenom, pseudo, mail, image, motdepasse, biographie)
VALUES ('Valcke', 'Tristan', 'Trisouille', 't.valcke@students.ephec.be',
        '"https://cdn-icons-png.flaticon.com/512/149/149071.png"',
        '$2b$12$WMwXzaY3ZQZW9/deHJeaLOz0LdLC9AkQTr8oUwEGH.CuX8Dh.8AXq', 'Voici ma bio'),
       ('Preat', 'Thomas', 'TomPrt', 'thomas.preat@students.ephec.be',
        '"https://cdn-icons-png.flaticon.com/512/149/149071.png"',
        '$2b$12$enuAKi57zLInxMWcwq9uP.RqAjqbqQ3xYdSiopqyQnN/rwySezWHu', 'Toujours le sourire !'),
       ('Roquet', 'Arnaud', 'Roqnoob', 'arnaud.roquet@students.ephec.be',
        '"https://cdn-icons-png.flaticon.com/512/149/149071.png"',
        '$2b$12$A/3DJii5iWUTQXzg.EbrCu08Vz0Txak3tvwJkJ77r8Wy4OuE/FEjC', 'Master en dégustation de pils.'),
       ('Doussis', 'Giorgios', 'GeoTheGreek', 'giorgios.doussis@students.ephec.be',
        '"https://cdn-icons-png.flaticon.com/512/149/149071.png"',
        '$2b$12$V9JBGxbPZ51brUVA4ctRk.8bFsNKNSU.KFXsee1.BJ/y31K3mGZ.e', 'J’amène le soleil avec moi.'),
       ('Kwizera', 'Dorian', 'DKwiz', 'dorian.kwizera@students.ephec.be',
        '"https://cdn-icons-png.flaticon.com/512/149/149071.png"',
        '$2b$12$obCmp53OrFY3.3UgPAOSI.HQD5o3WCfBu88r0.V.zSbGuq6sHKqWu', 'Toujours partant pour un défi.');

-- mdp :
-- Trisouille : "user123"
-- TomPrt : "preat123"
-- Roqnoob : "roquet456"
-- GeoTheGreek : "greece789"
-- DKwiz : "kwz321"