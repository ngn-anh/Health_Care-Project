import React, { useEffect, useState } from "react";
import api from "../api/axios_doctor";
import "../styles/DoctorAppointment.css";

interface Appointment {
  id?: string;
  patient: any;
  datetime: string;
  description: string;
  status: string;
}

const DoctorAppointmentPage: React.FC = () => {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [patients, setPatients] = useState<any[]>([]);
  const [formData, setFormData] = useState<Appointment>({
    patient: "",
    datetime: "",
    description: "",
    status: "pending",
  });
  const [editingId, setEditingId] = useState<string | null>(null);

  const fetchAppointments = async () => {
    try {
      const [resAppointments, resPatients] = await Promise.all([
        api.get("/doctor/appointments/"),
        api.get("/doctor/patients/")
      ]);
      setAppointments(resAppointments.data);
      setPatients(resPatients.data);
    } catch (error) {
      alert("Không thể tải dữ liệu lịch hẹn hoặc bệnh nhân.");
    }
  };

  useEffect(() => {
    fetchAppointments();
  }, []);

  const formatForDatetimeInput = (iso: string) => {
    const date = new Date(iso);
    const pad = (n: number) => n.toString().padStart(2, "0");

    const year = date.getFullYear();
    const month = pad(date.getMonth() + 1);
    const day = pad(date.getDate());
    const hour = pad(date.getHours());
    const min = pad(date.getMinutes());

    return `${year}-${month}-${day}T${hour}:${min}`; // Format chuẩn cho input
    };


  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingId) {
        await api.put(`/doctor/appointments/${editingId}/`, formData);
      } else {
        await api.post("/doctor/appointments/", formData);
      }
      setFormData({ patient: "", datetime: "", description: "", status: "pending" });
      setEditingId(null);
      fetchAppointments();
    } catch (error) {
      alert("Không thể lưu lịch hẹn.");
    }
  };

  const handleEdit = (appt: Appointment) => {
    console.log('appt',appt)
    setFormData({
        patient: appt.patient.id,
        datetime: formatForDatetimeInput(appt.datetime),
        description: appt.description,
        status: appt.status,
    });
    setEditingId(appt.id || null);
    };

  const handleDelete = async (id: string) => {
    if (window.confirm("Bạn có chắc muốn xóa lịch hẹn này không?")) {
      await api.delete(`/doctor/appointments/${id}/`);
      fetchAppointments();
    }
  };

  const formatDateTimeVN = (isoString: string) => {
    const date = new Date(isoString);
    const pad = (n: number) => n.toString().padStart(2, "0");
    const hours = pad(date.getHours());
    const minutes = pad(date.getMinutes());
    const seconds = pad(date.getSeconds());
    const day = pad(date.getDate());
    const month = pad(date.getMonth() + 1);
    const year = date.getFullYear();
    return `${hours}:${minutes}:${seconds} ${day}/${month}/${year}`;
  };

  return (
    <div className="appointment-container">
      <h2 className="title">📅 Danh sách lịch hẹn của tôi</h2>

      <form onSubmit={handleSubmit} className="appointment-form">
        <select
          name="patient"
          value={formData.patient}
          onChange={handleChange}
          required
        >
          <option value="">-- Chọn bệnh nhân --</option>
          {patients.map((p) => (
            <option key={p.id} value={p.id}>
              {p.username} ({p.email})
            </option>
          ))}
        </select>
        <input name="datetime" type="datetime-local" value={formData.datetime} onChange={handleChange} required />
        <input name="description" placeholder="Mô tả" value={formData.description} onChange={handleChange} required />
        <select name="status" value={formData.status} onChange={handleChange}>
          <option value="pending">Pending</option>
          <option value="confirmed">Confirmed</option>
          <option value="cancelled">Cancelled</option>
        </select>
        <button type="submit">{editingId ? "Cập nhật" : "Thêm"}</button>
      </form>

      <table className="appointment-table">
        <thead>
          <tr>
            <th>Ngày giờ</th>
            <th>Bệnh nhân</th>
            <th>Mô tả</th>
            <th>Trạng thái</th>
            <th>Hành động</th>
          </tr>
        </thead>
        <tbody>
          {appointments.map((a) => (
            <tr key={a.id}>
              <td>{formatDateTimeVN(a.datetime)}</td>
              <td>{a.patient?.username || a.patient}</td>
              <td>{a.description}</td>
              <td>{a.status}</td>
              <td>
                <button onClick={() => handleEdit(a)}>Sửa</button>
                <button onClick={() => handleDelete(a.id!)}>Xóa</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DoctorAppointmentPage;
