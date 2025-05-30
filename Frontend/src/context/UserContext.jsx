import React, {createContext, useContext, useEffect, useState} from "react";
import {toast} from "react-hot-toast";
const apiUrl = import.meta.env.VITE_API_URL;

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext); // <- garder ici mais groupé

export const UserProvider = ({children}) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    const fetchUser = async () => {
        try {
            const res = await fetch(`${apiUrl}/api/user/me`, {
                credentials: "include",
            });

            if (res.status === 401) {
                console.error("Pas de cookies valide, veuillez vous reconnecter !");
                setUser(null);
            } else if (res.ok) {
                const data = await res.json();
                console.log(data);
                setUser(data.user);
            } else {
                console.error("Erreur inconnue lors de la récupération de l'utilisateur");
            }
        } catch (err) {
            console.error("Erreur réseau :", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchUser();
    }, []);

    const login = async (username, password) => {
        try {
            const res = await fetch(`${apiUrl}/api/user/login`, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                credentials: "include",
                body: JSON.stringify({username, password}),
            });

            const data = await res.json();

            if (!res.ok || !data.success) {
                console.warn("Impossible de se connecter, mauvais identifiants!");
                return {success: false, message: data.message || "Échec de la connexion"};
            }

            await fetchUser();
            console.info("Connexion avec succès...");
            return {success: true, message: "Connexion réussie"};
        } catch (err) {
            console.error("Problème avec la backend !");
            return {success: false, message: "Erreur lors de la connexion"};
        }
    };

    const logout = async () => {
        try {
            await fetch(`${apiUrl}/api/user/logout`, {
                method: "POST",
                credentials: "include",
            });
        } catch (err) {
            console.error("Erreur de déconnexion :", err);
        } finally {
            setUser(null);
            toast.success("Déconnecté...");
        }
    };

    return (
        <AuthContext.Provider value={{user, loading, login, logout}}>
            {children}
        </AuthContext.Provider>
    );
};