import React, { useState, useEffect } from 'react';
import { doctorService } from '../services/doctorService';
import {
  Stethoscope,
  Search,
  Calendar,
  Award,
  IndianRupee,
  Filter,
  Loader2,
  Clock,
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const DoctorsPage = () => {
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDepartment, setSelectedDepartment] = useState('All');
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDoctors = async () => {
      setLoading(true);
      try {
        const res = await doctorService.getAllDoctors();
        const list = Array.isArray(res) ? res : res?.doctors || [];
        setDoctors(list);
      } catch (err) {
        console.error('Failed to load doctors:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchDoctors();
  }, []);

  const departments = ['All', 'Cardiology', 'Neurology', 'Pediatrics', 'Orthopedics', 'Dermatology'];

  const filteredDoctors = doctors.filter((doc) => {
    const matchesSearch =
      doc.specialization?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      doc.department?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      doc.qualification?.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesDept = selectedDepartment === 'All' || doc.department === selectedDepartment;
    return matchesSearch && matchesDept;
  });

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 pt-28 pb-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10">
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-50 border border-brand-200 text-xs font-bold text-brand-700">
            <Stethoscope className="w-3.5 h-3.5" /> Specialist Doctor Directory
          </div>
          <h1 className="text-3xl sm:text-5xl font-extrabold text-slate-900 tracking-tight">
            Hospital Specialist Doctors
          </h1>
          <p className="text-slate-600 text-sm sm:text-base">
            Consult experienced medical specialists across leading clinical departments.
          </p>
        </div>

        {/* Search & Filter Bar */}
        <div className="glass-card rounded-2xl p-4 border border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="relative w-full sm:w-80">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search by department or specialization..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-900 placeholder-slate-400 outline-none focus:border-brand-600"
            />
          </div>

          <div className="flex items-center gap-2 overflow-x-auto w-full sm:w-auto pb-1 sm:pb-0">
            <Filter className="w-4 h-4 text-slate-400 shrink-0 hidden sm:block" />
            {departments.map((dept) => (
              <button
                key={dept}
                onClick={() => setSelectedDepartment(dept)}
                className={`px-3 py-1.5 rounded-xl text-xs font-bold whitespace-nowrap transition-all ${
                  selectedDepartment === dept
                    ? 'bg-brand-600 text-white shadow-sm'
                    : 'bg-slate-100 text-slate-600 hover:text-slate-900 border border-slate-200'
                }`}
              >
                {dept}
              </button>
            ))}
          </div>
        </div>

        {/* Doctors Grid */}
        {loading ? (
          <div className="py-20 text-center">
            <Loader2 className="w-8 h-8 text-brand-600 animate-spin mx-auto mb-2" />
            <p className="text-xs text-slate-500 font-bold">Loading Doctors Directory...</p>
          </div>
        ) : filteredDoctors.length === 0 ? (
          <div className="glass-card rounded-3xl p-12 text-center text-slate-500 space-y-3">
            <Stethoscope className="w-10 h-10 text-slate-300 mx-auto" />
            <h3 className="text-base font-bold text-slate-800">No Doctors Found</h3>
            <p className="text-xs max-w-sm mx-auto">
              There are currently no doctor records matching your search filter.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredDoctors.map((doc, idx) => (
              <div
                key={doc._id || idx}
                className="glass-card rounded-3xl p-6 border border-slate-200 glass-card-hover space-y-4 flex flex-col justify-between"
              >
                <div className="space-y-3">
                  <div className="flex items-start justify-between gap-3">
                    <div className="w-12 h-12 rounded-2xl bg-brand-600 text-white font-bold text-lg flex items-center justify-center shadow-md">
                      DR
                    </div>
                    <span className="px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-[10px] font-bold uppercase tracking-wider">
                      {doc.status || 'Available'}
                    </span>
                  </div>

                  <div>
                    <h3 className="text-lg font-bold text-slate-900 mb-0.5">{doc.specialization}</h3>
                    <p className="text-xs font-bold text-brand-700">{doc.department} Department</p>
                  </div>

                  <div className="space-y-1.5 text-xs text-slate-600 pt-2 border-t border-slate-100">
                    <div className="flex items-center gap-2">
                      <Award className="w-3.5 h-3.5 text-slate-400" />
                      <span>{doc.qualification}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Clock className="w-3.5 h-3.5 text-slate-400" />
                      <span>{doc.experience} Years Experience</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <IndianRupee className="w-3.5 h-3.5 text-emerald-600" />
                      <span className="font-bold text-emerald-700">₹{doc.consultation_fee} Fee</span>
                    </div>
                  </div>
                </div>

                <button
                  onClick={() => {
                    if (!isAuthenticated) {
                      navigate('/signin', { state: { message: 'Sign in to book an appointment' } });
                    } else {
                      navigate('/dashboard');
                    }
                  }}
                  className="w-full mt-4 py-2.5 rounded-xl font-bold text-white bg-brand-600 hover:bg-brand-700 text-xs transition-all flex items-center justify-center gap-2 shadow-sm"
                >
                  <Calendar className="w-4 h-4" /> Book Appointment
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
