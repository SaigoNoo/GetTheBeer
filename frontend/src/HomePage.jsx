import React from "react";
import beerMug from "./img/beermug.png";
import "./styles/acceuil.css";
import { useNavigate } from "react-router-dom";
const HomePage = () => {
  const navigate = useNavigate();
  return (
    <div className="home-page">
      {/* Header */}
      <header>
        <div className="top-banner">
          <div className="left-content">
            <img src={beerMug} alt="Logo des bières" className="logo" />
            <div className="title">
              <h1>Get The Beer</h1>
              <h2>Le jeu de hasard des gens heureux</h2>
            </div>
          </div>
          <div className="right-content">
            <button className="account-btn">Mon compte</button>
            <button className="play-btn" onClick={() => navigate("/game")}>Jouer</button>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="main-content">
        <section className="stats">
          <h3>Mes stats</h3>
          {/* Contenu des stats */}
        </section>
        <section className="news">
          <h3>Actualités</h3>
          {/* Contenu des actualités */}
        </section>
        <section className="friends">
          <h3>Mes amis</h3>
          {/* Contenu des amis */}
        </section>
      </main>
    </div>
  );
};

export default HomePage;
