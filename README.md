# Health Care Management System

This project is a full-stack web application for healthcare management including user authentication and doctor dashboard functionality.

---

## 🏗 Project Structure
```
Health_Care-Project/
├── backend/         # Django + MongoDB Atlas
├── frontend/        # React + TypeScript + Vite
└── README.md
```

---

## 🚀 1. Backend Setup (Django + MongoDB Atlas)

### 📦 Dependencies
```bash
pip install -r requirements.txt
```

### ✅ MongoDB Atlas Connection
In `backend/settings.py`, make sure the following exists:
```python
from mongoengine import connect

connect(
    db="SAD",
    host="your-mongodb-atlas-uri",
    username="your-username",
    password="your-password"
)
```

### ⚙️ Run the server
```bash
cd backend
python manage.py runserver
```
Server will be live at: [http://localhost:8000](http://localhost:8000)

---

## 🌐 2. Frontend Setup (React + TypeScript + Vite)

### 📦 Install dependencies
```bash
cd frontend
npm install
```

### 🚀 Run the frontend
```bash
npm run dev
```
Frontend will be served at: [http://localhost:5173](http://localhost:5173)

---

## 🧪 API Endpoints (Auth)

### ✅ Register
`POST /api/auth/register/`
```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "abc123",
  "role": "doctor",
  "phone": "0123456789",
  "address": "Hà Nội"
}
```

### ✅ Login
`POST /api/auth/login/`
```json
{
  "username": "alice",
  "password": "abc123"
}
```
Returns `access token` and `user info`.

---

## 📂 Environment Notes
- Django: 5.x
- Database: MongoDB Atlas (via `mongoengine`)
- Frontend: React + TypeScript + Vite
- Authentication: JWT (custom)

---

## ✨ Features
- Đăng ký / đăng nhập người dùng theo vai trò
- Tự động chuyển hướng dashboard theo role
- Dashboard bác sĩ với layout chuẩn admin UI

---

## 📬 Contact
- Dev: [Your Name Here]
- Email: your@email.com
