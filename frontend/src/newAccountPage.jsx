import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./styles/connexion.css";
import beerMug from "./img/beermug.png";

const SignupPage = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [email, setEmail] = useState("");
    const [info, setInfo] = useState("");
    const navigate = useNavigate(); // Pour naviguer après l'inscription

    const signup = async (event) => {
        event.preventDefault();

        if (password !== confirmPassword) {
            setInfo(<p style={{ color: "red" }}>Les mots de passe ne correspondent pas.</p>);
            return;
        }

        try {
            const response = await fetch("http://localhost:8000/api/signup", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username, email, password }),
            });

            const data = await response.json();

            if (response.ok) {
                setInfo(<p style={{ color: "green" }}>{data.message}</p>);
                setTimeout(() => navigate("/home"), 1000); // Redirection après succès
            } else {
                setInfo(<p style={{ color: "red" }}>{data.message}</p>);
            }
        } catch (error) {
            setInfo(<p style={{ color: "red" }}>Erreur lors de la création du compte.</p>);
        }
    };

    return (
        <div className="signup-container">
            <div className="content">
                <h1>Créer un compte</h1>
                <form onSubmit={signup}>
                    <label htmlFor="username">Nom d'utilisateur :</label>
                    <input id="username" type="text" placeholder="Nom d'utilisateur" value={username} onChange={(e) => setUsername(e.target.value)} required />

                    <label htmlFor="email">Email :</label>
                    <input id="email" type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />

                    <label htmlFor="password">Mot de passe :</label>
                    <input id="password" type="password" placeholder="Mot de passe" value={password} onChange={(e) => setPassword(e.target.value)} required />

                    <label htmlFor="confirmPassword">Confirmer le mot de passe :</label>
                    <input id="confirmPassword" type="password" placeholder="Confirmer le mot de passe" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />

                    <br />
                    <input type="submit" value="S'inscrire" />
                </form>
                {info && <div id="info">{info}</div>}
                <a href="/" className="forgot-password">Déjà un compte ?</a>
            </div>
            <div className="bottom-left">
                <img src={beerMug} alt="Icône bière" />
                <div className="bottom-left-text">
                    <h1>Get The Beer</h1>
                    <h2>Le jeu de hasard des gens heureux</h2>
                </div>
            </div>
        </div>
    );
};

export default SignupPage;