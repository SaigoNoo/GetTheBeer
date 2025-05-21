import React, {useEffect, useState} from "react";
import beerMug from "./img/beermug.png";
import styles from "./styles/acceuil.module.css";
import {useNavigate} from "react-router-dom";
import {useAuth} from "./context/UserContext.jsx";
import axios from "axios";

const HomePage = () => {
    const navigate = useNavigate();
    const {user, loading, logout} = useAuth();
    const [search, setSearch] = useState("");
    const [searchResults, setSearchResults] = useState([]);
    const [friends, setFriends,] = useState([]);

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

    useEffect(() => {
        const delayDebounce = setTimeout(() => {
            if (search.trim() !== "") {
                axios
                    .get("http://127.0.0.1:8000/api/user/show_members", {
                        withCredentials: true,
                    })
                    .then((response) => {
                        const data = typeof response.data === "string" ? JSON.parse(response.data) : response.data;

                        // On filtre en fonction du pseudo, prénom ou nom
                        const filtered = data.filter((user) => {
                            const searchLower = search.toLowerCase();
                            return (
                                user.pseudo.toLowerCase().includes(searchLower) ||
                                user.prenom.toLowerCase().includes(searchLower) ||
                                user.nom.toLowerCase().includes(searchLower)
                            );
                        });

                        setSearchResults(filtered);
                    })
                    .catch((error) => {
                        console.error("Erreur lors de la recherche :", error);
                    });
            } else {
                setSearchResults([]); // reset si rien tapé
            }
        }, 500); // délai pour éviter trop de requêtes

        return () => clearTimeout(delayDebounce); // clean le timeout si tu tapes vite
    }, [search]);

    if (loading) {
        return <div>Chargement...</div>;
    }

    return (<div className={styles["home-page"]}>
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
                <div className={styles.searchFriends}>
                    <h3>Rechercher un ami:</h3>
                    <input
                        type="search"
                        placeholder="Rechercher un ami..."
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                    />
                    {searchResults.length > 0 && (
                        <ul className={styles.searchResults}>
                            {searchResults.map((user) => (
                                <li key={user.id}>
                                    <img src={user.image} className={styles.iconFriend}/>
                                    {user.pseudo} - {user.prenom} {user.nom}
                                    <a onClick={() => console.log("Ajout d'ami en WIP")}>➕</a>
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
                <h3>Mes amis</h3>
                <ul>
                    {Array.isArray(friends) && friends.length > 0 ? (friends.map((ami) => (
                        <span className={styles.friendLine}>
                                    <img className={styles.iconFriend} src={ami.image}></img>
                            {ami.pseudo} - {ami.prenom} {ami.nom}
                            <span className={styles.actions}>
                                        <a href="#">❌ Supprimer</a>
                                    </span>
                                </span>))) : (<li>Aucun ami pour le moment</li>)}
                </ul>
            </section>
        </main>
    </div>);
};

export default HomePage;
