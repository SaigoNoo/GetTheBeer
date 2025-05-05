import React, { createContext, useContext, useEffect, useState } from "react";

const AuthContext = createContext();

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchUser = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/me", {
        credentials: "include",
      });

      if (res.status === 401) {
        // Pas connecté : on ne log plus rien
        setUser(null);
      } else if (res.ok) {
        const data = await res.json();
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
      const res = await fetch("http://localhost:8000/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ username, password }),
      });

      const data = await res.json();

      if (!res.ok || !data.success) {
        return { success: false, message: data.message || "Échec de la connexion" };
      }

      await fetchUser();
      return { success: true, message: "Connexion réussie" };
    } catch (err) {
      return { success: false, message: "Erreur lors de la connexion" };
    }
  };

  const logout = async () => {
    try {
      await fetch("http://localhost:8000/api/logout", {
        method: "POST",
        credentials: "include",
      });
    } catch (err) {
      console.error("Erreur de déconnexion :", err);
    } finally {
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);