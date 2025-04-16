-- Création des tables dans l'ordre logique

CREATE TABLE IF NOT EXISTS titre (
    title_ID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title_name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS niveaux (
    ID_level INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title_ID INT UNSIGNED NOT NULL,
    min_bieres INT,
    FOREIGN KEY (title_ID) REFERENCES titre(title_ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS utilisateurs (
    user_ID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    pseudo VARCHAR(100) UNIQUE,
    mail VARCHAR(255) UNIQUE,
    image VARCHAR(255),
    motdepasse VARCHAR(255),
    biographie TEXT,
    reserve_biere INT DEFAULT 0,
    biere_gagnee INT DEFAULT 0,
    ID_level INT UNSIGNED NOT NULL,
    FOREIGN KEY (ID_level) REFERENCES niveaux(ID_level) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS amis (
    IDuser1 INT UNSIGNED NOT NULL,
    IDuser2 INT UNSIGNED NOT NULL,
    PRIMARY KEY (IDuser1, IDuser2),
    FOREIGN KEY (IDuser1) REFERENCES utilisateurs(user_ID) ON DELETE CASCADE,
    FOREIGN KEY (IDuser2) REFERENCES utilisateurs(user_ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS jeux (
    Game_ID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    date DATETIME,
    gagnant_ID INT UNSIGNED NOT NULL,
    bieres_en_jeu INT,
    FOREIGN KEY (gagnant_ID) REFERENCES utilisateurs(user_ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS duel (
    user_ID INT UNSIGNED NOT NULL,
    Game_ID INT UNSIGNED NOT NULL,
    PRIMARY KEY (user_ID, Game_ID),
    FOREIGN KEY (user_ID) REFERENCES utilisateurs(user_ID) ON DELETE CASCADE,
    FOREIGN KEY (Game_ID) REFERENCES jeux(Game_ID) ON DELETE CASCADE
);

-- Insertion de base
INSERT INTO titre (title_name) VALUES ('Nouveau venu');
INSERT INTO niveaux (title_ID, min_bieres) VALUES (1, 0);

-- Utilisateurs
INSERT INTO utilisateurs (nom, prenom, pseudo, mail, image, motdepasse, biographie, ID_level) VALUES
('Valcke', 'Tristan', 'Trisouille', 't.valcke@students.ephec.be', 'tris.png', 'user123', 'Voici ma bio', 1),
('Preat', 'Thomas', 'TomPrt', 'thomas.preat@students.ephec.be', 'thomas.png', 'preat123', 'Toujours le sourire !', 1),
('Roquet', 'Arnaud', 'Roqnoob', 'arnaud.roquet@students.ephec.be', 'arnaud.jpg', 'roquet456', 'Master en dégustation de pils.', 1),
('Doussis', 'Giorgios', 'GeoTheGreek', 'giorgios.doussis@students.ephec.be', 'giorgios.png', 'greece789', 'J’amène le soleil avec moi.', 1),
('Kwizera', 'Dorian', 'DKwiz', 'dorian.kwizera@students.ephec.be', 'dorian.jpg', 'kwz321', 'Toujours partant pour un défi.', 1);


-- Ajout manuel des relations d’amitié réussies
INSERT INTO amis (IDuser1, IDuser2) VALUES
(1, 2),
(1, 3),
(2, 4),
(3, 5);