import React, { useState } from "react";
import "./LoginForm.css";
import { FaUser, FaLock } from "react-icons/fa";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";

export const LoginForm = () => {
  const navigate = useNavigate();

  const { register, handleSubmit } = useForm();
  const onSubmit = async (formData) => {
    console.log(formData);
    const email = formData["email"];
    const password = formData["password"];
    // const rememberMe = data["rememberMe"]; // TODO: Use this to remember email/password
    axios
      .get("/employee/validate/" + email.toLowerCase(), {
        params: {
          password: password,
        },
      })
      .then((response) => {
        // setData(response.data);
        const data = response.data;
        console.log("Password matches " + data["passwordMatches"]);
        if (data["passwordMatches"] === undefined) {
          
        } else if (data["passwordMatches"] === true) {
          navigate("/dashboard");
        }
      })
      .catch((error) => {
        // Error
        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          // console.log(error.response.data);
          // console.log(error.response.status);
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
        console.log(error.config);
      });
  };

  return (
    <div className="wrapper">
      <form onSubmit={handleSubmit(onSubmit)}>
        <h1>⚔️ Defend Me</h1>
        <div className="input-box">
          <input {...register("email")}
            type="email"
            placeholder="Email"
            required
          />
          <FaUser className="icon" />
        </div>
        <div className="input-box">
          <input {...register("password")}
            type="password"
            placeholder="Password"
            required
          />
          <FaLock className="icon" />
        </div>

        <div className="remember-forgot">
          <label>
            <input {...register("rememberMe")}
              type="checkbox"
            />
            Remember me
          </label>
          <a href="#">Forgot password?</a>
        </div>

        <button type="submit">Login</button>

        {/* <div className="register-link">
          <p>
            Don't have an account? <a href="#">Register</a>
          </p>
        </div> */}
      </form>
    </div>
  );
};

export default LoginForm;
