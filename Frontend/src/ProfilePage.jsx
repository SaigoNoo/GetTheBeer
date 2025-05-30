import React, {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import styles from "./styles/profile.module.css";
import beerMug from "./img/beermug.png";
import {useAuth} from "./context/UserContext";
import {toast, Toaster} from 'react-hot-toast';

const apiUrl = import.meta.env.VITE_API_URL;

const ProfilePage = () => {
    const navigate = useNavigate();
    const {user} = useAuth();
    const [profile, setProfile] = useState(null);

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const response = await fetch(`${apiUrl}/api/user/profil`, {
                    credentials: "include",
                });
                if (!response.ok) throw new Error("Erreur lors de la récupération");
                const data = await response.json();
                setProfile(data);
                console.log("Profil chargé :", data);
            } catch (err) {
                console.error("Erreur chargement profil :", err);
            }
        };

        fetchProfile();
    }, []);

    if (!profile) return <div className={styles.loading}>Chargement du profil...</div>;

    return (
        <>
            <Toaster position="bottom-right" reverseOrder={false}/>

            <div className={styles.pageWrapper}>


                <header className={styles.header}>
                    <div className={styles["header-left"]}>
                        <img src={beerMug} alt="Logo" className={styles.logo}/>
                        <div className={styles.titre}>
                            <h1>Get The Beer</h1>
                            <h2>Le jeu d’hasard des alcoolos</h2>
                        </div>
                    </div>
                    <div className={styles["header-right"]}>
                        <button className={styles.bouton} onClick={() => navigate("/home")}>Accueil</button>
                        <button className={styles.bouton} onClick={() => navigate("/game")}>Jouer</button>
                    </div>
                </header>


                <main className={styles.mainContent}>
                    <div className={styles.profileCard}>
                        <div className={styles.profileImage} style={{backgroundImage: `url(${profile.image})`}}></div>

                        <div className={styles.userInfo}>
                            <table className={styles.table}>
                                <tr className={styles.headerLine}>
                                    <td>Nom:</td>
                                    <td>Prénom:</td>
                                </tr>
                                <tr className={styles.dataLine}>
                                    <td>{profile.prenom}</td>
                                    <td>{profile.nom}</td>
                                </tr>
                                <tr className={styles.headerLine}>
                                    <td>Pseudo:</td>
                                    <td>e-mail:</td>
                                </tr>
                                <tr className={styles.dataLine}>
                                    <td>{profile.pseudo}</td>
                                    <td>{profile.mail}</td>
                                </tr>
                                <tr className={styles.headerLine}>
                                    <td>Ma bio:</td>
                                </tr>
                                <tr className={styles.dataLine}>
                                    <td>{profile.biographie}</td>
                                </tr>
                            </table>
                        </div>
                    </div>


                    <div className={styles.actions}>
                        <button className={styles.button}
                                onClick={() => toast.error("Cette fonctionnalité est en cours de développement...")}>Modifier
                            le profil
                        </button>
                        <button className={styles.button} onClick={() => navigate("/home")}>Voir la liste d'amis
                        </button>
                    </div>
                </main>
            </div>
        </>
    );
};

export default ProfilePage;
