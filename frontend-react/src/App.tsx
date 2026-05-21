import { useState } from "react";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import { clearTokens, getAccessToken } from "./auth/storage";

export default function App() {
  const [authenticated, setAuthenticated] = useState(Boolean(getAccessToken()));

  function handleLogout() {
    clearTokens();
    setAuthenticated(false);
  }

  if (!authenticated) {
    return <Login onLogin={() => setAuthenticated(true)} />;
  }

  return <Dashboard onLogout={handleLogout} />;
}
