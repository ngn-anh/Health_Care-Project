import React from "react";
import { Link, useLocation } from "react-router-dom";
import "../../styles/Sidebar.css";

const Sidebar: React.FC = () => {
  const { pathname } = useLocation();

  const navItems = [
    { path: "/doctor/appointments", label: "📅 Quản lý lịch hẹn" },
    { path: "/doctor/patients", label: "👤 Bệnh nhân" },
    { path: "/doctor/diagnosis", label: "🩺 Chẩn đoán & kê đơn" },
    { path: "/doctor/lab-orders", label: "🧪 Yêu cầu xét nghiệm" },
    { path: "/doctor/reports", label: "📝 Báo cáo" },
    { path: "/doctor/results", label: "🔬 Kết quả xét nghiệm" },
    { path: "/doctor/messages", label: "💬 Giao tiếp" },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">🩻 Trang Chủ</div>
      <ul className="nav-list">
        {navItems.map((item) => (
          <li key={item.path} className={pathname === item.path ? "active" : ""}>
            <Link to={item.path}>{item.label}</Link>
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default Sidebar;
