import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import styles from "./styles/connexion.module.css";
import beerMug from "./img/beermug.png";
import axios from "axios";
import {useAuth} from "./context/UserContext.jsx";
import {toast, Toaster} from 'react-hot-toast';

const apiUrl = import.meta.env.VITE_API_URL;

const LoginPage = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [remember, setRemember] = useState(false);
    const [info, setInfo] = useState("");
    const [resetUsername, setResetUsername] = useState("");
    const [showResetForm, setShowResetForm] = useState(false);

    const navigate = useNavigate();
    const {user, loading, login} = useAuth();

    useEffect(() => {
        if (!loading && user) {
            console.log("Utilisateur connecté :", user.pseudo);
            navigate("/home");
        }
    }, [user, loading]);

    const handleLogin = async (event) => {
        event.preventDefault();
        try {
            const response = await login(username, password);
            if (response.success) {
                navigate("/home");
            } else {
                toast.error("Échec de la connexion");
            }
        } catch (error) {
            console.error("Erreur lors de la connexion :", error);
            toast.error("Erreur interne");
        }
    };

    const handleResetPassword = async (e) => {
        e.preventDefault();
        if (!resetUsername) {
            toast.error("Veuillez entrer votre nom d'utilisateur.");
            return;
        }

        try {
            const response = await axios.post(`${apiUrl}/api/user/reset_password_request`, {
                username: resetUsername,
            });

            if (response.data.code === "MAIL_SEND_OK") {
                toast.success(response.data.message);
                setShowResetForm(false);
            } else {
                toast.error(response.data.message || "Erreur lors de l'envoi.");
            }
        } catch (error) {
            console.error("Erreur API reset :", error);
            toast.error("Une erreur est survenue.");
        }
    };

    const [data, setData] = useState(null);
    useEffect(() => {
        axios
            .get(`${apiUrl}/api/test`)
            .then((response) => setData(response.data.message))
            .catch((error) => {
                console.error("Erreur de connexion au backend :", error);
                setData("Erreur de connexion au backend ❌");
            });
    }, []);

    return (
        <>
            <Toaster position="bottom-right" reverseOrder={false}/>

            <div className={styles["login-container"]}>
                <div className={styles.content}>
                    <h1>Bienvenue</h1>
                    {data && <h5 style={{color: "gray"}}>Backend : {data}</h5>}

                    {!showResetForm ? (
                        <form className={styles.form} onSubmit={handleLogin}>
                            <label className={styles.form_label} htmlFor="username">Username:</label>
                            <input
                                className={styles.form_input}
                                id="username"
                                type="text"
                                placeholder="Username"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                            />

                            <label className={styles.form_label} htmlFor="password">Password:</label>
                            <input
                                className={styles.form_input}
                                id="password"
                                type="password"
                                placeholder="Password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />

                            <div className={styles.form_check_wrapper}>
                                <input
                                    className={styles.form_checkbox}
                                    id="remember"
                                    type="checkbox"
                                    checked={remember}
                                    onChange={(e) => setRemember(e.target.checked)}
                                />
                                <label className={styles.form_label} htmlFor="remember">Retenir ma connexion</label>
                            </div>

                            <input className={styles.form_submit} type="submit" value="Se connecter"/>
                        </form>
                    ) : (
                        <form className={styles.form} onSubmit={handleResetPassword}>
                            <h2>Réinitialiser mon mot de passe</h2>
                            <input
                                className={styles.form_input}
                                placeholder="Username"
                                value={resetUsername}
                                onChange={(e) => setResetUsername(e.target.value)}
                            />
                            <input className={styles.form_submit} type="submit" value="Envoyer une demande"/>
                        </form>
                    )}

                    {info && <div id="info">{info}</div>}
                    <div id={styles["actions_login"]}>
                        <a
                            className={styles["forgot-password"]}
                            onClick={() => setShowResetForm(prev => !prev)}
                        >
                            {showResetForm ? "← Retour à la connexion" : "Mot de passe oublié ?"}
                        </a>
                        <a href="/signUp" className={styles["forgot-password"]} id={styles.link_signup}>
                            Créer un compte
                        </a>
                    </div>


                    <p className={styles["infobull"]}>
                        Information: GetTheBeer est un énorme projet développé par 5 étudiants...
                    </p>
                </div>

                <div className={styles["bottom-left"]}>
                    <img src={beerMug} alt="Icône bière"/>
                    <div className={styles["bottom-left-text"]}>
                        <h1>Get The Beer</h1>
                        <h2>Le jeu de hasard des gens heureux</h2>
                    </div>
                </div>
            </div>
        </>
    );
};

export default LoginPage;
