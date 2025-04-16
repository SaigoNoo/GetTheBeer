import React, { useEffect, useState } from "react";
import beerMug from "./img/beermug.png";
import styles from "./styles/acceuil.module.css";
import { useNavigate } from "react-router-dom";

const HomePage = () => {
  const navigate = useNavigate();
  const [friends, setFriends] = useState([]);
  const [userId, setUserId] = useState(1); // Remplace 1 par l'ID de l'utilisateur connecté dynamiquement plus tard

  useEffect(() => {
    fetch(`http://localhost:8000/api/friends/${userId}`)
      .then((response) => response.json())
      .then((data) => setFriends(data.amis))
      .catch((error) => console.error("Erreur lors de la récupération des amis:", error));
  }, [userId]);

  return (
    <div className={styles["home-page"]}>
      {/* Header */}
      <header>
        <div className={styles["top-banner"]}>
          <div className={styles["left-content"]}>
            <img src={beerMug} alt="Logo des bières" className={styles.logo} />
            <div className={styles.title}>
              <h1>Get The Beer</h1>
              <h2>Le jeu de hasard des gens heureux</h2>
            </div>
          </div>
          <div className={styles["right-content"]}>
            <button className={styles["account-btn"]}>Mon compte</button>
            <button className={styles["play-btn"]} onClick={() => navigate("/game")}>Jouer</button>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className={styles["main-content"]}>
        <section className={styles.stats}>
          <h3>Mes stats</h3>
          {/* Contenu des stats */}
        </section>
        <section className={styles.news}>
          <h3>Actualités</h3>
          {/* Contenu des actualités */}
        </section>
        <section className={styles.friends}>
          <h3>Mes amis</h3>
          <ul>
            {friends.map((ami) => (
              <li key={ami.user_ID}>
                {ami.prenom} {ami.nom} ({ami.pseudo})
              </li>
            ))}
          </ul>
        </section>
      </main>
    </div>
  );
};

export default HomePage;
