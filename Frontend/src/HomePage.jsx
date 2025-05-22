import React, {useEffect, useState} from "react";
import beerMug from "./img/beermug.png";
import styles from "./styles/acceuil.module.css";
import {useNavigate} from "react-router-dom";
import {useAuth} from "./context/UserContext.jsx";
import axios from "axios";
import {toast, Toaster} from 'react-hot-toast';


const HomePage = () => {
    const navigate = useNavigate();
    const {user, loading, logout} = useAuth();
    const [search, setSearch] = useState("");
    const [searchResults, setSearchResults] = useState([]);
    const [friends, setFriends] = useState([]);

    const deleteFriend = async (friendId) => {
        try {
            await axios.post(
                `http://localhost:8000/api/user/delete_friend/?user_id=${user.user_id}&friend_id=${friendId}`,
                {},
                {headers: {accept: "application/json"}, withCredentials: true}
            );
            fetchFriends();
            toast.success("Ami supprimé avec succès");
        } catch (error) {
            toast.error("Erreur lors de la suppression de l'ami !");
            console.error("Erreur lors de la suppression de l'ami :", error);
        }
    };

    const addFriend = async (friendId) => {
        try {
            await axios.post(
                `http://localhost:8000/api/user/add_friend/?user_id=${user.user_id}&friend_id=${friendId}`,
                {},
                {headers: {accept: "application/json"}, withCredentials: true}
            );
            fetchFriends();
            toast.success("Ami ajouté avec succès !");
        } catch (error) {
            toast.error("Erreur lors de l'ajout de l'ami !");
            console.error("Erreur lors de l'ajout d'ami :", error);
        }
    };

    useEffect(() => {
        if (!loading && !user) {
            navigate("/");
        } else if (!loading && user) {
            fetchFriends();
        }
    }, [loading, user]);

    const fetchFriends = async () => {
        try {
            const res = await axios.get("http://localhost:8000/api/user/list_friends", {withCredentials: true});
            const data = typeof res.data === "string" ? JSON.parse(res.data) : res.data;
            setFriends(data);
        } catch (error) {
            console.error("Erreur lors de la récupération des amis :", error);
        }
    };

    useEffect(() => {
        const delayDebounce = setTimeout(() => {
            if (search.trim()) fetchSearchResults();
            else setSearchResults([]);
        }, 500);

        return () => clearTimeout(delayDebounce);
    }, [search]);

    const fetchSearchResults = async () => {
        try {
            const res = await axios.get("http://127.0.0.1:8000/api/user/show_members", {withCredentials: true});
            const data = typeof res.data === "string" ? JSON.parse(res.data) : res.data;

            const filtered = data
                .filter(u => u.user_ID !== user.user_id)
                .filter(u =>
                    [u.pseudo, u.prenom, u.nom].some(field =>
                        field.toLowerCase().includes(search.toLowerCase())
                    )
                );

            setSearchResults(filtered);
        } catch (error) {
            console.error("Erreur lors de la recherche :", error);
        }
    };

    if (loading) return <div>Chargement...</div>;

    return (
        <>
            <Toaster position="bottom-right" reverseOrder={false}/>
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
                        <div className={styles.searchFriends}>
                            <h3>Rechercher un ami</h3>
                            <input
                                type="search"
                                placeholder="Rechercher un ami..."
                                value={search}
                                onChange={(e) => setSearch(e.target.value)}
                            />
                            {search.trim() && (
                                searchResults.length > 0 ? (
                                    <div className={styles.searchResults}>
                                        {searchResults.map((user) => (
                                            <div
                                                key={user.user_ID}
                                                className={`${styles.friendLine} ${styles.addFriend}`}  // fond vert pour ajout
                                                onClick={() => addFriend(user.user_ID)}
                                                role="button"
                                                tabIndex={0}
                                                onKeyDown={(e) => {
                                                    if (e.key === 'Enter' || e.key === ' ') addFriend(user.user_ID);
                                                }}
                                            >
                                                <img className={styles.iconFriend} src={user.image} alt="user"/>
                                                <div className={styles.textContent}>
                                                    {user.pseudo} - {user.prenom} {user.nom}
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                ) : (
                                    <p>Aucun résultat pour "{search}"</p>
                                )
                            )}

                            <h3>Mes amis</h3>
                            {Array.isArray(friends) && friends.length > 0 ? (
                                friends.map((ami) => (
                                    <div
                                        key={ami.user_ID}
                                        className={`${styles.friendLine} ${styles.deleteFriend}`}  // fond rouge pour suppression
                                        onClick={() => deleteFriend(ami.user_ID)}
                                        role="button"
                                        tabIndex={0}
                                        onKeyDown={(e) => {
                                            if (e.key === 'Enter' || e.key === ' ') deleteFriend(ami.user_ID);
                                        }}
                                    >
                                        <img className={styles.iconFriend} src={ami.image} alt="ami"/>
                                        <div className={styles.textContent}>
                                            {ami.pseudo} - {ami.prenom} {ami.nom}
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <p>Aucun ami pour le moment</p>
                            )}

                        </div>
                    </section>
                </main>
            </div>
        </>
    );
};

export default HomePage;
