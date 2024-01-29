import { createContext, useContext, ReactNode, useState } from "react";
import { useNavigate } from "react-router-dom";

interface AuthContextProps {
  token: string | null;
  setToken: (token: string | null) => void;
  logout?: () => void;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [token, setTokenState] = useState<string | null>(() => {
    // Attempt to retrieve token from localStorage during initialization
    const storedToken = localStorage.getItem("token");
    return storedToken || null;
  });
  const navigate = useNavigate();

  const setToken = (newToken: string | null) => {
    setTokenState(newToken);
    // Saving the token to localStorage
    if (newToken) {
      localStorage.setItem("token", newToken);
    } else {
      localStorage.removeItem("token");
    }
  };

  const logout = () => {
    setToken(null);
    navigate("/");
  };

  console.log("Token value:", token);

  return (
    <AuthContext.Provider value={{ token, setToken, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
