import React from "react";

export const Dashboard = () => {
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
      <div style={styles.container}>
        <h1>👋 Hello World LLC Dashboard</h1>
        <h2>Employee List</h2>
        <tr>
          <th>Name</th>
          <th>Email</th>
        </tr>
        {data.map((item, index) => (
          <tr key={index}>
            <td>{item.name}</td>
            <td>{item.email}</td>
          </tr>
        ))}
      </div>
    </>
  );
};
