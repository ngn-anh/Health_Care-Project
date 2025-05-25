import React from "react";
import { useNavigate } from "react-router-dom";
import "../../styles/Topbar.css";

const Topbar: React.FC = () => {
  const user = JSON.parse(localStorage.getItem("user") || "{}");
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("user");
    navigate("/login");
  };

  return (
    <header className="topbar">
      <div className="search-box">🔍 Search...</div>
      <div className="user-info">
        👨‍⚕️ {user.username}
        <button className="logout-btn" onClick={handleLogout}>
          🚪 Đăng xuất
        </button>
      </div>
    </header>
  );
};

export default Topbar;
