
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Dashboard.css";


const PatientDashboard: React.FC = () => {
  const navigate = useNavigate();
  const [patient, setPatient] = useState<any>(null);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (!storedUser) {
      navigate("/login");
      return;
    }
    const user = JSON.parse(storedUser);
    if (user.role !== "patient") {
      navigate("/");
    } else {
      setPatient(user);
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
        <div className="sidebar-header">🧑‍⚕️ Bệnh nhân</div>
        {/* <ul className="nav-list">
          <li onClick={() => setSelectedMenu("book")}>📅 Đặt lịch khám</li>
          <li onClick={() => setSelectedMenu("profile")}>📁 Hồ sơ bệnh án</li>
          <li onClick={() => setSelectedMenu("prescription")}>💊 Đơn thuốc</li>
          <li onClick={() => setSelectedMenu("payment")}>💳 Thanh toán hóa đơn</li>
          <li onClick={() => setSelectedMenu("report")}>🧪 Báo cáo xét nghiệm</li>
          <li onClick={() => setSelectedMenu("update")}>📝 Cập nhật thông tin cá nhân</li>
          <li onClick={handleLogout} className="logout">🚪 Đăng xuất</li>
        </ul> */}
        <ul className="nav-list">
          <li>
            📅 Đặt lịch khám
          </li>
          <li>
            <li>
                📁 Hồ sơ bệnh án
            </li>
          </li>
          <li>
          
              💊 Đơn thuốc
  
          </li>
          <li>🧪 Báo cáo xét nghiệm</li>
          <li>📝 Cập nhật thông tin cá nhân</li>
          <li onClick={handleLogout} className="logout">🚪 Đăng xuất</li>
        </ul>
      </aside>

      <div className="main-panel">
        <header className="topbar">
          <input type="text" placeholder="Tìm kiếm..." className="search-box" />
          <div className="user-info">👤 {patient?.username}</div>
        </header>
        <main className="dashboard-content">
          <h2 className="dashboard-title">Bảng điều khiển bệnh nhân</h2>
          <div className="cards">
                <div className="card">Lịch khám sắp tới</div>
                <div className="card">Hóa đơn chưa thanh toán</div>
                <div className="card">Đơn thuốc mới</div>
                <div className="card">Báo cáo xét nghiệm gần nhất</div>
              </div>
          {/* Có thể thêm các menu khác tương tự */}
        </main>
      </div>
    </div>
  );
};

export default PatientDashboard;
