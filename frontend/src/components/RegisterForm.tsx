import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './Form.css';

interface FormData {
  full_name: string;
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
  role: string;    
}

const RegisterForm: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    full_name: '',
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'patient',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      alert("Mật khẩu không khớp!");
      return;
    }
    try {
      await axios.post("http://localhost:8000/api/register/", {
        full_name: formData.full_name,
        username: formData.username,
        email: formData.email,
        password: formData.password,
        confirm_password: formData.confirmPassword,
        role: formData.role,
      });
      alert("Đăng ký thành công! Chuyển sang đăng nhập...");
      window.location.href = "/login";
    } catch (err: any) {
      console.error(err.response?.data || err);
      alert("Đăng ký thất bại!");
    }
  };

  return (
    <div className="center-screen">
      <form onSubmit={handleRegister} className="form-container">
        <h2 className="form-title green">📄 Đăng ký tài khoản</h2>
        <input className="form-input" name="full_name" placeholder="Họ tên" onChange={handleChange} />
        <input className="form-input" name="username" placeholder="Tên người dùng" onChange={handleChange} />
        <input className="form-input" name="email" placeholder="Email" onChange={handleChange} />
        <input className="form-input" name="password" type="password" placeholder="Mật khẩu" onChange={handleChange} />
        <input className="form-input" name="confirmPassword" type="password" placeholder="Xác nhận mật khẩu" onChange={handleChange} />
        <select className="select-input" name="role" onChange={handleChange}>
          <option value="patient">Bệnh nhân</option>
          <option value="doctor">Bác sĩ</option>
          <option value="nurse">Y tá</option>
          <option value="pharmacist">Dược sĩ</option>
          <option value="insurance">Nhân viên BHYT</option>
          <option value="lab_tech">Kỹ thuật viên</option>
          <option value="admin">Quản trị viên</option>
        </select>
        <button className="form-button green" type="submit">Đăng ký</button>
        <p className="form-link">Đã có tài khoản? <Link to="/login">Đăng nhập</Link></p>
      </form>
    </div>
  );
};

export default RegisterForm;
