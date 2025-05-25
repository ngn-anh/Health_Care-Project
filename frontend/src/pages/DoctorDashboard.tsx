import React from "react";
import { Outlet } from "react-router-dom";
import "../styles/Dashboard.css";
import Sidebar from "../components/doctor/Sidebar";
import Topbar from "../components/doctor/Topbar";

const DashboardLayout: React.FC = () => {
  return (
    <div className="dashboard-container">
      <Sidebar />
      <div className="main-panel">
        <Topbar />
        <div className="dashboard-content">
          <Outlet /> {/* 👈 chỗ render nội dung động */}
        </div>
      </div>
    </div>
  );
};

export default DashboardLayout;
