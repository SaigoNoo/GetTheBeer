import { useState } from "react";
import { useNavigate } from "react-router-dom";
import beermug from "./img/beermug.png"
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
            setInfo("Les mots de passe ne correspondent pas.");
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
                setInfo(data.message);
                setTimeout(() => navigate(`/home?id=${data.userId}`), 1000);
            } else {
                // Traduire l'erreur technique en message utilisateur
                setInfo(formatErrorMessage(data.detail));
            }
        } catch (error) {
            setInfo("Erreur lors de l'inscription.");
        }
    };

    // Fonction pour formater les messages d'erreur
    const formatErrorMessage = (errorDetail) => {
        const errorMessage = String(errorDetail);

        // Messages d'erreur spécifiques pour les problèmes courants
        if (errorMessage.includes("Duplicate entry") && errorMessage.includes("for key 'mail'")) {
            const email = errorMessage.match(/'([^']+)'/)[1];
            return `L'adresse email ${email} est déjà utilisée.`;
        }

        if (errorMessage.includes("Duplicate entry") && errorMessage.includes("for key 'pseudo'")) {
            const pseudo = errorMessage.match(/'([^']+)'/)[1];
            return `Le pseudo ${pseudo} est déjà pris.`;
        }

        // Autres cas d'erreurs possibles
        if (errorMessage.includes("Data too long")) {
            return "Une des informations saisies dépasse la longueur autorisée.";
        }

        // Message par défaut si aucun pattern ne correspond
        return `Erreur lors de l'inscription : ${errorDetail}`;
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
            <div className={styles.container}>
                <img src={beermug} alt="Chope de bière gauche" className={styles["image-left"]}/>
                <img src={beermug} alt="Chope de bière droite" className={styles["image-right"]}/>
            </div>
        </div>
    );
};

export default SignupPage;