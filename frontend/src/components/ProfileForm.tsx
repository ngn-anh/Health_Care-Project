import React, { useState, useEffect } from "react";
import api from "../axios";

const ProfileForm: React.FC<{ user: any }> = ({ user }) => {
  const [form, setForm] = useState({
    full_name: user.full_name || "",
    email: user.email || "",
    phone_number: user.phone_number || "",
    address: user.address || "",
    date_of_birth: "",
    gender: "",
    insurance_number: "",
  });

  // Lấy thông tin PatientProfile khi load
  useEffect(() => {
    api.get(`http://localhost:8002/api/patient/patient-profile/${user.id}/`)
      .then(res => setForm(f => ({ ...f, ...res.data })))
      .catch(() => {});
  }, [user.id]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const token = localStorage.getItem("accessToken");
    if (!token) {
      alert("Bạn cần đăng nhập lại để cập nhật thông tin cá nhân.");
      window.location.href = "/login";
      return;
    }
    try {
      // Cập nhật user (cần gửi token, api đã tự động thêm Authorization header)
      await api.patch(
        `/users/${user.id}/`,
        {
          full_name: form.full_name,
          email: form.email,
          phone_number: form.phone_number,
          address: form.address,
        }
      );
      // Cập nhật profile (gọi trực tiếp, không cần token)
      await fetch(`http://localhost:8002/api/patient/patient-profile/${user.id}/`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          full_name: form.full_name,
          email: form.email,
          phone_number: form.phone_number,
          address: form.address,
          date_of_birth: form.date_of_birth,
          gender: form.gender,
          insurance_number: form.insurance_number,
        }),
      });
      // Sau khi cập nhật, lấy lại dữ liệu mới nhất từ backend
      const res = await fetch(`http://localhost:8002/api/patient/patient-profile/${user.id}/`);
      if (res.ok) {
        const data = await res.json();
        setForm(f => ({ ...f, ...data }));
      }
      alert("Cập nhật thành công!");
    } catch (err: any) {
      if (err.response && err.response.status === 401) {
        alert("Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.");
        window.location.href = "/login";
      } else {
        alert("Có lỗi xảy ra khi cập nhật thông tin cá nhân.");
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="full_name" value={form.full_name} onChange={handleChange} placeholder="Họ tên" />
      <input name="email" value={form.email} onChange={handleChange} placeholder="Email" />
      <input name="phone_number" value={form.phone_number} onChange={handleChange} placeholder="Số điện thoại" />
      <input name="address" value={form.address} onChange={handleChange} placeholder="Địa chỉ" />
      <input name="date_of_birth" value={form.date_of_birth} onChange={handleChange} placeholder="Ngày sinh" type="date" />
      <input name="gender" value={form.gender} onChange={handleChange} placeholder="Giới tính" />
      <input name="insurance_number" value={form.insurance_number} onChange={handleChange} placeholder="Số bảo hiểm" />
      <button type="submit">Cập nhật</button>
    </form>
  );
};

export default ProfileForm;