import {Navigate} from "react-router-dom";
import {useAuth} from "../context/UserContext.jsx";

export default function PrivateRoute({children}) {
    const {user, loading} = useAuth();

    if (loading) {
        return <p style={{color: "white", textAlign: "center", marginTop: "50px"}}>Chargement...</p>;
    }

    if (!user) {
        return <Navigate to="/" replace/>;
    }

    return children;
}
