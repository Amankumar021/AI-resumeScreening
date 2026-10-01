import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Login() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [isRegistering, setIsRegistering] = useState(false);

  const handleLogin = async (event) => {
    event.preventDefault();

    if (!username || !password) {
      setMessage("Please enter username and password.");
      return;
    }

    try {
      setLoading(true);
      setMessage("");

      if (isRegistering) {
        await api.post("/auth/register", {
          username,
          password
        });
      }

      const response = await api.post("/auth/login", {
        username,
        password
      });

      localStorage.setItem(
        "token",
        response.data.access_token
      );

      localStorage.setItem(
        "username",
        username
      );

      navigate("/");
    } catch (error) {
      console.error(error);

      setMessage(
        error.response?.data?.detail ||
        (isRegistering ? "Account creation failed." : "Login failed.")
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">

      <div className="login-card">

        <h1>AI Resume Screening</h1>

        <p className="login-subtitle">
          {isRegistering ? "Create a recruiter account" : "Recruiter Login"}
        </p>

        <form onSubmit={handleLogin}>

          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(event) =>
              setUsername(event.target.value)
            }
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(event) =>
              setPassword(event.target.value)
            }
          />

          <button
            type="submit"
            disabled={loading}
          >
            {loading
              ? (isRegistering ? "Creating account..." : "Logging in...")
              : (isRegistering ? "Create account" : "Login")}
          </button>

        </form>

        <p className="login-message">
          {isRegistering ? "Already have an account?" : "Need an account?"}{" "}
          <button
            type="button"
            onClick={() => {
              setIsRegistering(!isRegistering);
              setMessage("");
            }}
          >
            {isRegistering ? "Login" : "Register"}
          </button>
        </p>

        {message && (
          <p className="login-message">
            {message}
          </p>
        )}

      </div>

    </div>
  );
}

export default Login;