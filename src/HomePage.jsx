import React, {useEffect, useState} from "react";
import beerMug from "./img/beermug.png";
import styles from "./styles/acceuil.module.css";
import {useNavigate} from "react-router-dom";
import {useAuth} from "./context/UserContext.jsx";
import axios from "axios";

const HomePage = () => {
    const navigate = useNavigate();
    const {user, loading, logout} = useAuth();
    const [friends, setFriends] = useState([]);

    useEffect(() => {
        if (!loading && !user) {
            navigate("/");
        } else if (!loading && user) {
            axios
                .get("http://localhost:8000/api/user/list_friends", {
                    withCredentials: true,
                })
                .then((response) => {
                    const data = typeof response.data === "string" ? JSON.parse(response.data) : response.data;
                    setFriends(data);
                })
                .catch((error) => {
                    console.error("Erreur lors de la récupération des amis :", error);
                });
        }
    }, [user, loading, navigate]);

    if (loading) {
        return <div>Chargement...</div>;
    }

    return (
        <div className={styles["home-page"]}>
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
                        <button className={styles["play-btn"]} onClick={() => navigate("/game")}>Jouer</button>
                        <button className={styles["logout-btn"]} onClick={logout}>Déconnexion</button>
                    </div>
                </div>
            </header>

            <main className={styles["main-content"]}>
                <section className={styles.stats}>
                    <h3>Mes stats</h3>
                </section>
                <section className={styles.news}>
                    <h3>Actualités</h3>
                </section>
                <section className={styles.friends}>
                    <h3>Mes amis</h3>
                    <ul>
                        {console.log(friends) || Array.isArray(friends) && friends.length > 0 ? (
                            friends.map((ami) => (
                                <li key={ami.user_ID}>{ami.pseudo}</li>
                            ))
                        ) : (
                            <li>Aucun ami pour le moment</li>
                        )}
                    </ul>
                </section>
            </main>
        </div>
    );
};

export default HomePage;
