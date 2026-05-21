import { FormEvent, useState } from "react";
import { api } from "../api/client";
import { setTokens } from "../auth/storage";

interface Props {
  onLogin: () => void;
}

export default function Login({ onLogin }: Props) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const response = await api.post("/auth/login", { username, password });
      setTokens(response.data.access_token, response.data.refresh_token);
      onLogin();
    } catch {
      setError("Credenciales invalidas");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 320, margin: "80px auto", fontFamily: "sans-serif" }}>
      <h2>Iniciar sesion</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 12 }}>
          <input
            placeholder="Usuario"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{ width: "100%", padding: 8 }}
          />
        </div>
        <div style={{ marginBottom: 12 }}>
          <input
            type="password"
            placeholder="Contrasena"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ width: "100%", padding: 8 }}
          />
        </div>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit" disabled={loading} style={{ width: "100%", padding: 8 }}>
          {loading ? "Ingresando..." : "Ingresar"}
        </button>
      </form>
    </div>
  );
}
