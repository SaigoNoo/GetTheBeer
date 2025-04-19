import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./styles/connexion.module.css";
import beerMug from "./img/beermug.png";
import axios from "axios";

const LoginPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(false);
  const [info, setInfo] = useState("");
  const navigate = useNavigate(); // Pour naviguer après connexion

  const login = async (event) => {
    {
    event.preventDefault();
    const response = await tryLogin(username, password);
    if (response.success) {
      setInfo(<p style={{ color: "green" }}>{response.message}</p>);
      setTimeout(() => {
        navigate("/home"); // Redirection après succès
      }, 1000);
    } else {
      setInfo(<p style={{ color: "red" }}>{response.message}</p>);
    }
    }
    //navigate("/home")
  };

  const [data, setData] = useState(null);

  useEffect(() => {
    // Appel à l'API FastAPI avec axios
    axios.get("http://localhost:8000/")
      .then(response => setData(response.data.message))
      .catch(error => console.error("Error:", error));
  }, []);
  

  const tryLogin = async (username, password) => {
    const response = await fetch("http://localhost:8000/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include", // <-- clé pour la session !
      body: JSON.stringify({ username, password }),
    });
    console.log(response.json())
    return await response.json();
  };

  return (
    <div className={styles["login-container"]}>
      <div className={styles.content}>
        <h1>connexion</h1>
        <div>
          <h5>FastAPI : {data}</h5>
        </div>
        <form className={styles.form} onSubmit={login}>
          <label className={styles.form_label} htmlFor="username">Username: </label>
          <input className={styles.form_input} id="username" type="text" placeholder="username" value={username} onChange={(e) => setUsername(e.target.value)} />
          <label className={styles.form_label} htmlFor="password">Password: </label>
          <input className={styles.form_input} id="password" type="password" placeholder="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          <br />
          <input className={styles.form_checkbox} id="remember" type="checkbox" checked={remember} onChange={(e) => setRemember(e.target.checked)} />
          <label className={styles.form_label} htmlFor="remember">Retenir ma connexion</label>
          <br />
          <input className={styles.form_submit} type="submit" value="Se connecter" />
        </form>
        {info && <div id="info">{info}</div>}
        <a href="#" className={styles["forgot-password"]}>Mot de passe oublié ?</a>
        <a href="/signUp" className={styles["forgot-password"]} id={styles.link_signup}>Créer un compte</a>
      </div>
      <div className={styles["bottom-left"]}>
        <img src={beerMug} alt="Icône bière" />
        <div className={styles["bottom-left-text"]}>
          <h1>Get The Beer</h1>
          <h2>Le jeu de hasard des gens heureux</h2>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;