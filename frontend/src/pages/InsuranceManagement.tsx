import React, { useEffect, useState } from "react";
import api from "../axios";
import "../styles/InsuranceManagement.css";

interface InsuranceContract {
  id: number;
  patient_id: number;
  patient_name: string;
  insurance_number: string;
  provider: string;
  start_date: string;
  end_date: string;
  is_active: boolean;
  verified: boolean;
  note?: string;
}

interface InsuranceClaim {
  id: number;
  contract: number;
  amount: number;
  status: string;
  created_at: string;
  processed_at?: string;
  note?: string;
}

const API_BASE = "http://localhost:8004"; // Đổi port nếu insurance_service chạy port khác

const InsuranceManagement: React.FC = () => {
  const [contracts, setContracts] = useState<InsuranceContract[]>([]);
  const [claims, setClaims] = useState<InsuranceClaim[]>([]);
  const [loading, setLoading] = useState(false);


  const fetchContracts = async () => {
    setLoading(true);
    const res = await api.get(`${API_BASE}/contracts/`, { baseURL: undefined });
    setContracts(res.data);
    setLoading(false);
  };

  const fetchClaims = async () => {
    setLoading(true);
    const res = await api.get(`${API_BASE}/claims/`, { baseURL: undefined });
    setClaims(res.data);
    setLoading(false);
  };

  useEffect(() => {
    fetchContracts();
    fetchClaims();
  }, []);


  const handleVerify = async (id: number) => {
    await api.patch(`${API_BASE}/contracts/${id}/`, { verified: true }, { baseURL: undefined });
    fetchContracts();
  };

  const handleApproveClaim = async (id: number) => {
    await api.patch(`${API_BASE}/claims/${id}/`, { status: "approved" }, { baseURL: undefined });
    fetchClaims();
  };

  const handlePayClaim = async (id: number) => {
    await api.patch(`${API_BASE}/claims/${id}/`, { status: "paid", processed_at: new Date().toISOString() }, { baseURL: undefined });
    fetchClaims();
  };

  return (
    <div className="insurance-mgmt-container">
      <h2 className="insurance-title">🛡️ Quản lý bảo hiểm</h2>
      <h3>Hợp đồng bảo hiểm</h3>
      {loading ? <div>Đang tải...</div> : (
        <table className="insurance-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Bệnh nhân</th>
              <th>Số bảo hiểm</th>
              <th>Nhà cung cấp</th>
              <th>Hiệu lực</th>
              <th>Trạng thái</th>
              <th>Xác minh</th>
              <th>Ghi chú</th>
              <th>Hành động</th>
            </tr>
          </thead>
          <tbody>
            {contracts.map(c => (
              <tr key={c.id}>
                <td>{c.id}</td>
                <td>{c.patient_name}</td>
                <td>{c.insurance_number}</td>
                <td>{c.provider}</td>
                <td>{c.start_date} - {c.end_date}</td>
                <td>{c.is_active ? "Hoạt động" : "Hết hiệu lực"}</td>
                <td>{c.verified ? "Đã xác minh" : "Chưa xác minh"}</td>
                <td>{c.note}</td>
                <td>
                  {!c.verified && <button onClick={() => handleVerify(c.id)}>Xác minh</button>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <h3>Yêu cầu bồi thường</h3>
      {loading ? <div>Đang tải...</div> : (
        <table className="insurance-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Hợp đồng</th>
              <th>Số tiền</th>
              <th>Trạng thái</th>
              <th>Ngày tạo</th>
              <th>Ngày xử lý</th>
              <th>Ghi chú</th>
              <th>Hành động</th>
            </tr>
          </thead>
          <tbody>
            {claims.map(claim => (
              <tr key={claim.id}>
                <td>{claim.id}</td>
                <td>{claim.contract}</td>
                <td>{claim.amount}</td>
                <td>{claim.status}</td>
                <td>{claim.created_at?.slice(0, 10)}</td>
                <td>{claim.processed_at?.slice(0, 10) || "-"}</td>
                <td>{claim.note}</td>
                <td>
                  {claim.status === "pending" && <button onClick={() => handleApproveClaim(claim.id)}>Duyệt</button>}
                  {claim.status === "approved" && <button onClick={() => handlePayClaim(claim.id)}>Xác nhận chi trả</button>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default InsuranceManagement;
