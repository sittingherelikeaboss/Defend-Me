import "./App.css";

// importing components from react-router-dom package
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

// Import LoginForm component
import { LoginForm } from "./Components/LoginForm/LoginForm";

import { Dashboard } from "./Components/Dashboard/Dashboard";

function App() {
  
  return (
    <>
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
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
