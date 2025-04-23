import React, { useContext, createContext, useEffect, useState } from "react";

const AuthContext = createContext();

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Vérifie si l'utilisateur est connecté
  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/me", {
          credentials: "include",
        });
        if (!res.ok) throw new Error("Non connecté");
        const data = await res.json();
        setUser(data.user);
      } catch (err) {
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  // Fonction de login
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
        return { success: false, message: data.message || "Connexion échouée" };
      }

      const meRes = await fetch("http://localhost:8000/api/me", {
        credentials: "include",
      });

      const meData = await meRes.json();
      setUser(meData.user);
      return { success: true, message: "Connexion réussie" };

    } catch (err) {
      return { success: false, message: "Erreur lors de la connexion" };
    }
  };

  // ✅ Fonction logout
  const logout = async () => {
    try {
      await fetch("http://localhost:8000/api/logout", {
        method: "POST",
        credentials: "include",
      });
    } catch (err) {
      console.error("Erreur pendant la déconnexion :", err);
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
