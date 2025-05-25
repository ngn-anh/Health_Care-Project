import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import DoctorAppointmentPage from './pages/DoctorAppointmentPage';
import DashboardLayout from './pages/DoctorDashboard';


const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/register" element={<RegisterForm />} />

        {/* Doctor Dashboard Layout */}
        <Route path="/doctor" element={<DashboardLayout />}>
          <Route path="appointments" element={<DoctorAppointmentPage />} />
          {/* Bạn có thể thêm các route khác tại đây như: */}
          {/* <Route path="patients" element={<PatientHistory />} /> */}
        </Route>
      </Routes>
    </Router>
  );
};

export default App;
