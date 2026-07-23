import React, { useState, useEffect } from 'react';
import { dashboardService } from '../../services/dashboardService';
import { appointmentService } from '../../services/appointmentService';
import { doctorService } from '../../services/doctorService';
import { medicalService } from '../../services/medicalService';
import { useAuth } from '../../context/AuthContext';
import {
  Calendar,
  Clock,
  Plus,
  FileText,
  FlaskConical,
  CreditCard,
  CheckCircle2,
  AlertCircle,
  Loader2,
  Upload,
  Pill,
  QrCode,
  IndianRupee,
  Building2,
  Check,
} from 'lucide-react';
import upiQrImg from '/upi_qr.jpg';

export const PatientDashboard = () => {
  const { user } = useAuth();
  const [metrics, setMetrics] = useState(null);
  const [myAppointments, setMyAppointments] = useState([]);
  const [prescriptionsList, setPrescriptionsList] = useState([]);
  const [labReportsList, setLabReportsList] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('appointments'); // appointments | prescriptions | reports

  // Book Appointment Modal State
  const [showBookModal, setShowBookModal] = useState(false);
  const [bookingForm, setBookingForm] = useState({
    doctor_id: '',
    appointment_date: new Date().toISOString().split('T')[0],
    time_slot: '10:00 AM - 10:30 AM',
    reason: 'General Consultation & Routine Checkup',
    notes: '',
  });

  // Payment Modal State
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [selectedApptForPayment, setSelectedApptForPayment] = useState(null);
  const [paymentForm, setPaymentForm] = useState({
    bill_id: '',
    amount: 1500,
    transaction_id: 'TXN-' + Math.floor(100000 + Math.random() * 900000),
    screenshot: null,
  });

  const patientId = user?.sub || user?._id || user?.id;
  const patientFullName = user?.full_name || user?.name || (user?.email ? user.email.split('@')[0].toUpperCase() : 'Patient');

  const fetchPatientData = async () => {
    setLoading(true);
    try {
      const data = await dashboardService.getPatientDashboard();
      setMetrics(data);

      const apptsRes = await appointmentService.getMyAppointments();
      const list = apptsRes?.appointments || (Array.isArray(apptsRes) ? apptsRes : []);
      setMyAppointments(list);

      const docsRes = await doctorService.getAllDoctors();
      const docsList = Array.isArray(docsRes) ? docsRes : (docsRes?.data || docsRes?.doctors || []);
      setDoctors(docsList);
      if (docsList.length > 0) {
        setBookingForm((prev) => ({ ...prev, doctor_id: docsList[0]._id || docsList[0].user_id }));
      }

      if (patientId) {
        const [prescRes, repRes] = await Promise.allSettled([
          medicalService.getPatientPrescriptions(patientId),
          medicalService.getPatientLabReports(patientId),
        ]);
        if (prescRes.status === 'fulfilled') {
          setPrescriptionsList(prescRes.value?.data || prescRes.value || []);
        }
        if (repRes.status === 'fulfilled') {
          setLabReportsList(repRes.value?.data || repRes.value || []);
        }
      }
    } catch (err) {
      console.error('Failed to fetch patient portal data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPatientData();
  }, []);

  const openPaymentModal = (appt = null) => {
    if (appt) {
      setSelectedApptForPayment(appt);
      // Find doctor consultation fee
      const doc = doctors.find((d) => (d._id || d.user_id) === appt.doctor_id);
      const fee = doc ? doc.consultation_fee : 1500;
      setPaymentForm({
        bill_id: appt.appointment_id || appt._id || ('BILL-' + Math.floor(100000 + Math.random() * 900000)),
        amount: fee,
        transaction_id: 'TXN-' + Math.floor(100000 + Math.random() * 900000),
        screenshot: null,
      });
    } else if (myAppointments.length > 0) {
      const firstAppt = myAppointments[0];
      setSelectedApptForPayment(firstAppt);
      const doc = doctors.find((d) => (d._id || d.user_id) === firstAppt.doctor_id);
      const fee = doc ? doc.consultation_fee : 1500;
      setPaymentForm({
        bill_id: firstAppt.appointment_id || firstAppt._id || ('BILL-' + Math.floor(100000 + Math.random() * 900000)),
        amount: fee,
        transaction_id: 'TXN-' + Math.floor(100000 + Math.random() * 900000),
        screenshot: null,
      });
    } else {
      setPaymentForm({
        bill_id: 'BILL-' + Math.floor(100000 + Math.random() * 900000),
        amount: 1500,
        transaction_id: 'TXN-' + Math.floor(100000 + Math.random() * 900000),
        screenshot: null,
      });
    }
    setShowPaymentModal(true);
  };

  const handleBookAppointment = async (e) => {
    e.preventDefault();
    if (!bookingForm.doctor_id) {
      alert('Please select a doctor.');
      return;
    }
    if (!patientId) {
      alert('Patient session not found. Please sign in again.');
      return;
    }

    try {
      await appointmentService.createAppointment({
        patient_id: patientId,
        ...bookingForm,
      });
      alert('Consultation appointment successfully booked!');
      setShowBookModal(false);
      fetchPatientData();
    } catch (err) {
      alert(err.message || 'Failed to book appointment');
    }
  };

  const handlePaymentUpload = async (e) => {
    e.preventDefault();
    if (!paymentForm.bill_id) {
      alert('Please enter or select your Bill/Invoice ID.');
      return;
    }
    if (!paymentForm.screenshot) {
      alert('Please select your payment receipt screenshot image file.');
      return;
    }

    try {
      const fd = new FormData();
      fd.append('bill_id', paymentForm.bill_id);
      fd.append('transaction_id', paymentForm.transaction_id);
      fd.append('screenshot', paymentForm.screenshot);

      await medicalService.uploadPaymentProof(fd);
      alert('Payment receipt proof successfully submitted to Niramaya Hospital Billing Desk!');
      setShowPaymentModal(false);
    } catch (err) {
      alert(err.message || 'Failed to upload payment proof');
    }
  };

  if (loading) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center gap-3 text-slate-700">
        <Loader2 className="w-8 h-8 text-brand-600 animate-spin" />
        <p className="text-xs font-bold">Loading Patient Portal...</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Banner */}
      <div className="glass-card rounded-3xl p-6 sm:p-8 border border-slate-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-gradient-to-r from-brand-50 via-white to-teal-50">
        <div>
          <span className="inline-block px-3 py-1 rounded-full bg-brand-100 text-brand-800 text-[11px] font-bold uppercase tracking-wider mb-2">
            Patient Portal • Welcome Back
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900">Welcome, {patientFullName}</h1>
          <p className="text-xs sm:text-sm text-slate-600">
            View your upcoming doctor visits, digital prescriptions, lab test reports, and billing receipts.
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setShowBookModal(true)}
            className="px-5 py-2.5 rounded-2xl font-bold text-white bg-brand-600 hover:bg-brand-700 shadow-md text-xs sm:text-sm flex items-center gap-2 transition-all"
          >
            <Plus className="w-4 h-4" /> Book Appointment
          </button>
          <button
            onClick={() => openPaymentModal(null)}
            className="px-4 py-2.5 rounded-2xl font-bold text-white bg-emerald-600 hover:bg-emerald-700 text-xs sm:text-sm flex items-center gap-2 shadow-md transition-all"
          >
            <CreditCard className="w-4 h-4" /> Pay Fees & Upload Proof
          </button>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div className="glass-card rounded-2xl p-4 border border-slate-200">
          <div className="text-xs font-bold text-slate-500 uppercase mb-1">Total Appointments</div>
          <div className="text-2xl font-extrabold text-slate-900">{myAppointments.length || (metrics?.total_appointments ?? 0)}</div>
        </div>

        <div className="glass-card rounded-2xl p-4 border border-emerald-200">
          <div className="text-xs font-bold text-emerald-700 uppercase mb-1">Completed Visits</div>
          <div className="text-2xl font-extrabold text-emerald-700">{metrics?.completed_appointments ?? 0}</div>
        </div>

        <div className="glass-card rounded-2xl p-4 border border-amber-200">
          <div className="text-xs font-bold text-amber-700 uppercase mb-1">Upcoming</div>
          <div className="text-2xl font-extrabold text-amber-700">{metrics?.pending_appointments ?? myAppointments.length ?? 0}</div>
        </div>

        <div className="glass-card rounded-2xl p-4 border border-brand-200">
          <div className="text-xs font-bold text-brand-700 uppercase mb-1">Prescriptions</div>
          <div className="text-2xl font-extrabold text-brand-700">{prescriptionsList.length || (metrics?.prescriptions?.length ?? 0)}</div>
        </div>

        <div className="glass-card rounded-2xl p-4 border border-teal-200">
          <div className="text-xs font-bold text-teal-700 uppercase mb-1">Lab Reports</div>
          <div className="text-2xl font-extrabold text-teal-700">{labReportsList.length || (metrics?.lab_reports?.length ?? 0)}</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-200 pb-3 overflow-x-auto">
        {[
          { id: 'appointments', label: 'My Appointments', icon: Calendar },
          { id: 'prescriptions', label: 'Prescriptions History', icon: Pill },
          { id: 'reports', label: 'Lab Test Reports', icon: FlaskConical },
        ].map((tab) => {
          const IconComp = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-2 transition-all ${
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

      {/* Appointments Tab */}
      {activeTab === 'appointments' && (
        <div className="glass-card rounded-3xl p-6 border border-slate-200 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-bold text-slate-900">Your Scheduled Consultations ({myAppointments.length})</h3>
            <button
              onClick={() => setShowBookModal(true)}
              className="text-xs font-bold text-brand-700 hover:text-brand-800 flex items-center gap-1"
            >
              <Plus className="w-3.5 h-3.5" /> Book New
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-700">
              <thead className="bg-slate-100 text-slate-500 uppercase tracking-wider text-[10px] font-bold">
                <tr>
                  <th className="p-3 rounded-l-xl">Doctor / Department</th>
                  <th className="p-3">Date & Time Slot</th>
                  <th className="p-3">Reason for Visit</th>
                  <th className="p-3">Status</th>
                  <th className="p-3 rounded-r-xl">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {myAppointments.length === 0 ? (
                  <tr>
                    <td colSpan="5" className="text-center py-8 text-slate-500">
                      No appointments currently scheduled. Click "Book Appointment" to schedule your first visit.
                    </td>
                  </tr>
                ) : (
                  myAppointments.map((appt, idx) => {
                    const docObj = doctors.find((d) => (d._id || d.user_id) === appt.doctor_id);
                    return (
                      <tr key={appt._id || idx} className="hover:bg-slate-50">
                        <td className="p-3 font-bold text-slate-900">
                          {docObj ? docObj.doctor_name || docObj.department : appt.doctor_id}
                          {docObj && <div className="text-[10px] text-brand-700 font-semibold">{docObj.department} ({docObj.specialization})</div>}
                        </td>
                        <td className="p-3">
                          <div className="font-bold text-slate-900">{appt.appointment_date}</div>
                          <div className="text-[10px] text-teal-700">{appt.time_slot}</div>
                        </td>
                        <td className="p-3">{appt.reason}</td>
                        <td className="p-3">
                          <span
                            className={`px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider ${
                              appt.status === 'Completed' || appt.status === 'completed'
                                ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                                : appt.status === 'Confirmed' || appt.status === 'confirmed'
                                ? 'bg-brand-50 text-brand-700 border border-brand-200'
                                : 'bg-amber-50 text-amber-700 border border-amber-200'
                            }`}
                          >
                            {appt.status || 'Scheduled'}
                          </span>
                        </td>
                        <td className="p-3">
                          <button
                            onClick={() => openPaymentModal(appt)}
                            className="px-3 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-[11px] flex items-center gap-1 shadow-sm transition-all"
                          >
                            <CreditCard className="w-3.5 h-3.5" /> Pay ₹{docObj ? docObj.consultation_fee : 1500} & Upload Proof
                          </button>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Prescriptions Tab */}
      {activeTab === 'prescriptions' && (
        <div className="glass-card rounded-3xl p-6 border border-slate-200 space-y-4">
          <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Pill className="w-5 h-5 text-brand-600" /> Digital Rx Prescriptions ({prescriptionsList.length || (metrics?.prescriptions?.length ?? 0)})
          </h3>

          <div className="space-y-3">
            {prescriptionsList.length === 0 && (!metrics?.prescriptions || metrics?.prescriptions?.length === 0) ? (
              <div className="text-center py-8 text-xs text-slate-500">No active digital prescriptions found on record.</div>
            ) : (
              (prescriptionsList.length > 0 ? prescriptionsList : metrics?.prescriptions || []).map((p, idx) => (
                <div key={p._id || idx} className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-2 text-xs">
                  <div className="flex justify-between font-bold text-slate-900">
                    <span>Diagnosis: {p.diagnosis || 'Clinical Treatment'}</span>
                    <span className="text-brand-700">{p.created_at ? new Date(p.created_at).toLocaleDateString() : 'Recent'}</span>
                  </div>
                  <p className="text-slate-600 font-semibold">Doctor Advice: {p.advice || 'Follow prescription dosage'}</p>
                  {p.medicines && p.medicines.length > 0 && (
                    <div className="mt-2 pt-2 border-t border-slate-200 text-[11px] space-y-1">
                      <span className="font-bold text-slate-800 uppercase tracking-wider text-[10px]">Prescribed Dosage:</span>
                      {p.medicines.map((m, mIdx) => (
                        <div key={mIdx} className="text-slate-700 font-medium">
                          • {m.name} ({m.dosage}) — {m.frequency} [{m.duration}]
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Lab Test Reports Tab */}
      {activeTab === 'reports' && (
        <div className="glass-card rounded-3xl p-6 border border-slate-200 space-y-4">
          <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <FlaskConical className="w-5 h-5 text-teal-600" /> Diagnostic Lab Test Reports ({labReportsList.length})
          </h3>

          <div className="space-y-3">
            {labReportsList.length === 0 ? (
              <div className="text-center py-8 text-xs text-slate-500">No lab test reports uploaded for your patient account yet.</div>
            ) : (
              labReportsList.map((rep, idx) => (
                <div key={rep._id || idx} className="p-4 rounded-2xl bg-emerald-50/50 border border-emerald-200 space-y-2 text-xs">
                  <div className="flex justify-between font-bold text-emerald-900">
                    <span>Diagnostic Result: {rep.result || rep.report || 'Laboratory Diagnostic Report'}</span>
                    <span className="text-emerald-700">{rep.created_at ? new Date(rep.created_at).toLocaleDateString() : 'Recent'}</span>
                  </div>
                  <p className="text-emerald-800 font-medium">Doctor Remarks: {rep.notes || rep.remarks || 'Normal Reference Range'}</p>
                  {rep.report_url && (
                    <a
                      href={rep.report_url}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-block mt-2 px-3 py-1.5 rounded-lg bg-emerald-600 text-white font-bold text-[11px] hover:bg-emerald-700 transition-all"
                    >
                      Download Lab Report PDF
                    </a>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Book Appointment Modal */}
      {showBookModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-panel bg-white rounded-3xl p-6 max-w-md w-full border border-slate-200 shadow-2xl space-y-4">
            <h3 className="text-xl font-bold text-slate-900">Book Doctor Consultation</h3>
            <form onSubmit={handleBookAppointment} className="space-y-3 text-xs">
              <div>
                <label className="block text-slate-700 font-semibold mb-1">Select Specialist Doctor</label>
                <select
                  value={bookingForm.doctor_id}
                  onChange={(e) => setBookingForm({ ...bookingForm, doctor_id: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none"
                >
                  {doctors.length === 0 ? (
                    <option value="">No doctors currently available</option>
                  ) : (
                    doctors.map((d) => (
                      <option key={d._id || d.user_id} value={d._id || d.user_id}>
                        {d.doctor_name || 'Dr. Specialist'} — {d.department} ({d.specialization}) — ₹{d.consultation_fee}
                      </option>
                    ))
                  )}
                </select>
              </div>

              <div>
                <label className="block text-slate-700 font-semibold mb-1">Date</label>
                <input
                  type="date"
                  required
                  value={bookingForm.appointment_date}
                  onChange={(e) => setBookingForm({ ...bookingForm, appointment_date: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none"
                />
              </div>

              <div>
                <label className="block text-slate-700 font-semibold mb-1">Preferred Time Slot</label>
                <select
                  value={bookingForm.time_slot}
                  onChange={(e) => setBookingForm({ ...bookingForm, time_slot: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none"
                >
                  <option value="09:00 AM - 09:30 AM">09:00 AM - 09:30 AM</option>
                  <option value="10:00 AM - 10:30 AM">10:00 AM - 10:30 AM</option>
                  <option value="02:00 PM - 02:30 PM">02:00 PM - 02:30 PM</option>
                  <option value="05:00 PM - 05:30 PM">05:00 PM - 05:30 PM</option>
                </select>
              </div>

              <div>
                <label className="block text-slate-700 font-semibold mb-1">Reason for Visit</label>
                <input
                  type="text"
                  required
                  value={bookingForm.reason}
                  onChange={(e) => setBookingForm({ ...bookingForm, reason: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none"
                />
              </div>

              <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowBookModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-100 text-slate-700 font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold"
                >
                  Confirm Consultation Booking
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Payment & PhonePe UPI QR Code Modal */}
      {showPaymentModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-md flex items-center justify-center p-4">
          <div className="glass-panel bg-white rounded-3xl p-6 max-w-lg w-full border border-slate-200 shadow-2xl space-y-5 max-h-[90vh] overflow-y-auto">
            
            {/* Header */}
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div>
                <span className="text-[10px] font-extrabold uppercase tracking-widest text-emerald-600 flex items-center gap-1">
                  <QrCode className="w-3.5 h-3.5" /> Direct PhonePe UPI Payment
                </span>
                <h3 className="text-xl font-extrabold text-slate-900">Hospital Fee & Receipt Proof</h3>
              </div>
              <button
                type="button"
                onClick={() => setShowPaymentModal(false)}
                className="w-8 h-8 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-500 font-bold flex items-center justify-center text-xs"
              >
                ✕
              </button>
            </div>

            {/* Price & Appointment Summary Banner */}
            <div className="p-4 rounded-2xl bg-gradient-to-r from-emerald-600 to-teal-700 text-white shadow-md space-y-1">
              <div className="text-xs uppercase tracking-wider font-semibold opacity-90">Total Payable Fee Amount</div>
              <div className="text-3xl font-extrabold flex items-center gap-1">
                ₹{Number(paymentForm.amount).toLocaleString('en-IN')}.00
              </div>
              {selectedApptForPayment && (
                <div className="text-xs pt-1 border-t border-emerald-500/50 opacity-95">
                  Appointment for: <span className="font-bold">{selectedApptForPayment.reason}</span> ({selectedApptForPayment.appointment_date})
                </div>
              )}
            </div>

            {/* PhonePe QR Code Image Display */}
            <div className="flex flex-col items-center justify-center p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-3">
              <div className="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center gap-1.5">
                <QrCode className="w-4 h-4 text-purple-600" /> Scan QR using PhonePe / Google Pay / Paytm
              </div>

              <div className="p-3 bg-white rounded-2xl border border-slate-200 shadow-md">
                <img
                  src={upiQrImg}
                  alt="PhonePe UPI Payment QR Code"
                  className="w-48 h-48 sm:w-56 sm:h-56 object-contain rounded-xl"
                />
              </div>

              <div className="text-center space-y-0.5 text-xs text-slate-600">
                <div className="font-extrabold text-slate-900">Payee: NIRAMAYA HEALTHCARE HOSPITAL</div>
                <div className="font-mono text-purple-700 font-bold text-[11px]">UPI ID: niramaya@phonepe</div>
                <div className="text-[10px] text-slate-400">Indore, Madhya Pradesh, India</div>
              </div>
            </div>

            {/* Payment Upload Form */}
            <form onSubmit={handlePaymentUpload} className="space-y-3 text-xs pt-2">
              <div>
                <label className="block text-slate-700 font-semibold mb-1">Select Consultation Appointment</label>
                <select
                  value={paymentForm.bill_id}
                  onChange={(e) => {
                    const chosen = myAppointments.find((a) => (a.appointment_id || a._id) === e.target.value);
                    if (chosen) {
                      setSelectedApptForPayment(chosen);
                      const doc = doctors.find((d) => (d._id || d.user_id) === chosen.doctor_id);
                      const fee = doc ? doc.consultation_fee : 1500;
                      setPaymentForm({ ...paymentForm, bill_id: e.target.value, amount: fee });
                    } else {
                      setPaymentForm({ ...paymentForm, bill_id: e.target.value });
                    }
                  }}
                  className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none"
                >
                  {myAppointments.length === 0 ? (
                    <option value={paymentForm.bill_id}>Invoice #{paymentForm.bill_id}</option>
                  ) : (
                    myAppointments.map((a) => (
                      <option key={a.appointment_id || a._id} value={a.appointment_id || a._id}>
                        {a.reason} — {a.appointment_date} ({a.time_slot})
                      </option>
                    ))
                  )}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-700 font-semibold mb-1">Fee Amount (₹ INR)</label>
                  <input
                    type="number"
                    required
                    value={paymentForm.amount}
                    onChange={(e) => setPaymentForm({ ...paymentForm, amount: Number(e.target.value) })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none font-bold"
                  />
                </div>

                <div>
                  <label className="block text-slate-700 font-semibold mb-1">UPI Ref / Transaction ID</label>
                  <input
                    type="text"
                    required
                    value={paymentForm.transaction_id}
                    onChange={(e) => setPaymentForm({ ...paymentForm, transaction_id: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none font-mono"
                  />
                </div>
              </div>

              <div>
                <label className="block text-slate-700 font-semibold mb-1">Attach Payment Screenshot Image</label>
                <input
                  type="file"
                  required
                  accept="image/*"
                  onChange={(e) => setPaymentForm({ ...paymentForm, screenshot: e.target.files[0] })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700"
                />
              </div>

              <div className="flex justify-end gap-3 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowPaymentModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-100 text-slate-700 font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold shadow-md flex items-center gap-1.5"
                >
                  <Check className="w-4 h-4" /> Submit Payment Receipt Proof
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
