import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  Sparkles,
  Calendar,
  Stethoscope,
  Activity,
  Brain,
  FileText,
  ArrowRight,
  CheckCircle2,
  ChevronRight,
  Upload,
  AlertCircle,
  Loader2,
  AlertTriangle,
} from 'lucide-react';
import { medicalService } from '../services/medicalService';
import { VaidyaReportViewer } from '../components/ai/VaidyaReportViewer';

export const HomePage = () => {
  const { isAuthenticated, role } = useAuth();
  const navigate = useNavigate();

  // Symptom Checker State (/ai/symptom-check)
  const [symptomsInput, setSymptomsInput] = useState('');
  const [symptomResult, setSymptomResult] = useState(null);
  const [analyzingSymptoms, setAnalyzingSymptoms] = useState(false);
  const [symptomError, setSymptomError] = useState('');

  // Vaidya AI File Report Analyzer State (/vaidya-ai/analyze)
  const [vaidyaFile, setVaidyaFile] = useState(null);
  const [analyzingReport, setAnalyzingReport] = useState(false);
  const [vaidyaReportResult, setVaidyaReportResult] = useState(null);
  const [vaidyaFileError, setVaidyaFileError] = useState('');

  const handleSymptomCheck = async (e) => {
    e.preventDefault();
    if (!symptomsInput.trim()) return;

    setAnalyzingSymptoms(true);
    setSymptomError('');
    setSymptomResult(null);

    try {
      const res = await medicalService.symptomCheck(symptomsInput);
      setSymptomResult(res?.analysis || res);
    } catch (err) {
      setSymptomError(err.message || 'Failed to complete AI symptom analysis');
    } finally {
      setAnalyzingSymptoms(false);
    }
  };

  const handleVaidyaReportAnalyze = async (e) => {
    e.preventDefault();
    if (!vaidyaFile) {
      setVaidyaFileError('Please select a PDF or image medical report file.');
      return;
    }

    setAnalyzingReport(true);
    setVaidyaFileError('');
    setVaidyaReportResult(null);

    try {
      const fd = new FormData();
      fd.append('file', vaidyaFile);
      const res = await medicalService.analyzeMedicalReport(fd);
      setVaidyaReportResult(res?.data || res);
    } catch (err) {
      setVaidyaFileError(err.message || 'Failed to analyze report file');
    } finally {
      setAnalyzingReport(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 pt-28 pb-16 overflow-hidden">
      {/* Background ambient glowing soft gradient circles */}
      <div className="absolute top-20 left-1/2 -translate-x-1/2 w-[700px] h-[400px] bg-brand-500/10 rounded-full blur-[140px] pointer-events-none -z-10" />

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-20 text-center relative">
        {/* Floating Badge */}
        <div className="inline-flex items-center gap-2.5 px-4 py-2 rounded-full glass-panel border border-brand-200 text-xs sm:text-sm text-brand-700 shadow-sm mb-8">
          <span className="flex h-2 w-2 relative">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span className="font-bold">Nirmaya Hospital Operating System</span>
          <span className="text-slate-300">|</span>
          <span className="text-teal-700 font-semibold flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5 text-teal-600" /> Vaidya AI
          </span>
        </div>

        {/* Hero Title */}
        <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-slate-900 max-w-5xl mx-auto leading-[1.1] mb-6">
          Precision Indian Healthcare & <br className="hidden sm:inline" />
          <span className="bg-gradient-to-r from-brand-700 via-blue-600 to-teal-600 bg-clip-text text-transparent">
            Clinical AI Platform
          </span>
        </h1>

        {/* Subtitle */}
        <p className="text-lg sm:text-xl text-slate-600 max-w-3xl mx-auto font-normal leading-relaxed mb-10">
          Empowering patients, specialist doctors, and healthcare administrators with real-time clinical telemetry, instant AI symptom checking, and Vaidya AI report
        </p>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 max-w-md mx-auto mb-16">
          <Link
            to={isAuthenticated ? "/dashboard" : "/signup"}
            className="w-full sm:w-auto px-8 py-4 rounded-full font-bold text-white bg-brand-600 hover:bg-brand-700 shadow-xl shadow-brand-600/20 hover:scale-105 transition-all flex items-center justify-center gap-2.5 text-base"
          >
            <Calendar className="w-5 h-5" />
            {isAuthenticated ? `Open ${role?.toUpperCase()} Dashboard` : "Book Appointment"}
            <ArrowRight className="w-4 h-4 ml-1" />
          </Link>

          <a
            href="#vaidya-ai"
            className="w-full sm:w-auto px-7 py-4 rounded-full font-semibold text-slate-700 glass-panel hover:bg-slate-100 transition-all flex items-center justify-center gap-2 text-base text-teal-700 border border-teal-200"
          >
            <Sparkles className="w-5 h-5 text-teal-600" />
            Vaidya AI (हिंदी / English)
          </a>
        </div>

        {/* Hero Feature Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto text-left">
          <div className="glass-card rounded-3xl p-6 relative overflow-hidden group border border-slate-200 hover:border-brand-300">
            <div className="w-12 h-12 rounded-2xl bg-brand-50 border border-brand-200 flex items-center justify-center text-brand-700 mb-4 group-hover:scale-110 transition-transform">
              <Calendar className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-2">Doctor Consultations</h3>
            <p className="text-xs text-slate-600 leading-relaxed mb-4">
              Book specialist consultations across Cardiology, Neurology, and Pediatrics in Indian Rupees (₹).
            </p>
            <Link to="/doctors" className="flex items-center text-xs font-bold text-brand-700 group-hover:translate-x-1 transition-transform">
              Browse Doctors Directory <ChevronRight className="w-4 h-4" />
            </Link>
          </div>

          <div className="glass-card rounded-3xl p-6 relative overflow-hidden group border border-teal-200 hover:border-teal-400">
            <div className="w-12 h-12 rounded-2xl bg-teal-50 border border-teal-200 flex items-center justify-center text-teal-700 mb-4 group-hover:scale-110 transition-transform">
              <Brain className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-2">Vaidya AI File Analyzer</h3>
            <p className="text-xs text-slate-600 leading-relaxed mb-4">
              Upload PDF or image lab work to listen to audio diagnostic explanations in Hindi or English.
            </p>
            <a href="#vaidya-ai" className="flex items-center text-xs font-bold text-teal-700 group-hover:translate-x-1 transition-transform">
              Upload Medical File <ChevronRight className="w-4 h-4" />
            </a>
          </div>

          <div className="glass-card rounded-3xl p-6 relative overflow-hidden group border border-slate-200 hover:border-emerald-300">
            <div className="w-12 h-12 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-700 mb-4 group-hover:scale-110 transition-transform">
              <Activity className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-2">Symptom Checker</h3>
            <p className="text-xs text-slate-600 leading-relaxed mb-4">
              Describe how you feel to receive instant clinical triage and department recommendations.
            </p>
            <a href="#symptom-checker" className="flex items-center text-xs font-bold text-emerald-700 group-hover:translate-x-1 transition-transform">
              Check Symptoms <ChevronRight className="w-4 h-4" />
            </a>
          </div>
        </div>
      </section>

      {/* Feature 1: AI Symptom Checker Section */}
      <section id="symptom-checker" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="glass-card rounded-3xl p-8 sm:p-12 border border-slate-200 shadow-md">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">
            <div className="space-y-4">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-50 border border-brand-200 text-xs font-bold text-brand-700">
                <Activity className="w-3.5 h-3.5" /> Feature 1: Health Symptom Triage
              </div>
              <h2 className="text-3xl font-extrabold text-slate-900 tracking-tight">
                AI Health Symptom Checker
              </h2>
              <p className="text-slate-600 text-sm leading-relaxed">
                Describe your symptoms in plain words. Our triage engine evaluates your input and provides initial health guidance.
              </p>
              <div className="space-y-2 text-xs text-slate-700">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  <span>Immediate health risk assessment</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  <span>Recommended hospital department mapping</span>
                </div>
              </div>
            </div>

            {/* Interactive Symptom Form */}
            <div className="bg-slate-50 rounded-2xl p-6 border border-slate-200 shadow-inner">
              <form onSubmit={handleSymptomCheck} className="space-y-4">
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                    Enter Symptoms
                  </label>
                  <textarea
                    rows="3"
                    value={symptomsInput}
                    onChange={(e) => setSymptomsInput(e.target.value)}
                    placeholder="e.g. Severe headache, fever of 101F, and dry cough for 2 days"
                    className="w-full px-4 py-3 rounded-xl bg-white border border-slate-200 focus:border-brand-600 text-xs text-slate-900 placeholder-slate-400 outline-none resize-none"
                  />
                </div>

                <button
                  type="submit"
                  disabled={analyzingSymptoms || !symptomsInput.trim()}
                  className="w-full py-3 rounded-xl font-bold text-white bg-brand-600 hover:bg-brand-700 shadow-md disabled:opacity-50 transition-all flex items-center justify-center gap-2 text-xs"
                >
                  {analyzingSymptoms ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" /> Analyzing Symptoms...
                    </>
                  ) : (
                    <>
                      <Activity className="w-4 h-4" /> Analyze Symptoms Now
                    </>
                  )}
                </button>
              </form>

              {symptomError && (
                <div className="mt-4 p-3 rounded-xl bg-rose-50 border border-rose-200 text-xs text-rose-700">
                  {symptomError}
                </div>
              )}

              {symptomResult && (
                <div className="mt-4 p-5 rounded-2xl bg-white border border-brand-200 space-y-3 text-xs shadow-sm">
                  <div className="font-extrabold text-brand-900 text-sm flex items-center justify-between">
                    <span>Clinical Symptom Triage Output:</span>
                    {symptomResult.urgency && (
                      <span className="px-2.5 py-0.5 rounded-full text-[10px] uppercase font-bold bg-amber-100 text-amber-800 border border-amber-300">
                        Urgency: {symptomResult.urgency}
                      </span>
                    )}
                  </div>

                  {typeof symptomResult === 'string' ? (
                    <p className="text-slate-800 leading-relaxed whitespace-pre-wrap">{symptomResult}</p>
                  ) : (
                    <div className="space-y-3 text-slate-800">
                      {symptomResult.possible_conditions && (
                        <div>
                          <strong className="text-slate-900 block mb-1">Possible Conditions:</strong>
                          <ul className="list-disc pl-4 space-y-1 text-slate-700">
                            {symptomResult.possible_conditions.map((c, i) => (
                              <li key={i}>{c}</li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {symptomResult.recommended_department && (
                        <div>
                          <strong className="text-slate-900">Recommended Department: </strong>
                          <span className="font-bold text-brand-700">{symptomResult.recommended_department}</span>
                        </div>
                      )}

                      {symptomResult.advice && (
                        <div>
                          <strong className="text-slate-900 block mb-1">Advice:</strong>
                          <p className="text-slate-700 leading-relaxed">{symptomResult.advice}</p>
                        </div>
                      )}

                      {symptomResult.disclaimer && (
                        <div className="p-2.5 rounded-xl bg-slate-100 text-[11px] text-slate-500 italic">
                          {symptomResult.disclaimer}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* Feature 2: Vaidya AI Clinical Report File Analyzer with Voice */}
      <section id="vaidya-ai" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="glass-card rounded-3xl p-8 sm:p-12 border border-teal-200 shadow-md">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">
            <div className="space-y-4">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-50 border border-teal-200 text-xs font-bold text-teal-700">
                <Sparkles className="w-3.5 h-3.5" /> Feature 2: Vaidya AI (हिंदी / English Narration)
              </div>
              <h2 className="text-3xl font-extrabold text-slate-900 tracking-tight">
                Vaidya AI Medical Report File Analyzer
              </h2>
              <p className="text-slate-600 text-sm leading-relaxed">
                Upload blood work, X-rays, or lab diagnostic PDFs to generate an instant clinical analysis with natural audio narration in <strong>Hindi (हिंदी)</strong> or <strong>English</strong>.
              </p>
              <div className="space-y-2 text-xs text-slate-700">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-teal-600" />
                  <span>Listen to analysis in Hindi (हिंदी) or English audio</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-teal-600" />
                  <span>Supports PDF, PNG, and JPEG medical files</span>
                </div>
              </div>
            </div>

            {/* Interactive Vaidya File Upload Form */}
            <div className="bg-teal-50/50 rounded-2xl p-6 border border-teal-200 shadow-inner space-y-4">
              <form onSubmit={handleVaidyaReportAnalyze} className="space-y-4">
                <div className="p-6 rounded-xl border-2 border-dashed border-teal-300 bg-white text-center">
                  <Upload className="w-8 h-8 mx-auto text-teal-600 mb-2" />
                  <input
                    type="file"
                    accept=".pdf,.png,.jpg,.jpeg"
                    id="homepage-vaidya-file"
                    onChange={(e) => setVaidyaFile(e.target.files[0])}
                    className="hidden"
                  />
                  <label htmlFor="homepage-vaidya-file" className="cursor-pointer text-xs text-slate-700 font-bold block">
                    {vaidyaFile ? vaidyaFile.name : 'Click to select PDF or image report file'}
                  </label>
                </div>

                <button
                  type="submit"
                  disabled={analyzingReport || !vaidyaFile}
                  className="w-full py-3 rounded-xl font-bold text-white bg-teal-600 hover:bg-teal-700 shadow-md disabled:opacity-50 transition-all flex items-center justify-center gap-2 text-xs"
                >
                  {analyzingReport ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" /> Running Vaidya AI OCR & Voice Generator...
                    </>
                  ) : (
                    <>
                      <Brain className="w-4 h-4" /> Analyze Lab Report (हिंदी / English)
                    </>
                  )}
                </button>
              </form>

              {vaidyaFileError && (
                <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 text-xs text-rose-700">
                  {vaidyaFileError}
                </div>
              )}

              {vaidyaReportResult && <VaidyaReportViewer data={vaidyaReportResult} />}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
