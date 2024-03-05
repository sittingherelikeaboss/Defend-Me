import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./Dashboard.css";
import { API_URL } from "../Assets/Constants";
import { useForm } from "react-hook-form";

export const Dashboard = () => {
  const [employeeData, setEmployeeData] = useState([{}]);
  const [scannedData, setScannedData] = useState([{}]);
  const [filterKey, setFilterKey] = useState("device_id");
  const [filterValue, setFilterValue] = useState(undefined);
  const [deviceId, setDeviceId] = useState(undefined);
  const [appVersion, setAppVersion] = useState(undefined);
  const [employeeEmail, setEmployeeEmail] = useState();

  const { register, handleSubmit: handleSubmitScanFilter } = useForm();

  // Here we set which endpoint for employee query to use. Default to the /employee
  const [employeeEndpoint, setEmployeeEndpoint] = useState("/employee");

  const onSubmitScanFilter = async (formData) => {
    setFilterValue(formData["filterValue"]); // TODO: why this isn't working?
    // console.log("filterValue",filterValue);
    // console.log("filterKey",filterKey);
    if (filterKey === "device_id") {
      setDeviceId(filterValue);
      // console.log('deviceId:', deviceId);
    } else if (filterKey === "app_version") {
      setAppVersion(filterValue);
      // console.log('appVersion:', appVersion);
    }
  };

  const onSubmitEmployeeFilter = async (formData) => {
    setEmployeeEmail(formData["email"]);
    if (employeeEmail) { // List all employees by Email Address
      setEmployeeEndpoint(`/employee/email/${employeeEmail}`);
      console.log(employeeEndpoint);
    }
  };

  useEffect(() => {
    console.log("Dashboard::useEffect employee runs");
    axios
      .get(`${API_URL}${employeeEndpoint}`, {
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
  }, [employeeEndpoint]);

  useEffect(() => {
    console.log("Dashboard::useEffect scan runs");
    axios
      .get(`${API_URL}/scan`, {
        params: {
          // secure: false,
          device_id: deviceId,
          app_version: appVersion,
        },
        headers: {
          "Access-Control-Allow-Origins": "*", // Adds CORS header to the request?
          "Content-Type": "application/json",
        },
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
  }, [deviceId]);

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
            <td>{scannedData.length ?? 0}</td>
          </tr>
        </table>
      </div>
      <div className="compromised-devices-header">
        <h2>Scanned Devices</h2>
      </div>
      <form onSubmit={handleSubmitScanFilter(onSubmitScanFilter)}>
        <div className="search-box">
          <input
            placeholder="Filter by attribute here"
            {...register("filterValue")}
          />
          <select
            id="filterKeys"
            value={filterKey}
            onChange={(e) => setFilterKey(e.data.value)}
            defaultValue={"device_id"}
          >
            <option value="device_id">Device ID</option>
            <option value="email">Email Address</option>
            <option value="app_version">App Version</option>
          </select>
          <button type="submit">Enter</button>
        </div>
      </form>
      <div className="compromised-devices-table">
        <table>
          <thead>
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
          </thead>
        </table>
        {/* <button type="previous" onClick={(e) => setPrevious(true)}>Previous</button>
        <button type="next" onClick={(e) => setNext(true)}>Next</button> */}
      </div>

      <div className="compromised-devices-header">
        <h2>Employee List</h2>
      </div>
      <form onSubmit={handleSubmitScanFilter(onSubmitEmployeeFilter)}>
        <div className="compromised-devices-table">
          <input placeholder="Enter email address" {...register("email")} />
          <button type="submit">Enter</button>
          <table>
            <tr>
              <th>Employee ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Created Date</th>
              <th>Updated Date</th>
            </tr>
            {employeeData.map((item, index) => (
              <tr key={index}>
                <td>{item.employee_id}</td>
                <td>{item.name}</td>
                <td>{item.email}</td>
                <td>{item.created_date}</td>
                <td>{item.updated_date}</td>
              </tr>
            ))}
          </table>
        </div>
      </form>
    </>
  );
};
