import {Routes, Route} from "react-router-dom";
import LoginPage from "./LoginPage";
import SignupPage from "./newAccountPage.jsx";
import HomePage from "./HomePage";
import GamePage from "./GamePage";
import ProfilePage from "./ProfilePage";
import {UserProvider, useAuth} from "./context/UserContext.jsx";
import "./styles/global.css";

// Wrapper pour attendre que le contexte finisse de charger
function AppRoutes() {
    const {loading, user} = useAuth();

    if (loading) {
        return <p style={{color: "white", textAlign: "center", marginTop: "50px"}}>Chargement...</p>;
    }

    return (
        <Routes>
            <Route path="/" element={<LoginPage/>}/>
            <Route path="/signUp" element={<SignupPage/>}/>
            <Route path="/home" element={<HomePage/>}/>
            <Route path="/game" element={<GamePage/>}/>
            <Route path="/profil" element={<ProfilePage/>}/>
        </Routes>
    );
}

function App() {
    return (
        <UserProvider>
            <AppRoutes/>
        </UserProvider>
    );
}

export default App;
