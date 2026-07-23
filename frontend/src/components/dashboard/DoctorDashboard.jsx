import React, { useState, useEffect } from 'react';
import { dashboardService } from '../../services/dashboardService';
import { appointmentService } from '../../services/appointmentService';
import { medicalService } from '../../services/medicalService';
import { useAuth } from '../../context/AuthContext';
import {
  Calendar,
  Clock,
  User,
  FileText,
  FlaskConical,
  Pill,
  CheckCircle2,
  AlertCircle,
  Loader2,
  Plus,
  Search,
  Upload,
  Activity,
  ChevronRight,
} from 'lucide-react';

export const DoctorDashboard = () => {
  const { user } = useAuth();
  const [metrics, setMetrics] = useState(null);
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('queue'); // queue | prescription | labtest | labreport | history

  // Modals & Active Selections
  const [selectedAppt, setSelectedAppt] = useState(null);
  const [showRecordModal, setShowRecordModal] = useState(false);
  const [showPrescriptionModal, setShowPrescriptionModal] = useState(false);
  const [showLabTestModal, setShowLabTestModal] = useState(false);

  // Forms
  const [recordForm, setRecordForm] = useState({
    diagnosis: '',
    symptoms: 'Fever, Body Ache',
    medications: 'Paracetamol 650mg, Vitamin C',
    allergies: 'None',
    notes: 'Rest recommended for 3 days',
    file: null,
  });

  const [prescriptionForm, setPrescriptionForm] = useState({
    appointment_id: '',
    patient_id: '',
    medical_record_id: '',
    diagnosis: 'Viral Fever & Upper Respiratory Tract Infection',
    advice: 'Drink warm water, take prescribed medicines after meals, rest for 3 days.',
    medicines: [
      { name: 'Tab Paracetamol 650mg', dosage: '650mg', frequency: '1-0-1 (Twice Daily)', duration: '5 Days' },
      { name: 'Cap Amoxicillin 500mg', dosage: '500mg', frequency: '1-1-1 (Thrice Daily)', duration: '5 Days' },
    ],
  });

  const [labTestForm, setLabTestForm] = useState({
    appointment_id: '',
    tests: ['Complete Blood Count (CBC)', 'Fasting Blood Sugar (FBS)'],
    notes: 'Urgent lab evaluation required for fever workup.',
  });

  const [labReportForm, setLabReportForm] = useState({
    lab_test_id: '',
    result: 'Hemoglobin: 13.5 g/dL (Normal), WBC Count: 7,200 /uL (Normal), Platelets: 2.5 Lakhs (Normal)',
    notes: 'All blood parameters within healthy reference range.',
    file: null,
  });

  // History Lookup
  const [selectedPatientId, setSelectedPatientId] = useState('');
  const [patientHistory, setPatientHistory] = useState({
    records: [],
    prescriptions: [],
    labTests: [],
    labReports: [],
  });

  const fetchDoctorData = async () => {
    setLoading(true);
    try {
      const data = await dashboardService.getDoctorDashboard();
      setMetrics(data);

      const apptsRes = await appointmentService.getDoctorAppointments();
      const list = apptsRes?.appointments || (Array.isArray(apptsRes) ? apptsRes : []);
      setAppointments(list);

      if (list.length > 0 && !selectedPatientId) {
        setSelectedPatientId(list[0].patient_id);
      }
    } catch (err) {
      console.error('Failed to fetch doctor portal data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDoctorData();
  }, []);

  // Fetch Patient History
  const fetchPatientHistoryData = async (patId) => {
    if (!patId) return;
    try {
      const [recs, prescs, tests, reprts] = await Promise.allSettled([
        medicalService.getPatientRecords(patId),
        medicalService.getPatientPrescriptions(patId),
        medicalService.getPatientLabTests(patId),
        medicalService.getPatientLabReports(patId),
      ]);

      setPatientHistory({
        records: recs.status === 'fulfilled' ? recs.value?.data || recs.value || [] : [],
        prescriptions: prescs.status === 'fulfilled' ? prescs.value?.data || prescs.value || [] : [],
        labTests: tests.status === 'fulfilled' ? tests.value?.data || tests.value || [] : [],
        labReports: reprts.status === 'fulfilled' ? reprts.value?.data || reprts.value || [] : [],
      });
    } catch (err) {
      console.error('Failed to fetch patient clinical history:', err);
    }
  };

  useEffect(() => {
    if (activeTab === 'history' && selectedPatientId) {
      fetchPatientHistoryData(selectedPatientId);
    }
  }, [activeTab, selectedPatientId]);

  const handleUpdateStatus = async (apptId, status) => {
    try {
      await appointmentService.updateStatus(apptId, status);
      alert(`Appointment status updated to ${status}!`);
      fetchDoctorData();
    } catch (err) {
      alert(err.message || 'Failed to update status');
    }
  };

  const handleRecordSubmit = async (e) => {
    e.preventDefault();
    const apptId = selectedAppt?.appointment_id || selectedAppt?._id || selectedAppt?.id;
    if (!apptId) {
      alert('Invalid appointment selection.');
      return;
    }
    try {
      const fd = new FormData();
      fd.append('appointment_id', apptId);
      fd.append('diagnosis', recordForm.diagnosis);
      fd.append('symptoms', recordForm.symptoms);
      fd.append('medications', recordForm.medications);
      fd.append('allergies', recordForm.allergies);
      fd.append('notes', recordForm.notes);
      if (recordForm.file) {
        fd.append('file', recordForm.file);
      }
      await medicalService.createMedicalRecord(fd);
      alert('Medical Record successfully logged!');
      setShowRecordModal(false);
      fetchDoctorData();
    } catch (err) {
      alert(err.message || 'Failed to log medical record');
    }
  };

  const handlePrescriptionSubmit = async (e) => {
    e.preventDefault();
    const apptId = prescriptionForm.appointment_id || selectedAppt?.appointment_id || selectedAppt?._id;
    const patId = selectedAppt?.patient_id || user?.sub;
    const docId = user?.sub || user?._id;
    if (!apptId) {
      alert('Please select an appointment for prescription.');
      return;
    }
    try {
      await medicalService.createPrescription({
        patient_id: patId,
        doctor_id: docId,
        medical_record_id: apptId,
        diagnosis: prescriptionForm.diagnosis,
        medicines: prescriptionForm.medicines,
        advice: prescriptionForm.advice,
      });
      alert('Prescription successfully generated & saved!');
      setShowPrescriptionModal(false);
      fetchDoctorData();
    } catch (err) {
      alert(err.message || 'Failed to generate prescription');
    }
  };

  const handleLabTestSubmit = async (e) => {
    e.preventDefault();
    const apptId = labTestForm.appointment_id || selectedAppt?.appointment_id || selectedAppt?._id;
    if (!apptId) {
      alert('Please select an appointment for ordering lab test.');
      return;
    }
    try {
      await medicalService.createLabTest({
        appointment_id: apptId,
        tests: labTestForm.tests,
        notes: labTestForm.notes,
      });
      alert('Lab Test Order placed successfully!');
      setShowLabTestModal(false);
      fetchDoctorData();
    } catch (err) {
      alert(err.message || 'Failed to order lab test');
    }
  };

  const handleLabReportSubmit = async (e) => {
    e.preventDefault();
    if (!labReportForm.lab_test_id) {
      alert('Please enter or select a Lab Test ID.');
      return;
    }
    try {
      const fd = new FormData();
      fd.append('lab_test_id', labReportForm.lab_test_id);
      fd.append('result', labReportForm.result);
      fd.append('notes', labReportForm.notes);
      if (labReportForm.file) {
        fd.append('file', labReportForm.file);
      }
      await medicalService.createLabReport(fd);
      alert('Lab Report successfully saved!');
      setLabReportForm({ lab_test_id: '', result: '', notes: '', file: null });
      fetchDoctorData();
    } catch (err) {
      alert(err.message || 'Failed to upload lab report');
    }
  };

  const addMedicineRow = () => {
    setPrescriptionForm((prev) => ({
      ...prev,
      medicines: [
        ...prev.medicines,
        { name: '', dosage: '', frequency: '1-0-1 (Twice Daily)', duration: '5 Days' },
      ],
    }));
  };

  const removeMedicineRow = (index) => {
    setPrescriptionForm((prev) => ({
      ...prev,
      medicines: prev.medicines.filter((_, idx) => idx !== index),
    }));
  };

  const doctorDisplayName = user?.full_name || user?.name || (user?.email ? `Dr. ${user.email.split('@')[0].split('.')[0].toUpperCase()}` : 'Dr. Practitioner');
  const formattedDoctorTitle = doctorDisplayName.startsWith('Dr.') ? doctorDisplayName : `Dr. ${doctorDisplayName}`;

  if (loading) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center gap-3 text-slate-700">
        <Loader2 className="w-8 h-8 text-teal-600 animate-spin" />
        <p className="text-xs font-bold">Loading Doctor Portal...</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Banner */}
      <div className="glass-card rounded-3xl p-6 sm:p-8 border border-slate-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-gradient-to-r from-teal-50 via-white to-brand-50">
        <div>
          <span className="inline-block px-3 py-1 rounded-full bg-teal-100 text-teal-800 text-[11px] font-bold uppercase tracking-wider mb-2">
            Doctor Clinical Portal • {formattedDoctorTitle}
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900">Welcome, {formattedDoctorTitle}</h1>
          <p className="text-xs sm:text-sm text-slate-600">
            Manage consultations, issue digital prescriptions, order lab tests, and view patient clinical history.
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => {
              if (appointments.length > 0) setSelectedAppt(appointments[0]);
              setShowPrescriptionModal(true);
            }}
            className="px-4 py-2.5 rounded-2xl font-bold text-white bg-brand-600 hover:bg-brand-700 shadow-md text-xs flex items-center gap-2 transition-all"
          >
            <Pill className="w-4 h-4" /> Write Prescription
          </button>
          <button
            onClick={() => {
              if (appointments.length > 0) setSelectedAppt(appointments[0]);
              setShowLabTestModal(true);
            }}
            className="px-4 py-2.5 rounded-2xl font-bold text-white bg-teal-600 hover:bg-teal-700 shadow-md text-xs flex items-center gap-2 transition-all"
          >
            <FlaskConical className="w-4 h-4" /> Order Lab Test
          </button>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div className="glass-card rounded-2xl p-4 border border-slate-200">
          <div className="text-xs font-bold text-slate-500 uppercase mb-1">Total Consultations</div>
          <div className="text-2xl font-extrabold text-slate-900">{metrics?.total_appointments ?? 0}</div>
        </div>

        <div className="glass-card rounded-2xl p-4 border border-emerald-200">
          <div className="text-xs font-bold text-emerald-700 uppercase mb-1">Completed</div>
          <div className="text-2xl font-extrabold text-emerald-700">{metrics?.completed_appointments ?? 0}</div>
        </div>

        <div className="glass-card rounded-2xl p-4 border border-amber-200">
          <div className="text-xs font-bold text-amber-700 uppercase mb-1">Pending</div>
          <div className="text-2xl font-extrabold text-amber-700">{metrics?.pending_appointments ?? 0}</div>
        </div>

        <div className="glass-card rounded-2xl p-4 border border-brand-200">
          <div className="text-xs font-bold text-brand-700 uppercase mb-1">Prescriptions</div>
          <div className="text-2xl font-extrabold text-brand-700">{metrics?.prescriptions_written ?? 0}</div>
        </div>

        <div className="glass-card rounded-2xl p-4 border border-teal-200">
          <div className="text-xs font-bold text-teal-700 uppercase mb-1">Lab Tests</div>
          <div className="text-2xl font-extrabold text-teal-700">{metrics?.lab_tests_ordered ?? 0}</div>
        </div>
      </div>

      {/* Workspace Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-200 pb-3 overflow-x-auto">
        {[
          { id: 'queue', label: 'Consultations Queue', icon: Calendar },
          { id: 'prescription', label: 'Write Prescription', icon: Pill },
          { id: 'labtest', label: 'Order Lab Tests', icon: FlaskConical },
          { id: 'labreport', label: 'Upload Lab Report', icon: Upload },
          { id: 'history', label: 'Patient Clinical History', icon: Activity },
        ].map((tab) => {
          const IconComp = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-2 whitespace-nowrap transition-all ${
                activeTab === tab.id
                  ? 'bg-teal-600 text-white shadow-sm'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <IconComp className="w-4 h-4" /> {tab.label}
            </button>
          );
        })}
      </div>

      {/* Tab 1: Queue */}
      {activeTab === 'queue' && (
        <div className="glass-card rounded-3xl p-6 border border-slate-200 space-y-4">
          <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Calendar className="w-5 h-5 text-teal-600" /> Patient Consultations Queue ({appointments.length})
          </h3>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-700">
              <thead className="bg-slate-100 text-slate-500 uppercase tracking-wider text-[10px] font-bold">
                <tr>
                  <th className="p-3 rounded-l-xl">Patient Name / ID</th>
                  <th className="p-3">Date & Slot</th>
                  <th className="p-3">Reason</th>
                  <th className="p-3">Status</th>
                  <th className="p-3 rounded-r-xl">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {appointments.length === 0 ? (
                  <tr>
                    <td colSpan="5" className="text-center py-8 text-slate-500">
                      No scheduled patient appointments found for your doctor account.
                    </td>
                  </tr>
                ) : (
                  appointments.map((appt, idx) => (
                    <tr key={appt._id || idx} className="hover:bg-slate-50">
                      <td className="p-3 font-bold text-slate-900">
                        {appt.patient_name || 'Patient'}
                        <div className="text-[10px] text-slate-500 font-mono">{appt.patient_id}</div>
                      </td>
                      <td className="p-3">
                        <div className="font-semibold text-slate-900">{appt.appointment_date}</div>
                        <div className="text-[10px] text-teal-700">{appt.time_slot}</div>
                      </td>
                      <td className="p-3 text-slate-700">{appt.reason}</td>
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
                        <div className="flex items-center gap-2">
                          <button
                            onClick={() => handleUpdateStatus(appt.appointment_id || appt._id || appt.id, 'Confirmed')}
                            className="px-2.5 py-1 rounded-lg bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 text-[11px] font-bold"
                          >
                            Confirm
                          </button>
                          <button
                            onClick={() => {
                              setSelectedAppt(appt);
                              setRecordForm({ ...recordForm, diagnosis: appt.reason || 'General Checkup' });
                              setShowRecordModal(true);
                            }}
                            className="px-2.5 py-1 rounded-lg bg-teal-50 hover:bg-teal-100 text-teal-700 border border-teal-200 text-[11px] font-bold"
                          >
                            Log Record
                          </button>
                          <button
                            onClick={() => {
                              setSelectedAppt(appt);
                              setPrescriptionForm((prev) => ({
                                ...prev,
                                appointment_id: appt.appointment_id || appt._id,
                                diagnosis: appt.reason || 'General Consultation',
                              }));
                              setShowPrescriptionModal(true);
                            }}
                            className="px-2.5 py-1 rounded-lg bg-brand-50 hover:bg-brand-100 text-brand-700 border border-brand-200 text-[11px] font-bold"
                          >
                            Prescribe
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab 2: Write Prescription */}
      {activeTab === 'prescription' && (
        <div className="glass-card rounded-3xl p-6 border border-slate-200 space-y-4">
          <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Pill className="w-5 h-5 text-brand-600" /> Write Digital Rx Prescription
          </h3>

          <form onSubmit={handlePrescriptionSubmit} className="space-y-4 text-xs">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-slate-700 font-semibold mb-1">Select Patient / Appointment</label>
                <select
                  value={prescriptionForm.appointment_id}
                  onChange={(e) => {
                    const chosen = appointments.find((a) => (a.appointment_id || a._id) === e.target.value);
                    if (chosen) setSelectedAppt(chosen);
                    setPrescriptionForm({ ...prescriptionForm, appointment_id: e.target.value });
                  }}
                  className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none"
                >
                  <option value="">Select Appointment from Consultation Queue</option>
                  {appointments.map((a) => (
                    <option key={a.appointment_id || a._id} value={a.appointment_id || a._id}>
                      {a.patient_name} — {a.appointment_date} ({a.reason})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-slate-700 font-semibold mb-1">Clinical Diagnosis</label>
                <input
                  type="text"
                  required
                  value={prescriptionForm.diagnosis}
                  onChange={(e) => setPrescriptionForm({ ...prescriptionForm, diagnosis: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none"
                />
              </div>
            </div>

            {/* Medicines List */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <label className="block text-slate-800 font-bold uppercase tracking-wider text-[11px]">
                  Prescribed Medications ({prescriptionForm.medicines.length})
                </label>
                <button
                  type="button"
                  onClick={addMedicineRow}
                  className="text-xs font-bold text-brand-700 hover:text-brand-800 flex items-center gap-1"
                >
                  <Plus className="w-3.5 h-3.5" /> Add Medication
                </button>
              </div>

              {prescriptionForm.medicines.map((med, idx) => (
                <div key={idx} className="p-3 rounded-2xl bg-slate-50 border border-slate-200 grid grid-cols-1 md:grid-cols-4 gap-3">
                  <div>
                    <span className="text-[10px] text-slate-500 font-semibold">Medicine Name</span>
                    <input
                      type="text"
                      required
                      placeholder="e.g. Tab Paracetamol 650mg"
                      value={med.name}
                      onChange={(e) => {
                        const updated = [...prescriptionForm.medicines];
                        updated[idx].name = e.target.value;
                        setPrescriptionForm({ ...prescriptionForm, medicines: updated });
                      }}
                      className="w-full px-2.5 py-1.5 rounded-lg bg-white border border-slate-200 text-slate-900 text-xs"
                    />
                  </div>

                  <div>
                    <span className="text-[10px] text-slate-500 font-semibold">Dosage</span>
                    <input
                      type="text"
                      placeholder="e.g. 650mg"
                      value={med.dosage}
                      onChange={(e) => {
                        const updated = [...prescriptionForm.medicines];
                        updated[idx].dosage = e.target.value;
                        setPrescriptionForm({ ...prescriptionForm, medicines: updated });
                      }}
                      className="w-full px-2.5 py-1.5 rounded-lg bg-white border border-slate-200 text-slate-900 text-xs"
                    />
                  </div>

                  <div>
                    <span className="text-[10px] text-slate-500 font-semibold">Frequency</span>
                    <input
                      type="text"
                      placeholder="e.g. 1-0-1 (Twice Daily)"
                      value={med.frequency}
                      onChange={(e) => {
                        const updated = [...prescriptionForm.medicines];
                        updated[idx].frequency = e.target.value;
                        setPrescriptionForm({ ...prescriptionForm, medicines: updated });
                      }}
                      className="w-full px-2.5 py-1.5 rounded-lg bg-white border border-slate-200 text-slate-900 text-xs"
                    />
                  </div>

                  <div className="flex items-center gap-2">
                    <div className="flex-1">
                      <span className="text-[10px] text-slate-500 font-semibold">Duration</span>
                      <input
                        type="text"
                        placeholder="e.g. 5 Days"
                        value={med.duration}
                        onChange={(e) => {
                          const updated = [...prescriptionForm.medicines];
                          updated[idx].duration = e.target.value;
                          setPrescriptionForm({ ...prescriptionForm, medicines: updated });
                        }}
                        className="w-full px-2.5 py-1.5 rounded-lg bg-white border border-slate-200 text-slate-900 text-xs"
                      />
                    </div>
                    {prescriptionForm.medicines.length > 1 && (
                      <button
                        type="button"
                        onClick={() => removeMedicineRow(idx)}
                        className="mt-4 text-rose-600 font-bold hover:text-rose-700 text-xs"
                      >
                        Remove
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>

            <div>
              <label className="block text-slate-700 font-semibold mb-1">Doctor Advice & Instructions</label>
              <textarea
                rows={2}
                value={prescriptionForm.advice}
                onChange={(e) => setPrescriptionForm({ ...prescriptionForm, advice: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none"
              />
            </div>

            <div className="flex justify-end pt-3">
              <button
                type="submit"
                className="px-6 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold text-xs shadow-md"
              >
                Issue & Save Prescription
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Tab 3: Order Lab Tests */}
      {activeTab === 'labtest' && (
        <div className="glass-card rounded-3xl p-6 border border-slate-200 space-y-4">
          <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <FlaskConical className="w-5 h-5 text-teal-600" /> Order Diagnostic Lab Test
          </h3>

          <form onSubmit={handleLabTestSubmit} className="space-y-4 text-xs max-w-xl">
            <div>
              <label className="block text-slate-700 font-semibold mb-1">Select Consultation Appointment</label>
              <select
                value={labTestForm.appointment_id}
                onChange={(e) => setLabTestForm({ ...labTestForm, appointment_id: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none"
              >
                <option value="">Select Appointment</option>
                {appointments.map((a) => (
                  <option key={a.appointment_id || a._id} value={a.appointment_id || a._id}>
                    {a.patient_name} — {a.appointment_date} ({a.reason})
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-slate-700 font-semibold mb-1">Requested Tests (Comma Separated)</label>
              <input
                type="text"
                required
                value={labTestForm.tests.join(', ')}
                onChange={(e) => setLabTestForm({ ...labTestForm, tests: e.target.value.split(',').map((t) => t.strip ? t.strip() : t.trim()) })}
                placeholder="e.g. Complete Blood Count (CBC), Fasting Blood Glucose, Lipid Profile"
                className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none"
              />
            </div>

            <div>
              <label className="block text-slate-700 font-semibold mb-1">Clinical Instructions & Notes</label>
              <textarea
                rows={3}
                value={labTestForm.notes}
                onChange={(e) => setLabTestForm({ ...labTestForm, notes: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none"
              />
            </div>

            <button
              type="submit"
              className="px-6 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-bold text-xs shadow-md"
            >
              Order Diagnostic Lab Test
            </button>
          </form>
        </div>
      )}

      {/* Tab 4: Upload Lab Report */}
      {activeTab === 'labreport' && (
        <div className="glass-card rounded-3xl p-6 border border-slate-200 space-y-4">
          <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Upload className="w-5 h-5 text-emerald-600" /> Upload Diagnostic Lab Report Results
          </h3>

          <form onSubmit={handleLabReportSubmit} className="space-y-4 text-xs max-w-xl">
            <div>
              <label className="block text-slate-700 font-semibold mb-1">Select Consultation / Lab Test Reference</label>
              <select
                value={labReportForm.lab_test_id}
                onChange={(e) => setLabReportForm({ ...labReportForm, lab_test_id: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none"
              >
                <option value="">Select Consultation Appointment</option>
                {appointments.map((a) => (
                  <option key={a.appointment_id || a._id} value={a.appointment_id || a._id}>
                    {a.patient_name} — {a.appointment_date} ({a.reason})
                  </option>
                ))}
              </select>
              <div className="mt-2 text-[10px] text-slate-500">Or type custom Lab Test ID if uploading for standalone lab test:</div>
              <input
                type="text"
                placeholder="Type or paste custom Lab Test ID string"
                value={labReportForm.lab_test_id}
                onChange={(e) => setLabReportForm({ ...labReportForm, lab_test_id: e.target.value })}
                className="w-full px-3 py-2 mt-1 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none"
              />
            </div>

            <div>
              <label className="block text-slate-700 font-semibold mb-1">Laboratory Findings & Result Summary</label>
              <textarea
                rows={3}
                required
                value={labReportForm.result}
                onChange={(e) => setLabReportForm({ ...labReportForm, result: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none"
              />
            </div>

            <div>
              <label className="block text-slate-700 font-semibold mb-1">Doctor Remarks</label>
              <input
                type="text"
                value={labReportForm.notes}
                onChange={(e) => setLabReportForm({ ...labReportForm, notes: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none"
              />
            </div>

            <div>
              <label className="block text-slate-700 font-semibold mb-1">Attach Lab PDF Report File</label>
              <input
                type="file"
                accept="application/pdf,image/*"
                onChange={(e) => setLabReportForm({ ...labReportForm, file: e.target.files[0] })}
                className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700"
              />
            </div>

            <button
              type="submit"
              className="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-md"
            >
              Upload Diagnostic Report
            </button>
          </form>
        </div>
      )}

      {/* Tab 5: Patient Clinical History Timeline */}
      {activeTab === 'history' && (
        <div className="glass-card rounded-3xl p-6 border border-slate-200 space-y-6">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-100 pb-4">
            <div>
              <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <Activity className="w-5 h-5 text-teal-600" /> Patient Clinical Activity Log
              </h3>
              <p className="text-xs text-slate-500">View complete treatment history, lab orders, reports, and prescriptions for a patient.</p>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold text-slate-600">Select Patient:</span>
              <select
                value={selectedPatientId}
                onChange={(e) => setSelectedPatientId(e.target.value)}
                className="px-3 py-1.5 rounded-xl bg-slate-100 border border-slate-200 text-slate-900 text-xs font-bold outline-none"
              >
                {appointments.map((a) => (
                  <option key={a.patient_id} value={a.patient_id}>
                    {a.patient_name} ({a.patient_id})
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Prescriptions Written */}
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-3">
              <h4 className="font-bold text-slate-900 text-xs flex items-center gap-2">
                <Pill className="w-4 h-4 text-brand-600" /> Issued Digital Prescriptions ({patientHistory.prescriptions.length})
              </h4>
              {patientHistory.prescriptions.length === 0 ? (
                <p className="text-xs text-slate-400">No prescriptions found for this patient.</p>
              ) : (
                patientHistory.prescriptions.map((p, idx) => (
                  <div key={p._id || idx} className="p-3 rounded-xl bg-white border border-slate-200 text-xs space-y-1">
                    <div className="font-bold text-slate-900">{p.diagnosis}</div>
                    <div className="text-[11px] text-brand-700">Advice: {p.advice}</div>
                    {p.medicines && p.medicines.length > 0 && (
                      <div className="mt-1 pt-1 border-t border-slate-100 text-[10px] text-slate-600">
                        {p.medicines.map((m, mIdx) => (
                          <div key={mIdx}>• {m.name} ({m.dosage}) — {m.frequency} [{m.duration}]</div>
                        ))}
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>

            {/* Lab Tests & Reports */}
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-3">
              <h4 className="font-bold text-slate-900 text-xs flex items-center gap-2">
                <FlaskConical className="w-4 h-4 text-teal-600" /> Ordered Lab Tests & Reports ({patientHistory.labTests.length + patientHistory.labReports.length})
              </h4>
              {patientHistory.labTests.length === 0 && patientHistory.labReports.length === 0 ? (
                <p className="text-xs text-slate-400">No lab tests or reports recorded for this patient.</p>
              ) : (
                <div className="space-y-2">
                  {patientHistory.labTests.map((t, idx) => (
                    <div key={t._id || idx} className="p-3 rounded-xl bg-white border border-slate-200 text-xs space-y-1">
                      <div className="font-bold text-slate-900">Lab Order: {(t.tests || []).join(', ')}</div>
                      <div className="text-[10px] text-teal-700">Notes: {t.notes || 'None'}</div>
                    </div>
                  ))}
                  {patientHistory.labReports.map((r, idx) => (
                    <div key={r._id || idx} className="p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-xs space-y-1">
                      <div className="font-bold text-emerald-900">Lab Result: {r.result}</div>
                      <div className="text-[10px] text-emerald-700">Remarks: {r.notes}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Record Modal */}
      {showRecordModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-panel bg-white rounded-3xl p-6 max-w-lg w-full border border-slate-200 shadow-2xl space-y-4">
            <h3 className="text-xl font-bold text-slate-900">Log Clinical Medical Record</h3>
            <form onSubmit={handleRecordSubmit} className="space-y-3 text-xs">
              <div>
                <label className="block text-slate-700 font-semibold mb-1">Diagnosis</label>
                <input
                  type="text"
                  required
                  value={recordForm.diagnosis}
                  onChange={(e) => setRecordForm({ ...recordForm, diagnosis: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none"
                />
              </div>

              <div>
                <label className="block text-slate-700 font-semibold mb-1">Symptoms</label>
                <input
                  type="text"
                  value={recordForm.symptoms}
                  onChange={(e) => setRecordForm({ ...recordForm, symptoms: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none"
                />
              </div>

              <div>
                <label className="block text-slate-700 font-semibold mb-1">Medications</label>
                <input
                  type="text"
                  value={recordForm.medications}
                  onChange={(e) => setRecordForm({ ...recordForm, medications: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none"
                />
              </div>

              <div>
                <label className="block text-slate-700 font-semibold mb-1">Attach Medical Document / Lab Scan</label>
                <input
                  type="file"
                  onChange={(e) => setRecordForm({ ...recordForm, file: e.target.files[0] })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700"
                />
              </div>

              <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowRecordModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-100 text-slate-700 font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-bold"
                >
                  Save Record
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Prescription Modal */}
      {showPrescriptionModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-panel bg-white rounded-3xl p-6 max-w-lg w-full border border-slate-200 shadow-2xl space-y-4">
            <h3 className="text-xl font-bold text-slate-900">Quick Write Rx Prescription</h3>
            <form onSubmit={handlePrescriptionSubmit} className="space-y-3 text-xs">
              <div>
                <label className="block text-slate-700 font-semibold mb-1">Diagnosis</label>
                <input
                  type="text"
                  required
                  value={prescriptionForm.diagnosis}
                  onChange={(e) => setPrescriptionForm({ ...prescriptionForm, diagnosis: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none"
                />
              </div>

              <div>
                <label className="block text-slate-700 font-semibold mb-1">Advice & Dosage Instructions</label>
                <textarea
                  rows={3}
                  required
                  value={prescriptionForm.advice}
                  onChange={(e) => setPrescriptionForm({ ...prescriptionForm, advice: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none"
                />
              </div>

              <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowPrescriptionModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-100 text-slate-700 font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold"
                >
                  Issue Rx
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Lab Test Modal */}
      {showLabTestModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-panel bg-white rounded-3xl p-6 max-w-lg w-full border border-slate-200 shadow-2xl space-y-4">
            <h3 className="text-xl font-bold text-slate-900">Order Diagnostic Tests</h3>
            <form onSubmit={handleLabTestSubmit} className="space-y-3 text-xs">
              <div>
                <label className="block text-slate-700 font-semibold mb-1">Tests Requested (Comma Separated)</label>
                <input
                  type="text"
                  required
                  value={labTestForm.tests.join(', ')}
                  onChange={(e) => setLabTestForm({ ...labTestForm, tests: e.target.value.split(',') })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none"
                />
              </div>

              <div>
                <label className="block text-slate-700 font-semibold mb-1">Notes</label>
                <textarea
                  rows={2}
                  value={labTestForm.notes}
                  onChange={(e) => setLabTestForm({ ...labTestForm, notes: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 outline-none"
                />
              </div>

              <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowLabTestModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-100 text-slate-700 font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-bold"
                >
                  Order Test
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
