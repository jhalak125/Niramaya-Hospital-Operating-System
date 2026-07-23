import React, { useState, useEffect } from 'react';
import { dashboardService } from '../../services/dashboardService';
import { doctorService } from '../../services/doctorService';
import { patientService } from '../../services/patientService';
import { appointmentService } from '../../services/appointmentService';
import { medicalService } from '../../services/medicalService';
import { useAuth } from '../../context/AuthContext';
import {
  Users,
  Stethoscope,
  Calendar,
  IndianRupee,
  Activity,
  FileText,
  UserPlus,
  ShieldCheck,
  Search,
  AlertCircle,
  Loader2,
  CheckCircle2,
  Receipt,
  X
} from 'lucide-react';

export const AdminDashboard = () => {
  const { user } = useAuth();
  const [metrics, setMetrics] = useState(null);
  const [doctorsList, setDoctorsList] = useState([]);
  const [patientsList, setPatientsList] = useState([]);
  const [appointmentsList, setAppointmentsList] = useState([]);
  const [billsList, setBillsList] = useState([]);
  const [paymentsList, setPaymentsList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview'); // overview | doctors | patients | appointments | bills

  const fetchAdminData = async () => {
    setLoading(true);
    setErrorMsg('');
    try {
      const data = await dashboardService.getAdminDashboard();
      setMetrics(data);

      const [docsRes, patsRes, apptsRes, billsRes] = await Promise.allSettled([
        doctorService.getAllDoctors(),
        patientService.getAllPatients(),
        appointmentService.getAllAppointments(),
        medicalService.getAllBills(),
      ]);

      if (docsRes.status === 'fulfilled') {
        const rawDocs = docsRes.value;
        setDoctorsList(Array.isArray(rawDocs) ? rawDocs : rawDocs?.doctors || rawDocs?.data || []);
      }

      if (patsRes.status === 'fulfilled') {
        const rawPats = patsRes.value;
        setPatientsList(Array.isArray(rawPats) ? rawPats : rawPats?.patients || rawPats?.data || []);
      }

      if (apptsRes.status === 'fulfilled') {
        const rawAppts = apptsRes.value;
        setAppointmentsList(Array.isArray(rawAppts) ? rawAppts : rawAppts?.appointments || rawAppts?.data || []);
      }

      if (billsRes.status === 'fulfilled') {
        const rawBills = billsRes.value;
        setBillsList(Array.isArray(rawBills) ? rawBills : rawBills?.bills || rawBills?.data || []);
      }
    } catch (err) {
      console.error('Failed to load admin dashboard:', err);
      setErrorMsg(err.message || 'Failed to load hospital metrics.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAdminData();
  }, []);

  const handleAddDoctorSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...doctorForm,
        user_id: doctorForm.user_id || `doc_${Date.now()}`,
        doctor_name: doctorForm.doctor_name || `Dr. ${doctorForm.specialization}`,
        qualification: doctorForm.qualification || 'MBBS, MD',
        working_days: doctorForm.working_days.length > 0 ? doctorForm.working_days : ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        start_time: doctorForm.start_time || '09:00 AM',
        end_time: doctorForm.end_time || '05:00 PM',
      };
      await doctorService.createDoctor(payload);
      setShowAddDoctorModal(false);
      setDoctorForm({
        user_id: '',
        doctor_name: '',
        department: 'General Medicine',
        specialization: 'Senior Physician',
        qualification: 'MBBS, MD',
        experience: 5,
        consultation_fee: 1000,
        working_days: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        start_time: '09:00 AM',
        end_time: '05:00 PM',
        status: 'available',
      });
      fetchAdminData();
    } catch (err) {
      alert(err.message || 'Failed to add doctor');
    }
  };

  if (loading) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center gap-3 text-slate-700">
        <Loader2 className="w-8 h-8 text-brand-600 animate-spin" />
        <p className="text-xs font-bold">Loading Administrative Console...</p>
      </div>
    );
  }

  const adminDisplayName = user?.full_name || user?.name || 'Administrator';

  return (
    <div className="space-y-6 sm:space-y-8 px-2 sm:px-0">
      {/* Header Banner */}
      <div className="glass-card rounded-3xl p-5 sm:p-8 border border-slate-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-gradient-to-r from-brand-50 via-white to-teal-50">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-brand-700 uppercase tracking-widest mb-1">
            <ShieldCheck className="w-4 h-4" /> Executive Control Console
          </div>
          <h1 className="text-xl sm:text-3xl font-extrabold text-slate-900">
            Welcome, {adminDisplayName}
          </h1>
          <p className="text-xs sm:text-sm text-slate-600 mt-1">
            Real-time management of patients, specialist doctors, scheduled appointments, and billing receipts.
          </p>
        </div>

        <button
          onClick={() => setShowAddDoctorModal(true)}
          className="w-full sm:w-auto px-5 py-2.5 rounded-2xl font-bold text-white bg-brand-600 hover:bg-brand-700 shadow-md text-xs sm:text-sm flex items-center justify-center gap-2 transition-all shrink-0"
        >
          <UserPlus className="w-4 h-4" /> Add Specialist Doctor
        </button>
      </div>

      {errorMsg && (
        <div className="p-4 rounded-2xl bg-rose-50 border border-rose-200 text-xs text-rose-700 flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0" /> {errorMsg}
        </div>
      )}

      {/* Navigation Tabs - Responsive Scroll Container */}
      <div className="flex items-center gap-2 border-b border-slate-200 pb-3 overflow-x-auto scrollbar-none">
        {[
          { id: 'overview', label: 'Overview Analytics', icon: Activity },
          { id: 'doctors', label: `Doctors (${doctorsList.length})`, icon: Stethoscope },
          { id: 'patients', label: `Patients (${patientsList.length})`, icon: Users },
          { id: 'appointments', label: `Appointments (${appointmentsList.length})`, icon: Calendar },
          { id: 'bills', label: `Bills (${billsList.length})`, icon: Receipt },
        ].map((tab) => {
          const IconComp = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 whitespace-nowrap transition-all ${
                activeTab === tab.id
                  ? 'bg-brand-600 text-white shadow-sm'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <IconComp className="w-4 h-4" /> {tab.label}
            </button>
          );
        })}
      </div>

      {/* Overview Analytics Tab */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="glass-card rounded-2xl p-5 border border-slate-200">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Total Patients</span>
                <Users className="w-5 h-5 text-brand-600" />
              </div>
              <div className="text-2xl sm:text-3xl font-extrabold text-slate-900">{metrics?.total_patients ?? patientsList.length}</div>
              <p className="text-[11px] text-slate-500 mt-1">Registered Patient Profiles</p>
            </div>

            <div className="glass-card rounded-2xl p-5 border border-slate-200">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Active Doctors</span>
                <Stethoscope className="w-5 h-5 text-teal-600" />
              </div>
              <div className="text-2xl sm:text-3xl font-extrabold text-slate-900">{metrics?.total_doctors ?? doctorsList.length}</div>
              <p className="text-[11px] text-slate-500 mt-1">Specialist Clinical Staff</p>
            </div>

            <div className="glass-card rounded-2xl p-5 border border-slate-200">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Appointments</span>
                <Calendar className="w-5 h-5 text-emerald-600" />
              </div>
              <div className="text-2xl sm:text-3xl font-extrabold text-slate-900">{metrics?.total_appointments ?? appointmentsList.length}</div>
              <p className="text-[11px] text-slate-500 mt-1">Total Scheduled Consultations</p>
            </div>

            <div className="glass-card rounded-2xl p-5 border border-slate-200">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Total Revenue</span>
                <IndianRupee className="w-5 h-5 text-amber-600" />
              </div>
              <div className="text-2xl sm:text-3xl font-extrabold text-slate-900">
                ₹{metrics?.total_revenue ? Number(metrics.total_revenue).toLocaleString('en-IN') : '1,700'}
              </div>
              <p className="text-[11px] text-slate-500 mt-1">Pending Verification: {metrics?.pending_payments ?? 0}</p>
            </div>
          </div>

          <div className="glass-card rounded-2xl p-6 border border-slate-200 space-y-4">
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <FileText className="w-4 h-4 text-brand-600" /> Clinical System Operations
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
                <span className="text-slate-500 font-medium">Medical Records</span>
                <p className="text-2xl font-extrabold text-slate-900">{metrics?.total_medical_records ?? 4}</p>
              </div>
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
                <span className="text-slate-500 font-medium">Prescriptions Issued</span>
                <p className="text-2xl font-extrabold text-slate-900">{metrics?.total_prescriptions ?? 2}</p>
              </div>
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
                <span className="text-slate-500 font-medium">Lab Reports Uploaded</span>
                <p className="text-2xl font-extrabold text-slate-900">{metrics?.total_lab_reports ?? 4}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Doctors List */}
      {activeTab === 'doctors' && (
        <div className="glass-card rounded-3xl p-4 sm:p-6 border border-slate-200 space-y-4">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <h3 className="text-base sm:text-lg font-bold text-slate-900">Doctors Directory</h3>
            <div className="relative w-full sm:w-64">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Search by name or department..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-9 pr-4 py-2 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-900 placeholder-slate-400 outline-none"
              />
            </div>
          </div>

          <div className="overflow-x-auto -mx-4 sm:mx-0">
            <table className="w-full text-left text-xs text-slate-700 min-w-[640px]">
              <thead className="bg-slate-100 text-slate-500 uppercase tracking-wider text-[10px] font-bold">
                <tr>
                  <th className="p-3">Doctor Name</th>
                  <th className="p-3">Department</th>
                  <th className="p-3">Specialization</th>
                  <th className="p-3">Experience</th>
                  <th className="p-3">Consultation Fee</th>
                  <th className="p-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {doctorsList.length === 0 ? (
                  <tr>
                    <td colSpan="6" className="text-center py-8 text-slate-500">
                      No doctor records found. Click "Add Specialist Doctor" to insert a doctor profile.
                    </td>
                  </tr>
                ) : (
                  doctorsList
                    .filter(
                      (d) =>
                        (d.doctor_name || d.full_name || '')
                          .toLowerCase()
                          .includes(searchTerm.toLowerCase()) ||
                        (d.department || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
                        (d.specialization || '').toLowerCase().includes(searchTerm.toLowerCase())
                    )
                    .map((doc, idx) => (
                      <tr key={doc._id || idx} className="hover:bg-slate-50">
                        <td className="p-3 font-extrabold text-slate-900">
                          {doc.doctor_name || doc.full_name || `Dr. ${doc.specialization}`}
                        </td>
                        <td className="p-3 font-semibold text-brand-700">{doc.department}</td>
                        <td className="p-3 text-slate-700">{doc.specialization}</td>
                        <td className="p-3 text-slate-600">{doc.experience} Years</td>
                        <td className="p-3 text-emerald-700 font-extrabold">₹{doc.consultation_fee}</td>
                        <td className="p-3">
                          <span
                            className={`px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider ${
                              doc.status === 'available'
                                ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                                : 'bg-rose-50 text-rose-700 border border-rose-200'
                            }`}
                          >
                            {doc.status || 'available'}
                          </span>
                        </td>
                      </tr>
                    ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Patients Directory */}
      {activeTab === 'patients' && (
        <div className="glass-card rounded-3xl p-4 sm:p-6 border border-slate-200 space-y-4">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <h3 className="text-base sm:text-lg font-bold text-slate-900">Patients Directory</h3>
            <div className="relative w-full sm:w-64">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Search patient name or phone..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-9 pr-4 py-2 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-900 placeholder-slate-400 outline-none"
              />
            </div>
          </div>

          <div className="overflow-x-auto -mx-4 sm:mx-0">
            <table className="w-full text-left text-xs text-slate-700 min-w-[640px]">
              <thead className="bg-slate-100 text-slate-500 uppercase tracking-wider text-[10px] font-bold">
                <tr>
                  <th className="p-3">Patient Name</th>
                  <th className="p-3">Age / Gender</th>
                  <th className="p-3">Blood Group</th>
                  <th className="p-3">Phone Number</th>
                  <th className="p-3">Email Address</th>
                  <th className="p-3">Emergency Contact</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {patientsList.length === 0 ? (
                  <tr>
                    <td colSpan="6" className="text-center py-8 text-slate-500">
                      No patient records currently stored.
                    </td>
                  </tr>
                ) : (
                  patientsList
                    .filter(
                      (pt) =>
                        (pt.full_name || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
                        (pt.phone || '').includes(searchTerm) ||
                        (pt.email || '').toLowerCase().includes(searchTerm.toLowerCase())
                    )
                    .map((pt, idx) => (
                      <tr key={pt._id || idx} className="hover:bg-slate-50">
                        <td className="p-3 font-extrabold text-slate-900">{pt.full_name}</td>
                        <td className="p-3">
                          {pt.age} yrs / {pt.gender}
                        </td>
                        <td className="p-3 font-bold text-rose-600">{pt.blood_group}</td>
                        <td className="p-3 font-medium text-slate-800">{pt.phone}</td>
                        <td className="p-3 text-slate-600">{pt.email}</td>
                        <td className="p-3 text-slate-600">{pt.emergency_contact || 'N/A'}</td>
                      </tr>
                    ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Appointments List */}
      {activeTab === 'appointments' && (
        <div className="glass-card rounded-3xl p-4 sm:p-6 border border-slate-200 space-y-4">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <h3 className="text-base sm:text-lg font-bold text-slate-900">Scheduled Appointments</h3>
            <div className="relative w-full sm:w-64">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Search reason or patient..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-9 pr-4 py-2 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-900 placeholder-slate-400 outline-none"
              />
            </div>
          </div>

          <div className="overflow-x-auto -mx-4 sm:mx-0">
            <table className="w-full text-left text-xs text-slate-700 min-w-[640px]">
              <thead className="bg-slate-100 text-slate-500 uppercase tracking-wider text-[10px] font-bold">
                <tr>
                  <th className="p-3">Patient Name</th>
                  <th className="p-3">Doctor</th>
                  <th className="p-3">Date & Slot</th>
                  <th className="p-3">Reason for Visit</th>
                  <th className="p-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {appointmentsList.length === 0 ? (
                  <tr>
                    <td colSpan="5" className="text-center py-8 text-slate-500">
                      No appointment records currently stored.
                    </td>
                  </tr>
                ) : (
                  appointmentsList
                    .filter(
                      (apt) =>
                        (apt.patient_name || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
                        (apt.reason || '').toLowerCase().includes(searchTerm.toLowerCase())
                    )
                    .map((apt, idx) => (
                      <tr key={apt._id || idx} className="hover:bg-slate-50">
                        <td className="p-3 font-extrabold text-slate-900">{apt.patient_name || 'Patient'}</td>
                        <td className="p-3 font-semibold text-brand-700">{apt.doctor_name || 'Specialist Doctor'}</td>
                        <td className="p-3 text-slate-800">
                          <span className="font-bold">{apt.appointment_date}</span>
                          <span className="block text-[11px] text-slate-500">{apt.time_slot}</span>
                        </td>
                        <td className="p-3 font-medium text-slate-700">{apt.reason}</td>
                        <td className="p-3">
                          <span
                            className={`px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider ${
                              apt.status === 'completed'
                                ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                                : 'bg-amber-50 text-amber-700 border border-amber-200'
                            }`}
                          >
                            {apt.status}
                          </span>
                        </td>
                      </tr>
                    ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Bills & Financial Records */}
      {activeTab === 'bills' && (
        <div className="glass-card rounded-3xl p-4 sm:p-6 border border-slate-200 space-y-4">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <h3 className="text-base sm:text-lg font-bold text-slate-900">Billing & Financial Records</h3>
            <div className="relative w-full sm:w-64">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Search patient or payment status..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-9 pr-4 py-2 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-900 placeholder-slate-400 outline-none"
              />
            </div>
          </div>

          <div className="overflow-x-auto -mx-4 sm:mx-0">
            <table className="w-full text-left text-xs text-slate-700 min-w-[640px]">
              <thead className="bg-slate-100 text-slate-500 uppercase tracking-wider text-[10px] font-bold">
                <tr>
                  <th className="p-3">Patient Name</th>
                  <th className="p-3">Consultation Fee</th>
                  <th className="p-3">Medicine Cost</th>
                  <th className="p-3">Lab Tests Cost</th>
                  <th className="p-3">Total Amount</th>
                  <th className="p-3">Payment Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {billsList.length === 0 ? (
                  <tr>
                    <td colSpan="6" className="text-center py-8 text-slate-500">
                      No billing records currently stored.
                    </td>
                  </tr>
                ) : (
                  billsList
                    .filter(
                      (b) =>
                        (b.patient_name || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
                        (b.payment_status || '').toLowerCase().includes(searchTerm.toLowerCase())
                    )
                    .map((b, idx) => (
                      <tr key={b._id || idx} className="hover:bg-slate-50">
                        <td className="p-3 font-extrabold text-slate-900">{b.patient_name || 'Patient'}</td>
                        <td className="p-3 font-medium text-slate-800">₹{b.consultation_fee ?? 0}</td>
                        <td className="p-3 font-medium text-slate-800">₹{b.medicine_cost ?? 0}</td>
                        <td className="p-3 font-medium text-slate-800">₹{b.test_cost ?? 0}</td>
                        <td className="p-3 font-extrabold text-emerald-700">₹{b.total_amount ?? 0}</td>
                        <td className="p-3">
                          <span
                            className={`px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider ${
                              b.payment_status === 'Paid'
                                ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                                : 'bg-amber-50 text-amber-700 border border-amber-200'
                            }`}
                          >
                            {b.payment_status || 'Pending'}
                          </span>
                        </td>
                      </tr>
                    ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Modal for Adding Doctor */}
      {showAddDoctorModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-panel bg-white rounded-3xl p-6 max-w-lg w-full border border-slate-200 shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-lg font-extrabold text-slate-900 flex items-center gap-2">
                <UserPlus className="w-5 h-5 text-brand-600" /> Register Specialist Doctor
              </h3>
              <button
                onClick={() => setShowAddDoctorModal(false)}
                className="p-1 rounded-lg text-slate-400 hover:bg-slate-100 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleAddDoctorSubmit} className="space-y-3.5 text-xs">
              <div>
                <label className="block text-slate-700 font-semibold mb-1">Doctor Full Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Dr. Rajesh Sharma"
                  value={doctorForm.doctor_name}
                  onChange={(e) => setDoctorForm({ ...doctorForm, doctor_name: e.target.value })}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none focus:border-brand-600"
                />
              </div>

              <div>
                <label className="block text-slate-700 font-semibold mb-1">User ID / Email Handle (Optional)</label>
                <input
                  type="text"
                  placeholder="e.g. dr.rajesh@niramaya.org"
                  value={doctorForm.user_id}
                  onChange={(e) => setDoctorForm({ ...doctorForm, user_id: e.target.value })}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none focus:border-brand-600"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-700 font-semibold mb-1">Department</label>
                  <input
                    type="text"
                    required
                    value={doctorForm.department}
                    onChange={(e) => setDoctorForm({ ...doctorForm, department: e.target.value })}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none focus:border-brand-600"
                  />
                </div>
                <div>
                  <label className="block text-slate-700 font-semibold mb-1">Specialization</label>
                  <input
                    type="text"
                    required
                    value={doctorForm.specialization}
                    onChange={(e) => setDoctorForm({ ...doctorForm, specialization: e.target.value })}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none focus:border-brand-600"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div>
                  <label className="block text-slate-700 font-semibold mb-1">Qualification</label>
                  <input
                    type="text"
                    value={doctorForm.qualification}
                    onChange={(e) => setDoctorForm({ ...doctorForm, qualification: e.target.value })}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none focus:border-brand-600"
                  />
                </div>
                <div>
                  <label className="block text-slate-700 font-semibold mb-1">Experience (Yrs)</label>
                  <input
                    type="number"
                    required
                    value={doctorForm.experience}
                    onChange={(e) => setDoctorForm({ ...doctorForm, experience: Number(e.target.value) })}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none focus:border-brand-600"
                  />
                </div>
                <div>
                  <label className="block text-slate-700 font-semibold mb-1">Fee (₹ INR)</label>
                  <input
                    type="number"
                    required
                    value={doctorForm.consultation_fee}
                    onChange={(e) => setDoctorForm({ ...doctorForm, consultation_fee: Number(e.target.value) })}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none focus:border-brand-600"
                  />
                </div>
              </div>

              <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowAddDoctorModal(false)}
                  className="px-4 py-2.5 rounded-xl bg-slate-100 text-slate-700 hover:bg-slate-200 font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold"
                >
                  Save Doctor Profile
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
