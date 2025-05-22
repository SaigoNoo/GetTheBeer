import React, {useEffect, useState} from "react";
import styles from "./styles/game.module.css";
import beerMug from "./img/beermug.png";
import {useNavigate} from "react-router-dom";
import {useAuth} from "./context/UserContext.jsx";


// Import images pour la roulette
import beer1 from "./img/beer1.png";
import beer2 from "./img/beer2.png";
import beer3 from "./img/beer3.png";
import beer4 from "./img/beer4.png";
import beer5 from "./img/beer5.png";

const images = [beer1, beer2, beer3, beer4, beer5];

const GamePage = () => {
    const navigate = useNavigate();
    const {user, loading, setUser} = useAuth();

    const [slots, setSlots] = useState([beer1, beer2, beer3]);
    const [isSpinning, setIsSpinning] = useState(false);
    const [forceResult, setForceResult] = useState(null);
    const [message, setMessage] = useState(""); // État pour afficher le message de victoire

    const [opponents, setOpponents] = useState([]);
    const [selectedOpponent, setSelectedOpponent] = useState(null);
    const [betAmount, setBetAmount] = useState(1);

    useEffect(() => {
        if (!loading && !user) {
            navigate("/");
        }
    }, [user, loading, navigate]);

    useEffect(() => {
        fetch("http://localhost:8000/api/game/opponents", {
            method: "GET",
            credentials: "include", // Include cookies in the request
        })
            .then(res => {
                if (!res.ok) {
                    throw new Error(`Erreur HTTP: ${res.status}`);
                }
                return res.json();
            })
            .then(data => {
                setOpponents(data);
            })
            .catch(err => {
                console.error("[ERROR] Dans la chaine fetch:", err); // Erreur
            })
    }, []);

    const spinSlots = async (opponent, betAmount) => {

        setMessage(""); // Réinitialiser le message à chaque tour

        // Vérifications avant de commencer
        if (!opponent) {
            setMessage("Veuillez sélectionner un adversaire");
            return;
        }

        if (user.reserve_biere < betAmount) {
            setMessage("Vous n'avez pas assez de bières en réserve");
            return;
        }

        if (opponent.reserve_biere < betAmount) {
            setMessage("Votre adversaire n'a pas assez de bières en réserve");
            return;
        }

        if (opponent.reserve_biere < betAmount) {
            setMessage("L'adversaire n'a pas assez de bières en réserve");
            return;
        }


        setIsSpinning(true);
        setMessage("");

        let interval = setInterval(() => {
            setSlots([
                images[Math.floor(Math.random() * images.length)],
                images[Math.floor(Math.random() * images.length)],
                images[Math.floor(Math.random() * images.length)]
            ]);
        }, 100);

        setTimeout(async () => {
            clearInterval(interval);
            setIsSpinning(false);

            let finalResult = forceResult || [
                images[Math.floor(Math.random() * images.length)],
                images[Math.floor(Math.random() * images.length)],
                images[Math.floor(Math.random() * images.length)],
            ];

            setSlots(finalResult);

            // Check if the user wins
            if (finalResult[0] === finalResult[1] && finalResult[1] === finalResult[2]) {
                setMessage("🎉 Victoire ! 🎉");

                // Call the backend to handle the transaction
                try {
                    const response = await fetch("http://localhost:8000/api/game/transaction", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        credentials: "include",
                        body: JSON.stringify({
                            winner_id: user.user_id,
                            loser_id: opponent.user_ID,
                            beers: betAmount,
                        }),
                    });

                    if (!response.ok) {
                        throw new Error("Erreur lors de la transaction");
                    }

                    const data = await response.json();

                    // Update the opponent's beer reserve
                    setOpponents((prevOpponents) =>
                        prevOpponents.map((o) =>
                            o.id === opponent.user_ID
                                ? {...o, reserve_biere: o.reserve_biere - betAmount}
                                : o
                        )
                    );
                } catch (error) {
                    console.error("Erreur lors de la transaction:", error);
                }
            } else {
                setMessage("😢 Défaite ! 😢");

                try {
                    const response = await fetch("http://localhost:8000/api/game/transaction", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        credentials: "include",
                        body: JSON.stringify({
                            winner_id: opponent.user_ID,
                            loser_id: user.user_id,
                            beers: betAmount,
                        }),
                    });

                    if (!response.ok) {
                        throw new Error("Erreur lors de la transaction");
                    }

                    const data = await response.json();

                    // Update the user's beer reserve
                    setUser((prevUser) => ({
                        ...prevUser,
                        reserve_biere: prevUser.reserve_biere - betAmount,
                    }));
                } catch (error) {
                    console.error("Erreur lors de la transaction:", error);
                }
            }
        }, 3000); // Stop spinning after 3 seconds
    };


    return (
        <div className={styles["game-page"]}>
            <header>
                <div className={styles["top-banner"]}>
                    <div className={styles["left-content"]}>
                        <img src={beerMug} alt="Logo des bières" className={styles.logo}/>
                        <div className={styles.title}>
                            <h1>Get The Beer</h1>
                            <h2>Le jeu de hasard des gens heureux</h2>
                        </div>
                    </div>
                    <div className={styles["right-content"]}>
                        <button className={styles["account-btn"]} onClick={() => navigate("/profil")}>Mon compte
                        </button>
                        <button className={styles["play-btn"]} onClick={() => navigate("/home")}>Retour</button>
                    </div>
                </div>
            </header>

            <main>
                <div className={styles["game-container"]}>
                    <h1>🎰 C'est la roulette AAAAAA 🎰</h1>

                    <div className={styles["slot-machine"]}>
                        {slots.map((slot, index) => (
                            <img key={index} src={slot} className={isSpinning ? styles.spinning : ""} alt="slot"/>
                        ))}
                    </div>

                    <h2>Jouer contre :</h2>
                    <select
                        value={selectedOpponent?.user_ID || ""}
                        onChange={e => setSelectedOpponent(
                            opponents.find(u => u.user_ID == e.target.value))
                        }
                    >
                        <option value="">Choisir un adversaire</option>
                        {opponents.map(opponent => (
                            <option key={opponent.user_ID} value={opponent.user_ID}>
                                {opponent.pseudo} ({opponent.beers} bières)
                            </option>
                        ))}
                    </select>

                    <div>
                        <label>Mise :</label>
                        <input
                            type="number"
                            min="1"
                            value={betAmount}
                            onChange={e => setBetAmount(parseInt(e.target.value) || 1)}
                        />
                    </div>

                    <button
                        className={styles.button}
                        onClick={() => spinSlots(selectedOpponent, betAmount)}
                        disabled={isSpinning}
                    >
                        Lancer la roulette skibidi
                    </button>

                    <p>Votre réserve de bières : {user?.reserve_biere || 0}</p>

                    {/* Option pour truquer le résultat */}
                    <div>
                        <button className={styles.button} onClick={() => setForceResult([beer2, beer2, beer2])}>Truquer
                            (3 bières identiques)
                        </button>
                        <button className={styles.button} onClick={() => setForceResult(null)}>Retour en mode
                            aléatoire
                        </button>
                    </div>
                    {message && <h2 className={styles["victory-message"]}>{message}</h2>}
                </div>
            </main>
        </div>
    );
};

export default GamePage;
