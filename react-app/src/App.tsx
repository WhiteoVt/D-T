import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./AuthContext";
import NavBar from "./components/NavBar";
import LogInScreen from "./screens/LogInScreen";
import SignUpScreen from "./screens/SignUpScreen";
import TitleScreen from "./screens/TitleScreen";
import GameListScreen from "./screens/GameListScreen";
import UserListScreen from "./screens/UserListScreen";
import MainScreen from "./screens/MainScreen";

function App() {
  return (
    <>
      <Router>
        <AuthProvider>
          <>
            <div className="sticky top-0">
              <NavBar />
            </div>
            <Routes>
              <Route path="/" element={<MainScreen />} />
              <Route path="/title/:slug" element={<TitleScreen />} />
              <Route path="/login" element={<LogInScreen />} />
              <Route path="/signup" element={<SignUpScreen />} />
              <Route path="/gamelist" element={<GameListScreen />} />
              <Route path="/userlist" element={<UserListScreen />} />
            </Routes>
          </>
        </AuthProvider>
      </Router>
    </>
  );
}

export default App;
