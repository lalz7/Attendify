import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    try {
      const res = await axios.post("http://localhost:8000/api/login/", {
        username,
        password,
      });
      localStorage.setItem("access", res.data.access);
      localStorage.setItem("refresh", res.data.refresh);
      setSuccess("Login berhasil!");
      setTimeout(() => {
        navigate("/dashboard");
      }, 1000);
    } catch (err) {
      setError("Username atau password salah!");
    }
  };

  return (
    <div
      className="min-vh-100 d-flex align-items-center justify-content-center"
      style={{
        background: "linear-gradient(135deg, #6a11cb 0%, #2575fc 100%)",
        minHeight: "100vh",
        width: "100vw",
      }}
    >
      <form
        onSubmit={handleSubmit}
        className="bg-white p-5 rounded-4 shadow-lg border-0 w-100"
        style={{ maxWidth: 500 }}
      >
        <div className="text-center mb-4">
          <img
            src="https://getbootstrap.com/docs/5.3/assets/brand/bootstrap-logo-shadow.png"
            alt="Logo"
            width={60}
            className="mb-2"
          />
          <h2 className="fw-bold mb-2 text-primary">Login</h2>
          <p className="text-secondary mb-0">Masuk ke akun Anda</p>
        </div>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="form-control mb-3 py-2"
          autoFocus
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="form-control mb-4 py-2"
        />
        <button
          type="submit"
          className="btn btn-primary w-100 py-2 fw-semibold shadow-sm"
        >
          Login
        </button>
        {error && (
          <div className="alert alert-danger mt-3 py-2 text-center">
            {error}
          </div>
        )}
        {success && (
          <div className="alert alert-success mt-3 py-2 text-center">
            {success}
          </div>
        )}
      </form>
    </div>
  );
}

export default LoginPage;
