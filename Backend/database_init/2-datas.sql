# ------------------ Ajout des données de base -------------------- #

INSERT INTO titre (title_name)
VALUES ('Nouveau venu');

INSERT INTO niveaux (title_ID, min_bieres)
VALUES (1, 0);

INSERT INTO utilisateurs (nom, prenom, pseudo, mail, image, motdepasse, biographie)
VALUES ('Valcke', 'Tristan', 'Trisouille', 't.valcke@students.ephec.be',
        'https://cdn-icons-png.flaticon.com/512/149/149071.png',
        '$2b$12$WMwXzaY3ZQZW9/deHJeaLOz0LdLC9AkQTr8oUwEGH.CuX8Dh.8AXq', 'Voici ma bio'),
       ('Preat', 'Thomas', 'TomPrt', 'thomas.preat@students.ephec.be',
        'https://cdn-icons-png.flaticon.com/512/149/149071.png',
        '$2b$12$enuAKi57zLInxMWcwq9uP.RqAjqbqQ3xYdSiopqyQnN/rwySezWHu', 'Toujours le sourire !'),
       ('Roquet', 'Arnaud', 'Roqnoob', 'arnaud.roquet@students.ephec.be',
        'https://cdn-icons-png.flaticon.com/512/149/149071.png',
        '$2b$12$A/3DJii5iWUTQXzg.EbrCu08Vz0Txak3tvwJkJ77r8Wy4OuE/FEjC', 'Master en dégustation de pils.'),
       ('Doussis', 'Giorgios', 'GeoTheGreek', 'giorgios.doussis@students.ephec.be',
        'https://cdn-icons-png.flaticon.com/512/149/149071.png',
        '$2b$12$V9JBGxbPZ51brUVA4ctRk.8bFsNKNSU.KFXsee1.BJ/y31K3mGZ.e', 'J’amène le soleil avec moi.'),
       ('Kwizera', 'Dorian', 'DKwiz', 'dorian.kwizera@students.ephec.be',
        'https://cdn-icons-png.flaticon.com/512/149/149071.png',
        '$2b$12$obCmp53OrFY3.3UgPAOSI.HQD5o3WCfBu88r0.V.zSbGuq6sHKqWu', 'Toujours partant pour un défi.');

-- Trisouille : "user123"
-- TomPrt : "preat123"
-- Roqnoob : "roquet456"
-- GeoTheGreek : "greece789"
-- DKwiz : "kwz321"