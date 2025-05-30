import {useEffect, useState} from "react";
import {useLocation, useNavigate} from "react-router-dom";
import axios from "axios";
import {toast, Toaster} from "react-hot-toast";
import styles from "./styles/connexion.module.css";

const apiUrl = import.meta.env.VITE_API_URL;

const ResetPassword = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    // Récupérer le token depuis l'URL
    const queryParams = new URLSearchParams(location.search);
    const token = queryParams.get("token");

    // Rediriger vers la page d'accueil si le token est absent
    useEffect(() => {
        if (!token) {
            navigate("/", {replace: true});
        }
    }, [token, navigate]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!password || !confirmPassword) {
            toast.error("Remplis tous les champs");
            return;
        }

        if (password !== confirmPassword) {
            toast.error("Les mots de passe ne correspondent pas");
            return;
        }

        try {
            const response = await axios.post(`${apiUrl}/api/user/reset_password`, {
                token: token,
                password: password,
            });

            if (response.data.code === "RESET_OK") {
                toast.success(response.data.message);
                setTimeout(() => navigate("/"), 1500);
            } else {
                toast.error(response.data.message || "Erreur");
            }
        } catch (err) {
            console.error(err);
            toast.error("Erreur serveur");
        }
    };

    return (
        <>
            <Toaster position="bottom-right"/>
            <div className={styles["reset-page"]}>
                <h2>Réinitialisation du mot de passe</h2>
                <form onSubmit={handleSubmit} className={styles.form}>
                    <input
                        type="password"
                        placeholder="Nouveau mot de passe"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className={styles.form_input}
                    />
                    <input
                        type="password"
                        placeholder="Confirmer le mot de passe"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        className={styles.form_input}
                    />
                    <button className={styles.form_submit} type="submit">
                        Réinitialiser
                    </button>
                </form>
            </div>
        </>
    );
};

export default ResetPassword;
