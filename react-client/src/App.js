import "./App.css";
import { useState, useEffect } from "react";
import axios from "axios";
import { LoginForm } from "./Components/LoginForm/LoginForm";

function App() {
  const [data, setData] = useState([{}]);
  useEffect(() => {
    axios
      .get("/employee")
      .then((response) => {
        const employees = response.data;
        setData(employees.data);
        console.log(data);
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
  }, []);

  return (
    <>
    <div>
      <LoginForm />
    </div>
    </>
  );
}

// Styling
const styles = {
  container: {
    backgroundColor: "#fff9c4",
    padding: "10px 50px 60px 50px",
  },
  listItem: {
    borderTop: "1px dashed #ccc",
  },
};

export default App;
