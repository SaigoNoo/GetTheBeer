import { Routes, Route } from "react-router-dom";
import LoginPage from "./LoginPage";
import SignupPage from "./newAccountPage.jsx";
import HomePage from "./HomePage";
import GamePage from "./GamePage";
import "./styles/global.css";


function App() {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/home" element={<HomePage />} />
      <Route path="/game" element={<GamePage />} />
      <Route path="/signUp" element={<SignupPage />} />
    </Routes>
  );
}

export default App;