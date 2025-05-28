import React, { useEffect, useState } from "react";
import api from "../axios";
import "../styles/Dashboard.css";

interface Schedule {
    id?: number;
    staff_id: number;
    staff_name?: string;
    role: string;
    date: string;
    start_time: string;
    end_time: string;
    note?: string;
}

interface User {
    id: number;
    full_name: string;
    role: string;
}

const SCHEDULE_API = "http://localhost:8001/api/schedules/";

const ScheduleManagement: React.FC = () => {
    const [schedules, setSchedules] = useState<Schedule[]>([]);
    const [users, setUsers] = useState<User[]>([]);
    const [form, setForm] = useState<Schedule>({
        staff_id: 0,
        role: "doctor",
        date: "",
        start_time: "",
        end_time: "",
        note: "",
    });
    const [editingId, setEditingId] = useState<number | null>(null);

    useEffect(() => {
        api.get("/users/").then(res => {
            setUsers(res.data.filter((u: User) => u.role === "doctor" || u.role === "nurse"));
        });
        fetchSchedules();
    }, []);

    const fetchSchedules = () => {
        fetch(SCHEDULE_API)
            .then(res => res.json())
            .then(data => setSchedules(data));
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const selectedUser = users.find(u => u.id === Number(form.staff_id));
        if (!selectedUser) return;
        const payload = {
            ...form,
            staff_id: Number(form.staff_id),
            staff_name: selectedUser.full_name,
            role: selectedUser.role,
        };
        if (editingId) {
            await fetch(`${SCHEDULE_API}${editingId}/`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });
            setEditingId(null);
        } else {
            await fetch(SCHEDULE_API, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });
        }
        setForm({ staff_id: 0, role: "doctor", date: "", start_time: "", end_time: "", note: "" });
        fetchSchedules();
    };

    const handleEdit = (s: Schedule) => {
        setEditingId(s.id!);
        setForm({
            staff_id: s.staff_id,
            role: s.role,
            date: s.date,
            start_time: s.start_time,
            end_time: s.end_time,
            note: s.note || "",
        });
    };

    const handleDelete = async (id?: number) => {
        if (!id) return;
        if (window.confirm("Xóa lịch này?")) {
            await fetch(`${SCHEDULE_API}${id}/`, { method: "DELETE" });
            fetchSchedules();
        }
    };

    // lọc lịch theo ngày, vai trò và nhân viên
    const [filter, setFilter] = useState({ date: "", role: "", staff_id: "" });

    const filteredSchedules = schedules.filter(s => {
        return (!filter.date || s.date === filter.date)
            && (!filter.role || s.role === filter.role)
            && (!filter.staff_id || String(s.staff_id) === filter.staff_id);
    });

    return (
        <div className="schedule-mgmt-container">
            <h2 className="schedule-title">Lên lịch cho bác sĩ và y tá</h2>
            <form className="schedule-form" onSubmit={handleSubmit} style={{ marginBottom: 20 }}>
                <select name="staff_id" value={form.staff_id} onChange={handleChange} required>
                    <option value="">Chọn nhân viên</option>
                    {users.map(u => (
                        <option key={u.id} value={u.id}>{u.full_name} ({u.role === "doctor" ? "Bác sĩ" : "Y tá"})</option>
                    ))}
                </select>
                <input type="date" name="date" value={form.date} onChange={handleChange} required />
                <input type="time" name="start_time" value={form.start_time} onChange={handleChange} required />
                <input type="time" name="end_time" value={form.end_time} onChange={handleChange} required />
                <input name="note" placeholder="Ghi chú" value={form.note} onChange={handleChange} />
                <button className="btn-primary" type="submit">{editingId ? "Cập nhật" : "Thêm lịch"}</button>
                {editingId && <button className="btn-cancel" type="button" onClick={() => { setEditingId(null); setForm({ staff_id: 0, role: "doctor", date: "", start_time: "", end_time: "", note: "" }); }}>Hủy</button>}
            </form>
            <div className="schedule-filter" style={{ marginBottom: 10 }}>
                <input type="date" value={filter.date} onChange={e => setFilter({ ...filter, date: e.target.value })} />
                <select value={filter.role} onChange={e => setFilter({ ...filter, role: e.target.value })}>
                    <option value="">Tất cả vai trò</option>
                    <option value="doctor">Bác sĩ</option>
                    <option value="nurse">Y tá</option>
                </select>
                <select value={filter.staff_id} onChange={e => setFilter({ ...filter, staff_id: e.target.value })}>
                    <option value="">Tất cả nhân viên</option>
                    {users.map(u => (
                        <option key={u.id} value={u.id}>{u.full_name}</option>
                    ))}
                </select>
            </div>
            <table className="schedule-table">
                <thead>
                    <tr>
                        <th>Nhân viên</th>
                        <th>Vai trò</th>
                        <th>Ngày</th>
                        <th>Bắt đầu</th>
                        <th>Kết thúc</th>
                        <th>Ghi chú</th>
                        <th>Hành động</th>
                    </tr>
                </thead>
                <tbody>
                    {schedules.map(s => (
                        <tr key={s.id}>
                            <td>{s.staff_name}</td>
                            <td>{s.role === "doctor" ? "Bác sĩ" : "Y tá"}</td>
                            <td>{s.date}</td>
                            <td>{s.start_time}</td>
                            <td>{s.end_time}</td>
                            <td>{s.note}</td>
                            <td>
                                <button onClick={() => handleEdit(s)}>Sửa</button>
                                <button onClick={() => handleDelete(s.id)}>Xóa</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default ScheduleManagement;