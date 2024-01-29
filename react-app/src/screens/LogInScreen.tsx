import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../AuthContext.tsx";

const LogInScreen = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();
  const { setToken } = useAuth();

  const handleUsernameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUsername(e.target.value);
  };

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
  };

  const handleLogIn = async () => {
    console.log("Logging in with:", username, password);
    try {
      const response = await fetch("http://localhost:8000/api/login/", {
        method: "POST",
        headers: {
          accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });

      console.log("Response:", response);

      if (response.ok) {
        const { token } = await response.json();
        setToken(token);
        console.log("User successfully Logged In");
        navigate("/");
      } else {
        const errorData = await response.json();
        console.error("LogIn failed:", errorData);
        setErrorMessage("Log in failed. Please try again.");
      }
    } catch (error) {
      console.error("Error during login:", error);
    }
  };

  return (
    <div className="flex justify-center mt-20">
      <div className="w-1/5 flex flex-col ">
        <label className="ml-4 text-sm font-medium text-gray-700">
          Username
        </label>
        <input
          type="text"
          id="usernameInput"
          className="mt-1 p-2 border border-gray-300 rounded-md"
          placeholder="Enter username"
          value={username}
          onChange={handleUsernameChange}
        />

        <label className="ml-4 mt-4 text-sm font-medium text-gray-700">
          Password
        </label>
        <input
          type="password"
          id="passwordInput"
          className="mt-1 p-2 border border-gray-300 rounded-md"
          placeholder="Enter password"
          value={password}
          onChange={handlePasswordChange}
        />

        {errorMessage && <p className="text-red-500 mt-2">{errorMessage}</p>}

        <button
          className="bg-blue-500 text-white p-2 rounded-md mt-10"
          onClick={handleLogIn}
        >
          Log In
        </button>
      </div>
    </div>
  );
};

export default LogInScreen;
