import React, { useState, useEffect } from "react";
import styles from "./styles/game.module.css";
import beerMug from "./img/beermug.png";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useAuth } from "./authProvider.jsx";


// Import images pour la roulette
import beer1 from "./img/beer1.png";
import beer2 from "./img/beer2.png";
import beer3 from "./img/beer3.png";
import beer4 from "./img/beer4.png";
import beer5 from "./img/beer5.png";
/*
function Products() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    // Effectuer la requête GET vers FastAPI pour récupérer les produits
    axios.get("http://127.0.0.1:8000/products")
      .then(response => {
        setProducts(response.data.products); // Mise à jour du state avec les produits reçus
      })
      .catch(error => console.error("Erreur lors de la récupération des produits:", error));
  }, []); // [] signifie qu'on exécute cet effet une seule fois au montage du composant
};
*/
const images = [beer1, beer2, beer3, beer4, beer5];

const GamePage = () => {
  const navigate = useNavigate();
  const { user, loading } = useAuth();
  const [slots, setSlots] = useState([beer1, beer2, beer3]);
  const [isSpinning, setIsSpinning] = useState(false);
  const [forceResult, setForceResult] = useState(null);
  const [message, setMessage] = useState(""); // État pour afficher le message de victoire

  useEffect(() => {
    if (!loading && !user) {
      navigate("/");
    }
  }, [user, loading, navigate]);

  if (loading) {
    return <div>Chargement...</div>; // Optionnel : spinner ou écran vide
  }

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
      <div className={styles["game-page"]}>
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
              <button className={styles["play-btn"]} onClick={() => navigate("/home")}>Retour</button>
            </div>
          </div>
        </header>

        <main>
          <div className={styles["game-container"]}>
            <h1>🎰 C'est la roulette AAAAAA 🎰</h1>
            <div className={styles["slot-machine"]}>
              {slots.map((slot, index) => (
                  <img key={index} src={slot} className={isSpinning ? styles.spinning : ""} alt="slot" />
              ))}
            </div>

            <button className={styles.button} onClick={spinSlots} disabled={isSpinning}>Lancer la roulette skibidi</button>

            {/* Option pour truquer le résultat */}
            <button className={styles.button} onClick={() => setForceResult([beer2, beer2, beer2])}>Truquer (3 bières identiques)</button>
            <button className={styles.button} onClick={() => setForceResult(null)}>Retour en mode aléatoire</button>

            {message && <h2 className={styles["victory-message"]}>{message}</h2>}
          </div>
        </main>
      </div>
  );
};

export default GamePage;
