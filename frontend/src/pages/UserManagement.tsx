import React, { useEffect, useState } from "react";
import api from "../axios";
import "../components/Form.css";

interface User {
  id: string;
  username: string;
  full_name: string;
  email: string;
  phone_number?: string;
  address?: string;
  role: string;
  is_active: boolean;
}

const roleOptions = [
  { value: "patient", label: "Bệnh nhân" },
  { value: "doctor", label: "Bác sĩ" },
  { value: "nurse", label: "Y tá" },
  { value: "pharmacist", label: "Dược sĩ" },
  { value: "lab_tech", label: "Kỹ thuật viên" },
  { value: "insurance", label: "Bảo hiểm" },
  { value: "admin", label: "Quản trị viên" },
];

const initialNewUser: Partial<User> = {
  username: "",
  full_name: "",
  email: "",
  phone_number: "",
  address: "",
  role: "patient",
  is_active: true,
};

const UserManagement: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [newUser, setNewUser] = useState<Partial<User>>(initialNewUser);
  // Lấy danh sách người dùng
  const fetchUsers = async () => {
    const res = await api.get("/users/");
    setUsers(res.data);
  };

  // Thêm người dùng mới
  const handleNewUserChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    setNewUser({ ...newUser, [e.target.name]: e.target.value });
  };

  const handleAddUser = async (e: React.FormEvent) => {
    e.preventDefault();
    if (
      !newUser.username ||
      !newUser.full_name ||
      !newUser.email ||
      !newUser.role
    ) {
      alert("Vui lòng nhập đầy đủ thông tin!");
      return;
    }
    try {
      await api.post("/users/", {
        ...newUser,
        is_active: newUser.is_active !== false,
      });
      setNewUser(initialNewUser);
      fetchUsers();
    } catch (err: any) {
      alert(
        "Thêm người dùng thất bại: " +
          (err.response?.data?.error || "Lỗi không xác định")
      );
    }
  };
  // Xóa người dùng
  useEffect(() => {
    fetchUsers();
  }, []);

  const handleEdit = (user: User) => setEditingUser(user);

  const handleDelete = async (id: string) => {
    if (window.confirm("Xóa người dùng này?")) {
      await api.delete(`/users/${id}/`);
      fetchUsers();
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    if (!editingUser) return;
    setEditingUser({ ...editingUser, [e.target.name]: e.target.value });
  };

  const handleSave = async () => {
    if (!editingUser) return;
    await api.put(`/users/${editingUser.id}/`, editingUser);
    setEditingUser(null);
    fetchUsers();
  };

  return (
    <div className="user-mgmt-container">
      <h2>Quản lý người dùng & vai trò</h2>
      <form
        className="user-form"
        onSubmit={handleAddUser}
        style={{ marginBottom: 20 }}
      >
        <input
          name="full_name"
          placeholder="Họ tên"
          value={newUser.full_name || ""}
          onChange={handleNewUserChange}
        />
        <input
          name="username"
          placeholder="Tên đăng nhập"
          value={newUser.username || ""}
          onChange={handleNewUserChange}
        />
        <input
          name="email"
          placeholder="Email"
          value={newUser.email || ""}
          onChange={handleNewUserChange}
        />
        <input
          name="phone_number"
          placeholder="Số điện thoại"
          value={newUser.phone_number || ""}
          onChange={handleNewUserChange}
        />
        <input
          name="address"
          placeholder="Địa chỉ"
          value={newUser.address || ""}
          onChange={handleNewUserChange}
        />
        <select
          name="role"
          value={newUser.role || "patient"}
          onChange={handleNewUserChange}
        >
          {roleOptions.map((r) => (
            <option key={r.value} value={r.value}>
              {r.label}
            </option>
          ))}
        </select>
        <select
          name="is_active"
          value={newUser.is_active ? "true" : "false"}
          onChange={(e) =>
            setNewUser({ ...newUser, is_active: e.target.value === "true" })
          }
        >
          <option value="true">Hoạt động</option>
          <option value="false">Khóa</option>
        </select>
        <button type="submit">Thêm mới</button>
      </form>
      <table className="user-table">
        <thead>
          <tr>
            <th>Tên</th>
            <th>Tài khoản</th>
            <th>Email</th>
            <th>Vai trò</th>
            <th>Trạng thái</th>
            <th>Hành động</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u) =>
            editingUser?.id === u.id ? (
              <tr key={u.id}>
                <td>
                  <input
                    name="full_name"
                    value={editingUser.full_name}
                    onChange={handleChange}
                  />
                </td>
                <td>
                  <input
                    name="username"
                    value={editingUser.username}
                    onChange={handleChange}
                  />
                </td>
                <td>
                  <input
                    name="email"
                    value={editingUser.email}
                    onChange={handleChange}
                  />
                </td>
                <td>
                  <select
                    name="role"
                    value={editingUser.role}
                    onChange={handleChange}
                  >
                    {roleOptions.map((r) => (
                      <option key={r.value} value={r.value}>
                        {r.label}
                      </option>
                    ))}
                  </select>
                </td>
                <td>
                  <select
                    name="is_active"
                    value={editingUser.is_active ? "true" : "false"}
                    onChange={(e) =>
                      setEditingUser({
                        ...editingUser,
                        is_active: e.target.value === "true",
                      })
                    }
                  >
                    <option value="true">Hoạt động</option>
                    <option value="false">Khóa</option>
                  </select>
                </td>
                <td>
                  <button onClick={handleSave}>Lưu</button>
                  <button onClick={() => setEditingUser(null)}>Hủy</button>
                </td>
              </tr>
            ) : (
              <tr key={u.id}>
                <td>{u.full_name}</td>
                <td>{u.username}</td>
                <td>{u.email}</td>
                <td>{roleOptions.find((r) => r.value === u.role)?.label}</td>
                <td>{u.is_active ? "Hoạt động" : "Khóa"}</td>
                <td>
                  <button onClick={() => handleEdit(u)}>Sửa</button>
                  <button onClick={() => handleDelete(u.id)}>Xóa</button>
                </td>
              </tr>
            )
          )}
        </tbody>
      </table>
    </div>
  );
};

export default UserManagement;
