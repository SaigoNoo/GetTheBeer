import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./styles/profile.module.css";
import beerMug from "./img/beermug.png";
import { useAuth } from "./context/UserContext";

const ProfilePage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/profile", {
          credentials: "include",
        });
        if (!response.ok) throw new Error("Erreur lors de la récupération");
        const data = await response.json();
        setProfile(data);
        console.log("Profil chargé :", data);
      } catch (err) {
        console.error("Erreur chargement profil :", err);
      }
    };

    fetchProfile();
  }, []);

  if (!profile) return <div className={styles.loading}>Chargement du profil...</div>;

  return (
    <div className={styles.pageWrapper}>


      <header className={styles.header}>
        <div className={styles["header-left"]}>
          <img src={beerMug} alt="Logo" className={styles.logo} />
          <div className={styles.titre}>
            <h1>Get The Beer</h1>
            <h2>Le jeu d’hasard des alcoolos</h2>
          </div>
        </div>
        <div className={styles["header-right"]}>
          <button className={styles.bouton} onClick={() => navigate("/home")}>Accueil</button>
          <button className={styles.bouton} onClick={() => navigate("/game")}>Jouer</button>
        </div>
      </header>


      <main className={styles.mainContent}>
        <div className={styles.profileCard}>
          <div className={styles.profileImage}></div>

          <div className={styles.userInfo}>
            <p><strong>Nom :</strong> {profile.nom}</p>
            <p><strong>Prénom :</strong> {profile.prenom}</p>
            <p><strong>Pseudo :</strong> {profile.pseudo}</p>

            <p className={styles.statistiques}>Statistique future à venir</p>
            <p className={styles.statistiques}>Statistique future à venir</p>

            <p><strong>Biographie :</strong></p>
            <p className={styles.bio}>{profile.biographie || "Aucune biographie pour le moment."}</p>
          </div>
        </div>


        <div className={styles.actions}>
          <button className={styles.button} onClick={() => navigate("/home")}>Modifier le profil</button>
          <button className={styles.button} onClick={() => navigate("/home")}>Voir la liste d'amis</button>
        </div>
      </main>
    </div>
  );
};

export default ProfilePage;
