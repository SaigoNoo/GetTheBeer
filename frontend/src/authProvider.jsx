import { createContext, useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true); // Pour éviter le flash de contenu
  const navigate = useNavigate();

  useEffect(() => {
    let isMounted = true;
    const controller = new AbortController();

    fetch("http://localhost:8000/api/me", {
      credentials: "include",
      signal: controller.signal,
    })
      .then(res => {
        if (res.status === 401) {
          if (isMounted) {
            setUser(null);
            setLoading(false);
          }
          return null;
        }
        return res.json();
      })
      .then(data => {
        if (data && isMounted) {
          setUser(data.user);
          setLoading(false);
        }
      })
      .catch(() => {
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
      controller.abort();
    };
  }, []);

  // Fonction de login (à utiliser dans LoginPage)
  const login = async (username, password) => {
    const response = await fetch("http://localhost:8000/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    if (response.ok) {
      // Attendre 500ms pour que le cookie soit stocké
      await new Promise(resolve => setTimeout(resolve, 500));
      const meResponse = await fetch("http://localhost:8000/api/me", {
        credentials: "include"
      });
      const userData = await meResponse.json();
      setUser(userData.user);
      navigate("/home");
    }
    return data;
  };

  // Fonction de logout
  const logout = async () => {
    await fetch("http://localhost:8000/api/logout", {
      method: "POST",
      credentials: "include",
    });
    setUser(null);
    navigate("/login");
  };

  return (
    <AuthContext.Provider value={{ user, setUser, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}

export default AuthProvider;