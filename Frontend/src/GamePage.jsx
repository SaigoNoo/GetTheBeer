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
import {toast, Toaster} from "react-hot-toast";

const apiUrl = import.meta.env.VITE_API_URL;

const images = [beer1, beer2, beer3, beer4, beer5];

const GamePage = () => {
    const navigate = useNavigate();
    const {user, loading, setUser} = useAuth();

    const [slots, setSlots] = useState([beer1, beer2, beer3]);
    const [isSpinning, setIsSpinning] = useState(false);
    const [forceResult, setForceResult] = useState(null);
    const [message, setMessage] = useState(""); // message victoire/défaite

    const [opponents, setOpponents] = useState([]);
    const [selectedOpponent, setSelectedOpponent] = useState(null);
    const [betAmount, setBetAmount] = useState(1);

    useEffect(() => {
        if (!loading && !user) {
            navigate("/");
        }
    }, [user, loading, navigate]);

    // Fonction pour récupérer les adversaires
    const fetchOpponents = () => {
        fetch(`${apiUrl}/api/game/opponents`, {
            method: "GET",
            credentials: "include",
        })
        .then(res => {
            if (!res.ok) throw new Error(`Erreur HTTP: ${res.status}`);
            return res.json();
        })
        .then(data => setOpponents(data))
        .catch(err => console.error("[ERROR] fetch opponents:", err));
    };

    // Fonction pour récupérer les infos user
    const fetchUser = () => {
        fetch(`${apiUrl}/api/user/me`, {
            method: "GET",
            credentials: "include",
        })
        .then(res => {
            if (!res.ok) throw new Error(`Erreur HTTP: ${res.status}`);
            return res.json();
        })
        .then(data => setUser(data))
        .catch(err => console.error("[ERROR] fetch user:", err));
    };

    // Charger les adversaires et user au démarrage (quand user chargé)
    useEffect(() => {
        if (!loading && user) {
            fetchOpponents();
            fetchUser();
        }
    }, [loading, user]);

    const spinSlots = async (opponent, betAmount) => {
        setMessage("");

        if (!opponent) {
            toast.error("Veuillez sélectionner un adversaire");
            return;
        }

        if (user.reserve_biere < betAmount) {
            toast.error("Vous n'avez pas assez de bières en réserve");
            return;
        }

        if (opponent.reserve_biere < betAmount) {
            toast.error("Votre adversaire n'a pas assez de bières en réserve");
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

            const userWon = finalResult[0] === finalResult[1] && finalResult[1] === finalResult[2];

            try {
                const response = await fetch(`${apiUrl}/api/game/transaction`, {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    credentials: "include",
                    body: JSON.stringify({
                        winner_id: userWon ? user.user_id : opponent.user_ID,
                        loser_id: userWon ? opponent.user_ID : user.user_id,
                        beers: betAmount,
                    }),
                });

                if (!response.ok) throw new Error("Erreur lors de la transaction");

                await response.json();

                // Après la transaction, on recharge les données depuis le backend
                fetchOpponents();
                fetchUser();

            } catch (error) {
                console.error("Erreur lors de la transaction:", error);
                toast.error("Erreur lors de la transaction, réessaie plus tard");
            }

            setMessage(userWon ? "🎉 Victoire ! 🎉" : "😢 Défaite ! 😢");

        }, 3000);
    };

    return (
        <>
            <Toaster position="bottom-right" reverseOrder={false}/>

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
                            <button className={styles.button}
                                    onClick={() => setForceResult([beer2, beer2, beer2])}>Truquer
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
        </>
    );
};

export default GamePage;
