import React, { useState, useEffect } from 'react';
import { Sparkles, X, Upload, Brain, AlertCircle, Loader2 } from 'lucide-react';
import { medicalService } from '../../services/medicalService';
import { VaidyaReportViewer } from '../ai/VaidyaReportViewer';

export const VaidyaAiPopup = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  // Form & Result State
  const [file, setFile] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 250) {
        setIsVisible(true);
      } else {
        setIsVisible(false);
      }
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleAnalyzeReport = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a PDF or image medical report file.');
      return;
    }

    setAnalyzing(true);
    setError('');
    setResult(null);

    try {
      const fd = new FormData();
      fd.append('file', file);
      const res = await medicalService.analyzeMedicalReport(fd);
      setResult(res?.data || res);
    } catch (err) {
      setError(err.message || 'Failed to process report file');
    } finally {
      setAnalyzing(false);
    }
  };

  if (!isVisible && !isOpen) return null;

  return (
    <>
      {/* Floating Trigger Button (Bottom-Right) */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 z-40 px-5 py-3 rounded-full bg-gradient-to-r from-brand-600 via-teal-600 to-emerald-600 hover:from-brand-500 hover:to-emerald-500 text-white font-bold text-xs sm:text-sm shadow-2xl shadow-teal-500/40 hover:scale-105 transition-all flex items-center gap-2.5 animate-bounce-slow border border-white/20"
        >
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping" />
          <Sparkles className="w-4 h-4 text-teal-200" />
          <span>Vaidya AI Report Assistant (हिंदी / English)</span>
        </button>
      )}

      {/* Floating Vaidya AI Modal Window */}
      {isOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-panel bg-white/95 rounded-3xl p-6 sm:p-8 max-w-lg w-full border border-teal-500/30 shadow-2xl space-y-5 relative animate-in fade-in zoom-in-95 duration-200 max-h-[90vh] overflow-y-auto">
            {/* Header */}
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-2xl bg-teal-50 border border-teal-200 flex items-center justify-center text-teal-600">
                  <Brain className="w-5 h-5" />
                </div>
                <div>
                  <div className="flex items-center gap-1.5 text-[10px] font-bold text-teal-600 uppercase tracking-wider">
                    <Sparkles className="w-3 h-3" /> Vaidya AI Multilingual Report Engine
                  </div>
                  <h3 className="text-lg font-extrabold text-slate-900">Upload & Analyze Clinical Report</h3>
                </div>
              </div>
              <button
                onClick={() => setIsOpen(false)}
                className="p-1.5 rounded-full text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-all"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs text-slate-600 leading-relaxed">
              Upload blood work, X-rays, or lab diagnostic PDFs to generate an instant clinical analysis with audio narration in <strong>Hindi (हिंदी)</strong> or <strong>English</strong>.
            </p>

            {/* Form */}
            <form onSubmit={handleAnalyzeReport} className="space-y-4">
              <div className="p-6 rounded-2xl border-2 border-dashed border-slate-200 hover:border-teal-400 bg-slate-50 text-center transition-all">
                <Upload className="w-8 h-8 mx-auto text-teal-600 mb-2" />
                <input
                  type="file"
                  accept=".pdf,.png,.jpg,.jpeg"
                  id="vaidya-popup-file"
                  onChange={(e) => setFile(e.target.files[0])}
                  className="hidden"
                />
                <label htmlFor="vaidya-popup-file" className="cursor-pointer text-xs text-slate-700 font-bold block">
                  {file ? file.name : 'Click to select PDF, PNG, or JPEG report file'}
                </label>
              </div>

              <button
                type="submit"
                disabled={analyzing || !file}
                className="w-full py-3 rounded-xl font-bold text-white bg-gradient-to-r from-teal-600 to-brand-600 hover:from-teal-500 hover:to-brand-500 shadow-lg shadow-teal-500/20 disabled:opacity-50 transition-all flex items-center justify-center gap-2 text-xs"
              >
                {analyzing ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin text-white" />
                    Processing Lab Report via Vaidya AI...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4" /> Run Vaidya AI Analysis
                  </>
                )}
              </button>
            </form>

            {error && (
              <div className="p-3.5 rounded-xl bg-rose-50 border border-rose-200 text-xs text-rose-700 flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0" /> {error}
              </div>
            )}

            {result && <VaidyaReportViewer data={result} />}
          </div>
        </div>
      )}
    </>
  );
};
