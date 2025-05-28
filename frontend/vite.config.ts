import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react';
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api/bookings': 'http://localhost:8002', // patient_service
      '/api/patient': 'http://localhost:8002',  // patient_service
      '/api/schedules': 'http://localhost:8001', // schedule_service
      '/api/users': 'http://localhost:8000',    // user_service
      // ... các proxy khác nếu cần
    },
  },
});