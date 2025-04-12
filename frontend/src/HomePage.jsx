import React from "react";
import beerMug from "./img/beermug.png";
import styles from "./styles/acceuil.module.css";
import { useNavigate } from "react-router-dom";
const HomePage = () => {
  const navigate = useNavigate();
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
            {/* Contenu des amis */}
          </section>
        </main>
      </div>
  );
};

export default HomePage;
