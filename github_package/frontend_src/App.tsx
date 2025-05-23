import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import AuthForm from "./components/AuthForm";
import SilentContributorDashboard from "./components/SilentContributorDashboard";
import "./App.css";

function App() {
  // In a real implementation, this would check for authentication
  const isAuthenticated = false;

  return (
    <Router>
      <Routes>
        <Route path="/auth" element={<AuthForm />} />
        <Route
          path="/dashboard"
          element={
            isAuthenticated ? (
              <SilentContributorDashboard />
            ) : (
              <Navigate to="/auth" replace />
            )
          }
        />
        <Route
          path="/"
          element={
            <Navigate to={isAuthenticated ? "/dashboard" : "/auth"} replace />
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
