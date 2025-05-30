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
    const navigate = useNavigate();
    const {user, loading, login} = useAuth();

    useEffect(() => {
        if (!loading && user) {
            console.log("Utilisateur connecté :", user.pseudo);
            navigate("/home");
        } else {
            console.error("Pas de session enregistrée !");
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
                    <h1>Connexion</h1>
                    {data && <h5 style={{color: "gray"}}>Backend : {data}</h5>}

                    <form className={styles.form} onSubmit={handleLogin}>
                        <label className={styles.form_label} htmlFor="username">Username:</label>
                        <input
                            className={styles.form_input}
                            id="username"
                            type="text"
                            placeholder="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />

                        <label className={styles.form_label} htmlFor="password">Password:</label>
                        <input
                            className={styles.form_input}
                            id="password"
                            type="password"
                            placeholder="password"
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

                    {info && <div id="info">{info}</div>}

                    <a href="/reset" className={styles["forgot-password"]}>Mot de passe oublié ?</a>
                    <a href="/signUp" className={styles["forgot-password"]} id={styles.link_signup}>Créer un compte</a>
                    <p className={styles["infobull"]}>Information: GetTheBeer est un énorme projet développé par 5
                        étudiants, et étant donné que les technologies que nous mettons en place
                        sont nouvelles pour nous, nous avons eu un peu de mal a tout finir, il se peut donc que
                        certaines fonctionnalitées vous semblent
                        relativement basiques, mais elles seronts améliorées, visuellement et fonctionnellement avec le
                        temps !</p>
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