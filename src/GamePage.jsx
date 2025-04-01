import React, { useState, useEffect } from "react";
import "./styles/game.css";
import beerMug from "./img/beermug.png";
import { useNavigate } from "react-router-dom";

// Import images pour la roulette
import beer1 from "./img/beer1.png";
import beer2 from "./img/beer2.png";
import beer3 from "./img/beer3.png";
import beer4 from "./img/beer4.png";
import beer5 from "./img/beer5.png";

const images = [beer1, beer2, beer3, beer4, beer5];

const GamePage = () => {
  const navigate = useNavigate();

  const [slots, setSlots] = useState([beer1, beer2, beer3]);
  const [isSpinning, setIsSpinning] = useState(false);
  const [forceResult, setForceResult] = useState(null);
  const [message, setMessage] = useState(""); // État pour afficher le message de victoire

  const spinSlots = () => {
    setIsSpinning(true);
    setMessage(""); // Réinitialiser le message à chaque tour

    
    let interval = setInterval(() => {
      setSlots([
        images[Math.floor(Math.random() * images.length)],
        images[Math.floor(Math.random() * images.length)],
        images[Math.floor(Math.random() * images.length)]
      ]);
    }, 100);

    setTimeout(() => {
      clearInterval(interval);
      setIsSpinning(false);

      let finalResult = forceResult || [
        images[Math.floor(Math.random() * images.length)],
        images[Math.floor(Math.random() * images.length)],
        images[Math.floor(Math.random() * images.length)]
      ];

      setSlots(finalResult);

      // Vérifier si toutes les images sont identiques
      if (finalResult[0] === finalResult[1] && finalResult[1] === finalResult[2]) {
        setMessage("🎉 Victoire ! 🎉");
      }
    }, 3000); // Arrêt après 3 secondes
  };


  return (
    <div className="game-page">
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
            <button className="play-btn" onClick={() => navigate("/home")}>Retour</button>
          </div>
        </div>
      </header>

      <main>
        <div className="game-container">
          <h1>🎰 C'est la roulette AAAAAA 🎰</h1>

          <div className="slot-machine">
            {slots.map((slot, index) => (
              <img key={index} src={slot} className={isSpinning ? "spinning" : ""} alt="slot" />
            ))}
          </div>

          <button onClick={spinSlots} disabled={isSpinning}>Lancer la roulette</button>

          {/* Option pour truquer le résultat */}
          <button onClick={() => setForceResult([beer2, beer2, beer2])}>Truquer (3 bières identiques)</button>
          <button onClick={() => setForceResult(null)}>Retour en mode aléatoire</button>
        
          {message && <h2 className="victory-message">{message}</h2>}
        </div>
      </main>
    </div>
  );
};

export default GamePage;
