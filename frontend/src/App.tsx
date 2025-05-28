import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import DoctorDashboard from './pages/DoctorDashboard';
import AdminDashboard from './pages/AdminDashboard';
import UserManagement from './pages/UserManagement';
import ScheduleManagement from './pages/ScheduleManagement';
import PaymentManagement from './pages/PaymentManagement';

import PatientDashboard from './pages/PatientDashboard';
import InsuranceManagement from './pages/InsuranceManagement';


const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/register" element={<RegisterForm />} />
        <Route path="/doctor" element={<DoctorDashboard />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/admin/users" element={<UserManagement />} />
        <Route path="/admin/schedule" element={<ScheduleManagement />} />
        <Route path="/admin/payments" element={<PaymentManagement />} />
        <Route path="/admin/insurance" element={<InsuranceManagement />} />
        <Route path="/patient" element={<PatientDashboard />} />
      </Routes>
    </Router>
  );
};

export default App;
