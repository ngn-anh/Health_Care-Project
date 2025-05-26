import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './Form.css';

const LoginForm: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
  try {
    const res = await axios.post("http://localhost:7000/api/auth/login/", {
      username,
      password,
    });

    localStorage.setItem("accessToken", res.data.access);
    localStorage.setItem("user", JSON.stringify(res.data.user));

    alert("Đăng nhập thành công!");

    // Điều hướng theo role
    const role = res.data.user.role;
    if (role === "doctor") {
      window.location.href = "/doctor";
    } else if (role === "patient") {
      window.location.href = "/patient";
    } else {
      window.location.href = "/";
    }
  } catch {
    alert("Đăng nhập thất bại!");
  }
  };

  return (
    <div className="center-screen">
      <form onSubmit={handleLogin} className="form-container">
        <h2 className="form-title blue">🔒 Đăng nhập</h2>
        <input className="form-input" placeholder="Tên đăng nhập" value={username} onChange={(e) => setUsername(e.target.value)} />
        <input className="form-input" type="password" placeholder="Mật khẩu" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button className="form-button blue" type="submit">Đăng nhập</button>
        <p className="form-link">Chưa có tài khoản? <Link to="/register">Đăng ký</Link></p>
      </form>
    </div>
  );
};

export default LoginForm;