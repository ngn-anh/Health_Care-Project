import React, { useEffect, useState } from "react";

const PAYMENT_API = "http://localhost:8002/api/payments/"; // Đổi port nếu cần
const USER_API = "http://localhost:8000/api/users/"; // Đổi port nếu user_service chạy port khác

interface Payment {
    id?: number;
    user_id: number;
    user_name: string;
    amount: number;
    method: string;
    status: string;
    created_at?: string;
    note?: string;
}

const statusOptions = [
    { value: "pending", label: "Chờ xử lý" },
    { value: "completed", label: "Đã thanh toán" },
    { value: "failed", label: "Thất bại" },
    { value: "refunded", label: "Đã hoàn tiền" },
];

const PaymentManagement: React.FC = () => {
    const [users, setUsers] = useState<{ id: number, full_name: string }[]>([]);

    const [search, setSearch] = useState("");
    const [suggestions, setSuggestions] = useState<{ id: number, full_name: string }[]>([]);

    const [payments, setPayments] = useState<Payment[]>([]);
    const [form, setForm] = useState<Payment>({
        user_id: 0,
        user_name: "",
        amount: 0,
        method: "",
        status: "pending",
        note: "",
    });
    const [editingId, setEditingId] = useState<number | null>(null);

    const token = localStorage.getItem("accessToken");

    const fetchPayments = () => {
        fetch(PAYMENT_API, {
            headers: { "Authorization": `Bearer ${token}` }
        })
            .then(res => res.json())
            .then(data => setPayments(data));
    };
    // Lọc danh sách người dùng theo tên khi nhập vào ô tìm kiếm
    useEffect(() => {
        if (search.trim() === "") {
            setSuggestions([]);
            return;
        }
        const filtered = users
            .filter(u => u.full_name.toLowerCase().includes(search.toLowerCase()));
        setSuggestions(filtered);
    }, [search, users]);

    useEffect(() => {
        fetch(USER_API, {
            headers: { "Authorization": `Bearer ${token}` }
        })
            .then(res => res.json())
            .then(data => setUsers(data));
        fetchPayments();
    }, []);

    const handleAddPayment = async (payment: any) => {
        await fetch(PAYMENT_API, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify(payment),
        });
        fetchPayments();
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const method = editingId ? "PUT" : "POST";
        const url = editingId ? `${PAYMENT_API}${editingId}/` : PAYMENT_API;
        await fetch(url, {
            method,
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify(form),
        });
        setEditingId(null);
        setForm({ user_id: 0, user_name: "", amount: 0, method: "", status: "pending", note: "" });
        fetchPayments();
    };

    const handleEdit = (p: Payment) => {
        setEditingId(p.id!);
        setForm({ ...p });
    };

    const handleDelete = async (id?: number) => {
        if (!id) return;
        if (window.confirm("Xóa thanh toán này?")) {
            await fetch(`${PAYMENT_API}${id}/`, {
                method: "DELETE",
                headers: { "Authorization": `Bearer ${token}` }
            });
            fetchPayments();
        }
    };

    return (
        <div className="payment-mgmt-container">
            <h2 className="payment-title">💳 Quản lý thanh toán</h2>

            <div style={{ position: "relative", minWidth: 250, display: "flex", alignItems: "center", gap: 8 }}>
                <input
                    type="text"
                    placeholder="Tìm kiếm bệnh nhân..."
                    value={search}
                    onChange={e => setSearch(e.target.value)}
                    className="form-input"
                    autoComplete="off"
                    style={{ flex: 1 }}
                />
                <button
                    type="button"
                    className="btn-primary"
                    style={{ padding: "8px 16px" }}
                    onClick={() => {
                        // Có thể trigger lại filter hoặc focus vào input
                        if (search.trim() === "") return;
                        const filtered = users.filter(u => u.full_name.toLowerCase().includes(search.toLowerCase()));
                        setSuggestions(filtered);
                    }}
                >
                    Tìm kiếm
                </button>
                {suggestions.length > 0 && (
                    <ul className="suggestion-list">
                        {suggestions.map(u => (
                            <li
                                key={u.id}
                                onClick={() => {
                                    setForm({ ...form, user_id: u.id, user_name: u.full_name });
                                    setSearch(u.full_name);
                                    setSuggestions([]);
                                }}
                            >
                                {u.full_name} (ID: {u.id})
                            </li>
                        ))}
                    </ul>
                )}
            </div>
            <div className="payment-table-wrapper">
                <table className="payment-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Người dùng</th>
                            <th>Số tiền</th>
                            <th>Phương thức</th>
                            <th>Trạng thái</th>
                            <th>Ngày tạo</th>
                            <th>Ghi chú</th>
                            <th>Hành động</th>
                        </tr>
                    </thead>
                    <tbody>
                        {payments.map(p => (
                            <tr key={p.id}>
                                <td>{p.user_id}</td>
                                <td>{p.user_name}</td>
                                <td>{p.amount}</td>
                                <td>{p.method}</td>
                                <td>{statusOptions.find(s => s.value === p.status)?.label}</td>
                                <td>{p.created_at?.slice(0, 10)}</td>
                                <td>{p.note}</td>
                                <td>
                                    <button className="btn-edit" onClick={() => handleEdit(p)}>Sửa</button>
                                    <button className="btn-delete" onClick={() => handleDelete(p.id)}>Xóa</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default PaymentManagement;