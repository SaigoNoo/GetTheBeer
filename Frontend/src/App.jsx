import {Route, Routes} from "react-router-dom";
import LoginPage from "./LoginPage";
import SignupPage from "./newAccountPage.jsx";
import HomePage from "./HomePage";
import GamePage from "./GamePage";
import ProfilePage from "./ProfilePage";
import {useAuth, UserProvider} from "./context/UserContext.jsx";
import PrivateRoute from "./components/PrivateRoute.jsx";
import "./styles/global.css";


function AppRoutes() {
    const {loading} = useAuth();

    if (loading) {
        return <p style={{color: "white", textAlign: "center", marginTop: "50px"}}>Chargement...</p>;
    }

    return (
        <Routes>
            <Route path="/" element={<LoginPage/>}/>
            <Route path="/signUp" element={<SignupPage/>}/>
            <Route
                path="/home"
                element={
                    <PrivateRoute>
                        <HomePage/>
                    </PrivateRoute>
                }
            />
            <Route
                path="/game"
                element={
                    <PrivateRoute>
                        <GamePage/>
                    </PrivateRoute>
                }
            />
            <Route
                path="/profil"
                element={
                    <PrivateRoute>
                        <ProfilePage/>
                    </PrivateRoute>
                }
            />
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
