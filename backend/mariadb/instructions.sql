------------------ Création des tables --------------------

CREATE TABLE utilisateurs (
    user_ID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    pseudo VARCHAR(100) UNIQUE,
    mail VARCHAR(255) UNIQUE,
    image VARCHAR(255),
    motdepasse VARCHAR(255),
    biographie TEXT,
    titre VARCHAR(100)
);


CREATE TABLE bieres_utilisateur (
    ID_user INT UNSIGNED,
    bieres_restantes INT DEFAULT 0,
    FOREIGN KEY (ID_user) REFERENCES utilisateurs(user_ID) ON DELETE CASCADE
);


CREATE TABLE amis (
    IDuser1 INT UNSIGNED,
    IDuser2 INT UNSIGNED,
    PRIMARY KEY (IDuser1, IDuser2),
    FOREIGN KEY (IDuser1) REFERENCES utilisateurs(user_ID) ON DELETE CASCADE,
    FOREIGN KEY (IDuser2) REFERENCES utilisateurs(user_ID) ON DELETE CASCADE
);


CREATE TABLE jeux (
    Game_ID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    date DATETIME,
    gagnant_ID INT UNSIGNED,
    bieres_en_jeu INT,
    IDuser1 INT UNSIGNED,
    IDuser2 INT UNSIGNED,
    FOREIGN KEY (gagnant_ID) REFERENCES utilisateurs(user_ID) ON DELETE SET NULL,
    FOREIGN KEY (IDuser1) REFERENCES utilisateurs(user_ID) ON DELETE CASCADE,
    FOREIGN KEY (IDuser2) REFERENCES utilisateurs(user_ID) ON DELETE CASCADE
);


CREATE TABLE niveaux (
    ID_level INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    level_name VARCHAR(100),
    min_bieres INT
);


CREATE TABLE niveau_utilisateur (
    ID_user INT UNSIGNED,
    level_ID INT UNSIGNED,
    date_obtention DATE,
    xp INT,
    PRIMARY KEY (ID_user, level_ID),
    FOREIGN KEY (ID_user) REFERENCES utilisateurs(user_ID) ON DELETE CASCADE,
    FOREIGN KEY (level_ID) REFERENCES niveaux(ID_level) ON DELETE CASCADE
);


------------------ Ajout des données de base --------------------


INSERT INTO utilisateurs (nom, prenom, pseudo, mail, image, motdepasse, biographie, titre) VALUES
('Valcke', 'Tristan', 'Trisouille', 't.valcke@students.ephec.be', 'tris.png', 'user123', 'Voici ma bio', 'Sage comme une image'),
('Preat', 'Thomas', 'TomPrt', 'thomas.preat@students.ephec.be', 'thomas.png', 'preat123', 'Toujours le sourire !', 'Le Charmeur'),
('Rocquet', 'Arnaud', 'Rocqnoob', 'arnaud.rocquet@students.ephec.be', 'arnaud.jpg', 'rocquet456', 'Master en dégustation de pils.', 'Le Stratège'),
('Doussis', 'Giorgios', 'GeoTheGreek', 'giorgios.doussis@students.ephec.be', 'giorgios.png', 'greece789', 'J’amène le soleil avec moi.', 'Le Méditerranéen'),
('Kwizera', 'Dorian', 'DKwiz', 'dorian.kwizera@students.ephec.be', 'dorian.jpg', 'kwz321', 'Toujours partant pour un défi.', 'Le Compétiteur');


------------------ Procédures et Fonctions --------------------