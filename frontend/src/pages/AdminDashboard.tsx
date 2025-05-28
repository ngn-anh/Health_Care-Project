import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Dashboard.css";
import { Link } from "react-router-dom";

const AdminDashboard: React.FC = () => {
  const navigate = useNavigate();
  const [admin, setAdmin] = useState<any>(null);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (!storedUser) {
      navigate("/login");
      return;
    }
    const user = JSON.parse(storedUser);
    if (user.role !== "admin") {
      navigate("/"); // không phải admin, chuyển hướng về trang chủ
    } else {
      setAdmin(user);
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
        <div className="sidebar-header">👑 Quản trị viên</div>
        <ul className="nav-list">
          <li>
            <Link to="/admin/users" style={{ color: "inherit", textDecoration: "none" }}>
              👥 Quản lý người dùng và vai trò
            </Link>
          </li>
          <li>
            <li>
              <Link to="/admin/schedule" style={{ color: "inherit", textDecoration: "none" }}>
                📅 Lên lịch bác sĩ và y tá
              </Link>
            </li>
          </li>
          <li>
            <Link to="/admin/payments" style={{ color: "inherit", textDecoration: "none" }}>
              💳 Quản lý thanh toán
            </Link>
          </li>
          <li>
            <Link to="/admin/insurance" style={{ color: "inherit", textDecoration: "none" }}>
              🛡️ Xử lý bảo hiểm
            </Link>
          </li>
          <li onClick={handleLogout} className="logout">🚪 Đăng xuất</li>
        </ul>
      </aside>

      <div className="main-panel">
        <header className="topbar">
          <input type="text" placeholder="Tìm kiếm..." className="search-box" />
          <div className="user-info">👤 {admin?.username}</div>
        </header>

        <main className="dashboard-content">
          <h2 className="dashboard-title">Bảng điều khiển quản trị</h2>
          <div className="cards">
            <div className="card">Người dùng: 1234</div>
            <div className="card">Bác sĩ: 56</div>
            <div className="card">Y tá: 34</div>
            <div className="card">Yêu cầu thanh toán: 12</div>
          </div>

          <div className="widgets">
            <div className="widget">📋 Danh sách người dùng</div>
            <div className="widget">📅 Lịch làm việc</div>
            <div className="widget">💰 Báo cáo thanh toán</div>
            <div className="widget">🛡️ Trạng thái bảo hiểm</div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default AdminDashboard;
