import React, { useState, useContext, createContext } from "react";
import "./LoginForm.css";
import { FaUser, FaLock } from "react-icons/fa";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { API_URL } from "../Assets/Constants";

const AuthContext = createContext();
export const AuthData = () => useContext(AuthContext);

export const LoginForm = () => {
  const navigate = useNavigate();
  const { register, handleSubmit } = useForm();
  const [showError, setShowError] = useState(false);

  const onSubmit = async (formData) => {
    const email = formData["email"];
    const password = formData["password"];

    axios
      .post(`${API_URL}/login`, {
        email: email,
        password: password,
      }, {
        headers: {
          "Access-Control-Allow-Origins": "*", // Adds CORS header to the request?
          "Content-Type": "application/json",
        },
      })
      .then((response) => {
        const responseBody = response.data;
        console.log("Access Token: " + responseBody["access_token"]);
        if (responseBody["access_token"] !== undefined) {
          console.log("Let's navigate to /dashboard!");
          navigate("/dashboard");
        } else {
          console.log("showError: " + showError);
        }
      })
      .catch((error) => {
        // Error
        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          // console.log(error.response.data);
          console.log(error.response.status);
          setShowError(true);
          console.log("showError: " + showError);
          // console.log(error.response.headers);
        } else if (error.request) {
          // The request was made but no response was received
          // `error.request` is an instance of XMLHttpRequest in the
          // browser and an instance of
          // http.ClientRequest in node.js
          console.log(error.request);
        } else {
          // Something happened in setting up the request that triggered an Error
          console.log("Error", error.message);
        }
      });
  };

  return (
    <div className="login-wrapper">
      <form onSubmit={handleSubmit(onSubmit)}>
        <h1>⚔️ Defend Me</h1>
        <div className="input-box">
          <input
            {...register("email")}
            type="email"
            placeholder="Email"
            required
          />
          <FaUser className="icon" />
        </div>
        <div className="input-box">
          <input
            {...register("password")}
            type="password"
            placeholder="Password"
            required
          />
          <FaLock className="icon" />
          <span>{showError && "Invalid email or password"}</span>
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default LoginForm;
