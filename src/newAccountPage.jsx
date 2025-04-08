import { useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./styles/signup.module.css";


const SignupPage = () => {
    const [formData, setFormData] = useState({
        nom: "",
        prenom: "",
        pseudo: "",
        mail: "",
        motdepasse: "",
        confirmPassword: "",
        biographie: ""
    });

    const [info, setInfo] = useState("");
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    };

    const signup = async (event) => {
        event.preventDefault();

        if (formData.motdepasse !== formData.confirmPassword) {
            setInfo(<p style={{ color: "red" }}>Les mots de passe ne correspondent pas.</p>);
            return;
        }

        try {
            const response = await fetch("http://localhost:8000/api/signup", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            });

            const data = await response.json();

            if (response.ok) {
                setInfo(<p style={{ color: "green" }}>{data.message}</p>);
                setTimeout(() => navigate("/home"), 1000);
            } else {
                setInfo(<p style={{ color: "red" }}>{data.message}</p>);
            }
        } catch (error) {
            setInfo(<p style={{ color: "red" }}>Erreur lors de l'inscription.</p>);
        }
    };

    return (
        <div className={styles.signup_container}>
            <div className={styles.signup_content}>
                <h1>Créer un compte</h1>
                <form className={styles.signup_form} onSubmit={signup}>
                    <input className={styles.signup_form_input} name="nom" placeholder="Nom" value={formData.nom} onChange={handleChange} required />
                    <input className={styles.signup_form_input} name="prenom" placeholder="Prénom" value={formData.prenom} onChange={handleChange} required />
                    <input className={styles.signup_form_input} name="pseudo" placeholder="Pseudo" value={formData.pseudo} onChange={handleChange} required />
                    <input className={styles.signup_form_input} name="mail" type="email" placeholder="Email" value={formData.mail} onChange={handleChange} required />
                    <textarea className={styles.signup_form_textarea} name="biographie" placeholder="Biographie" value={formData.biographie} onChange={handleChange} />
                    <input className={styles.signup_form_input} name="motdepasse" type="password" placeholder="Mot de passe" value={formData.motdepasse} onChange={handleChange} required />
                    <input className={styles.signup_form_input} name="confirmPassword" type="password" placeholder="Confirmer le mot de passe" value={formData.confirmPassword} onChange={handleChange} required />
                    <br />
                    <input className={styles.signup_form_submit} type="submit" value="S'inscrire" />
                </form>
                {info && <div id="info">{info}</div>}
                <a href="/" className={styles.login}>Déjà un compte ?</a>
            </div>
        </div>
    );
};

export default SignupPage;