import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Dashboard.css";

const DoctorDashboard: React.FC = () => {
  const navigate = useNavigate();
  const [doctor, setDoctor] = useState<any>(null);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (!storedUser) {
      navigate("/login");
      return;
    }
    const user = JSON.parse(storedUser);
    if (user.role !== "doctor") {
      navigate("/");
    } else {
      setDoctor(user);
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("user");
    navigate("/login");
  };

  return (
    <div className="admin-layout">
      <aside className="sidebar">
        <div className="sidebar-header">Trang Chủ</div>
        <ul className="nav-list">
          <li>📅 Quản lý lịch hẹn</li>
          <li>📄 Lịch sử bệnh nhân</li>
          <li>🩺 Chẩn đoán & kê đơn</li>
          <li>🧪 Yêu cầu xét nghiệm</li>
          <li>📝 Báo cáo</li>
          <li>🔬 Kết quả xét nghiệm</li>
          <li>💬 Giao tiếp</li>
          <li onClick={handleLogout} className="logout">🚪 Đăng xuất</li>
        </ul>
      </aside>
      <div className="main-panel">
        <header className="topbar">
          <input type="text" placeholder="Search for..." className="search-box" />
          <div className="user-info">👤 {doctor?.username}</div>
        </header>

        <main className="dashboard-content">
          <h2 className="dashboard-title">Bảng điều khiển</h2>
          <div className="cards">
            <div className="card">Earnings (Monthly): $40,000</div>
            <div className="card">Earnings (Annual): $215,000</div>
            <div className="card">Tasks: 50%</div>
            <div className="card">Pending Requests: 18</div>
          </div>

          <div className="widgets">
            <div className="widget">📈 Biểu đồ thống kê</div>
            <div className="widget">📊 Nguồn doanh thu</div>
            <div className="widget">🧾 Danh sách việc cần làm</div>
            <div className="widget">🧍 Minh họa người dùng</div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default DoctorDashboard;