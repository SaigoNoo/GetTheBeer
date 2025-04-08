import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./styles/connexion.css";
import beerMug from "./img/beermug.png";
import axios from "axios";

const LoginPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(false);
  const [info, setInfo] = useState("");
  const navigate = useNavigate(); // Pour naviguer après connexion

  const login = async (event) => {
    {/*
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
    */}
    navigate("/home")
  };

  const [data, setData] = useState(null);

  useEffect(() => {
    // Appel à l'API FastAPI avec axios
    axios.get("http://localhost:8000/")
      .then(response => setData(response.data.message))
      .catch(error => console.error("Error:", error));
  }, []);
  

  const tryLogin = async (username, password) => {
    const url = `http://localhost:8000/api/login?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`;
    const response = await fetch(url);
    return await response.json();
  };

  return (
    <div className="login-container">
      <div className="content">
        <h1>connexion</h1>
        <div>
          <h1>FastAPI : {data}</h1>
        </div>
        <form onSubmit={login}>
          <label htmlFor="username">Username: </label>
          <input id="username" type="text" placeholder="username" value={username} onChange={(e) => setUsername(e.target.value)} />
          <label htmlFor="password">Password: </label>
          <input id="password" type="password" placeholder="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          <br />
          <input id="remember" type="checkbox" checked={remember} onChange={(e) => setRemember(e.target.checked)} />
          <label htmlFor="remember">Retenir ma connexion</label>
          <br />
          <input type="submit" value="Se connecter" />
        </form>
        {info && <div id="info">{info}</div>}
        <a href="#" className="forgot-password">Mot de passe oublié ?</a>
        <a href="/singUp" className="forgot-password" id={"link_signup"}>Créer un compte</a>
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

export default LoginPage;