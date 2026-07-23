import React from 'react';
import { useAuth } from '../context/AuthContext';
import { AdminDashboard } from '../components/dashboard/AdminDashboard';
import { DoctorDashboard } from '../components/dashboard/DoctorDashboard';
import { PatientDashboard } from '../components/dashboard/PatientDashboard';

export const DashboardPage = () => {
  const { role } = useAuth();

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 pt-28 pb-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {role === 'admin' && <AdminDashboard />}
        {role === 'doctor' && <DoctorDashboard />}
        {role === 'patient' && <PatientDashboard />}
        {!['admin', 'doctor', 'patient'].includes(role) && <PatientDashboard />}
      </div>
    </div>
  );
};
