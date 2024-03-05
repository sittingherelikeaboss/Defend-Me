import React, { useState, useEffect } from "react";
import axios from "axios";
import "./Dashboard.css";
import { API_URL } from "../Assets/Constants";

export const Dashboard = () => {
  const [employeeData, setEmployeeData] = useState([{}]);
  const [scannedData, setScannedData] = useState([{}]);

  useEffect(() => {
    axios
      .get(`${API_URL}/employee`, {
        headers: {
          "Access-Control-Allow-Origins": "*", // Adds CORS header to the request?
          "Content-Type": "application/json",
        },
      })
      .then((response) => {
        const employees = response.data;
        setEmployeeData(employees.data);
      })
      .catch((error) => {
        // Error
        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          // console.log(error.response.data);
          console.log(error.response.status);
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

  useEffect(() => {
    axios
      .get(`${API_URL}/scan`, {
        params: {
          secure: false,
        },
        headers: {
          "Access-Control-Allow-Origins": "*", // Adds CORS header to the request?
          "Content-Type": "application/json",
        }
      })
      .then((response) => {
        const scanned = response.data;
        setScannedData(scanned.data);
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
      <div className="main-header">
        <h1>Hello World LLC Dashboard</h1>
      </div>
      <div className="statistics">
        <h2>Current Report</h2>
        <table>
          <tr>
            <th>Employees</th>
            <th>Devices Scanned</th>
            <th>Compromised Devices</th>
          </tr>
          <tr>
            <td>{employeeData.length}</td>
            <td>10000</td>
            <td>{scannedData.length}</td>
          </tr>
        </table>
      </div>
      <div className="compromised-devices-header">
        <h2>Compromised Devices</h2>
      </div>
      <div className="search-box">
          <input placeholder="Type search criteria here"></input>
          <select name="cars" id="cars">
            <option value="email">Email Address</option>
            <option value="device_id">Device ID</option>
            <option value="app_version">App Version</option>
          </select>
        </div>
      <div className="compromised-devices-table">
        <table>
          <tr>
            <th>Device ID</th>
            <th>App Version</th>
            <th>OS Version</th>
            <th>Threats</th>
            <th>Threat Detected</th>
          </tr>
          {scannedData.map((item, index) => (
            <tr key={index}>
              <td>{item.device_id}</td>
              <td>{item.app_version}</td>
              <td>{item.os_version}</td>
              <td>{item.threats}</td>
              <td>{item.created_date}</td>
            </tr>
          ))}
        </table>
      </div>
    </>
  );
};
