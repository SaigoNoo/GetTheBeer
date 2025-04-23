import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "./context/UserContext";
import styles from "./styles/profil.module.css";

const ProfilePage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
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
        console.error(err);
      }
      
    };

    fetchProfile();
  }, []);

  if (!profile) return <p>Chargement...</p>;

  return (
    <div className={styles["profile-page"]}>
      <div className={styles["profile-container"]}>
        <h1>{profile.pseudo}</h1>
        <p><strong>Nom :</strong> {profile.nom}</p>
        <p><strong>Prénom :</strong> {profile.prenom}</p>
        <p><strong>Email :</strong> {profile.mail}</p>

        <h2>Statistiques</h2>
        <p>À venir...</p>

        <h2>Biographie</h2>
        <p>{profile.biographie}</p>

        <button className={styles.backBtn} onClick={() => navigate("/home")}>
          Retour
        </button>
        <button className={styles.backBtn} style={{ marginLeft: "10px" }}>
          Modifier le profil
        </button>
      </div>
    </div>
  );
};

export default ProfilePage;
