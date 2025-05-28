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
      // Lấy JWT token
      const res = await axios.post("http://localhost:8000/api/token/", {
        username,
        password,
      });
      localStorage.setItem("accessToken", res.data.access);

      // Lấy thông tin user
      const userRes = await axios.get("http://localhost:8000/api/me/", {
        headers: {
          Authorization: `Bearer ${res.data.access}`,
        },
      });
      localStorage.setItem("user", JSON.stringify(userRes.data));

      alert("Đăng nhập thành công!");

      // Sau khi đăng nhập thành công và đã có user info:
      const user = userRes.data;
      localStorage.setItem("user", JSON.stringify(user));

      // // Gọi API tạo profile (chỉ cần gọi, backend sẽ tự kiểm tra tồn tại)
      // if (user.role === "patient") {
      //   fetch("http://localhost:8002/api/patient/create-profile/", {
      //     method: "POST",
      //     headers: { "Content-Type": "application/json" },
      //     body: JSON.stringify({ user_id: user.id }),
      //   });
      // }

      // Điều hướng theo role
      const role = userRes.data.role;
      if (role === "doctor") {
        window.location.href = "/doctor";
      } else if (role === "patient") {
        window.location.href = "/patient";
      } else if (role === "admin") {
        window.location.href = "/admin";
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