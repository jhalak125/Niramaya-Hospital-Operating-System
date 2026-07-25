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
          className="fixed bottom-4 right-4 sm:bottom-6 sm:right-6 z-40 px-4 sm:px-5 py-2.5 sm:py-3 rounded-full bg-gradient-to-r from-brand-600 via-teal-600 to-emerald-600 hover:from-brand-500 hover:to-emerald-500 text-white font-bold text-[11px] sm:text-sm shadow-2xl shadow-teal-500/40 hover:scale-105 transition-all flex items-center gap-2 border border-white/20 max-w-[90vw]"
        >
          <div className="w-2 h-2 rounded-full bg-emerald-400 animate-ping shrink-0" />
          <Sparkles className="w-4 h-4 text-teal-200 shrink-0" />
          <span className="truncate">Vaidya AI Report Assistant (हिंदी / English)</span>
        </button>
      )}

      {/* Floating Vaidya AI Modal Window */}
      {isOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-3 sm:p-4">
          <div className="glass-panel bg-white/98 rounded-2xl sm:rounded-3xl p-4 sm:p-8 max-w-xl w-full border border-teal-500/30 shadow-2xl space-y-4 sm:space-y-5 relative animate-in fade-in zoom-in-95 duration-200 max-h-[92vh] overflow-y-auto">
            {/* Header */}
            <div className="flex items-start justify-between gap-2">
              <div className="flex items-center gap-2.5 sm:gap-3">
                <div className="w-9 h-9 sm:w-10 sm:h-10 rounded-2xl bg-teal-50 border border-teal-200 flex items-center justify-center text-teal-600 shrink-0">
                  <Brain className="w-5 h-5" />
                </div>
                <div>
                  <div className="flex items-center gap-1.5 text-[9px] sm:text-[10px] font-bold text-teal-600 uppercase tracking-wider">
                    <Sparkles className="w-3 h-3 shrink-0" /> Vaidya AI Multilingual Report Engine
                  </div>
                  <h3 className="text-base sm:text-lg font-extrabold text-slate-900 leading-tight">Upload & Analyze Clinical Report</h3>
                </div>
              </div>
              <button
                onClick={() => setIsOpen(false)}
                className="p-1.5 rounded-full text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-all shrink-0"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs text-slate-600 leading-relaxed">
              Upload blood work, X-rays, or lab diagnostic PDFs to generate an instant clinical analysis with audio narration in <strong>Hindi (हिंदी)</strong> or <strong>English</strong>.
            </p>

            {/* Form */}
            <form onSubmit={handleAnalyzeReport} className="space-y-3 sm:space-y-4">
              <div className="p-4 sm:p-6 rounded-2xl border-2 border-dashed border-slate-200 hover:border-teal-400 bg-slate-50 text-center transition-all">
                <Upload className="w-7 h-7 sm:w-8 sm:h-8 mx-auto text-teal-600 mb-1.5" />
                <input
                  type="file"
                  accept=".pdf,.png,.jpg,.jpeg"
                  id="vaidya-popup-file"
                  onChange={(e) => setFile(e.target.files[0])}
                  className="hidden"
                />
                <label htmlFor="vaidya-popup-file" className="cursor-pointer text-xs text-slate-700 font-bold block truncate px-2">
                  {file ? file.name : 'Click to select PDF, PNG, or JPEG report file'}
                </label>
              </div>

              <button
                type="submit"
                disabled={analyzing || !file}
                className="w-full py-3 rounded-xl font-bold text-white bg-gradient-to-r from-teal-600 to-brand-600 hover:from-teal-500 hover:to-brand-500 shadow-lg shadow-teal-500/20 disabled:opacity-50 transition-all flex items-center justify-center gap-2 text-xs sm:text-sm"
              >
                {analyzing ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin text-white shrink-0" />
                    Processing Lab Report via Vaidya AI...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4 shrink-0" /> Run Vaidya AI Analysis
                  </>
                )}
              </button>
            </form>

            {error && (
              <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 text-xs text-rose-700 flex items-center gap-2">
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
