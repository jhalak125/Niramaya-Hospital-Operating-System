import React, { useState, useRef } from 'react';
import { Volume2, VolumeX, Sparkles, CheckCircle2, AlertTriangle, FileText, Globe, Stethoscope } from 'lucide-react';

export const VaidyaReportViewer = ({ data }) => {
  const [activeLang, setActiveLang] = useState('hi'); // 'hi' or 'en'
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef(null);

  if (!data) return null;

  // Extract fields from backend response
  const englishText = data.english_text || data.summary || data.findings || (typeof data === 'string' ? data : JSON.stringify(data));
  const hindiText = data.hindi_text || "आपकी मेडिकल रिपोर्ट का विवरण यहाँ उपलब्ध है।";

  const englishAudioUrl = data.english_voice ? (data.english_voice.startsWith('http') ? data.english_voice : `https://niramaya-hospital-operating-system.onrender.com${data.english_voice}`) : null;
  const hindiAudioUrl = data.hindi_voice ? (data.hindi_voice.startsWith('http') ? data.hindi_voice : `https://niramaya-hospital-operating-system.onrender.com${data.hindi_voice}`) : null;

  const currentAudioUrl = activeLang === 'hi' ? hindiAudioUrl : englishAudioUrl;
  const currentText = activeLang === 'hi' ? hindiText : englishText;

  const handleTogglePlay = () => {
    if (isPlaying) {
      if (audioRef.current) {
        audioRef.current.pause();
      }
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
      setIsPlaying(false);
    } else {
      if (currentAudioUrl) {
        if (!audioRef.current) {
          audioRef.current = new Audio(currentAudioUrl);
        } else {
          audioRef.current.src = currentAudioUrl;
        }

        audioRef.current
          .play()
          .then(() => setIsPlaying(true))
          .catch(() => speakBrowserTts(currentText, activeLang));

        audioRef.current.onended = () => setIsPlaying(false);
      } else {
        speakBrowserTts(currentText, activeLang);
      }
    }
  };

  const speakBrowserTts = (text, lang) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = lang === 'hi' ? 'hi-IN' : 'en-IN';
      utterance.onend = () => setIsPlaying(false);
      utterance.onerror = () => setIsPlaying(false);
      window.speechSynthesis.speak(utterance);
      setIsPlaying(true);
    } else {
      alert('Speech Synthesis not supported in browser.');
    }
  };

  return (
    <div className="space-y-4 rounded-2xl bg-gradient-to-br from-teal-50 to-emerald-50/60 p-3.5 sm:p-5 border border-teal-200 text-slate-800 text-xs sm:text-sm shadow-sm w-full max-w-full overflow-hidden">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-teal-200/80 pb-3">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-xl bg-teal-600 text-white flex items-center justify-center font-bold shrink-0">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h4 className="font-extrabold text-slate-900 text-xs sm:text-sm leading-tight">Vaidya AI Diagnostic Analysis</h4>
            <p className="text-[10px] text-teal-700 font-semibold">Indian Clinical Multilingual Voice Output</p>
          </div>
        </div>

        {/* Audio Language Switcher */}
        <div className="flex items-center gap-1 bg-white p-1 rounded-xl border border-teal-200 self-stretch sm:self-auto justify-center">
          <button
            type="button"
            onClick={() => {
              setActiveLang('hi');
              if (isPlaying) handleTogglePlay();
            }}
            className={`flex-1 sm:flex-none px-3 py-1 rounded-lg font-bold text-[11px] transition-all text-center ${
              activeLang === 'hi'
                ? 'bg-teal-600 text-white shadow-xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            हिंदी (Hindi)
          </button>
          <button
            type="button"
            onClick={() => {
              setActiveLang('en');
              if (isPlaying) handleTogglePlay();
            }}
            className={`flex-1 sm:flex-none px-3 py-1 rounded-lg font-bold text-[11px] transition-all text-center ${
              activeLang === 'en'
                ? 'bg-teal-600 text-white shadow-xs'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            English
          </button>
        </div>
      </div>

      {/* Voice Narration Control Bar */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2.5 p-3 rounded-xl bg-white border border-teal-200 shadow-xs">
        <div className="flex items-center gap-2">
          <Globe className="w-4 h-4 text-teal-600 shrink-0" />
          <span className="font-bold text-slate-800 text-xs">
            {activeLang === 'hi' ? 'रिपोर्ट विवरण (ऑडियो सुनें):' : 'Report Analysis Narration:'}
          </span>
        </div>

        <button
          type="button"
          onClick={handleTogglePlay}
          className={`w-full sm:w-auto px-4 py-2 sm:py-1.5 rounded-xl font-bold text-xs flex items-center justify-center gap-2 transition-all shadow-sm ${
            isPlaying
              ? 'bg-rose-600 hover:bg-rose-700 text-white'
              : 'bg-teal-600 hover:bg-teal-700 text-white'
          }`}
        >
          {isPlaying ? (
            <>
              <VolumeX className="w-4 h-4 animate-pulse" /> Pause Audio
            </>
          ) : (
            <>
              <Volume2 className="w-4 h-4" /> Listen ({activeLang === 'hi' ? 'हिंदी' : 'English'})
            </>
          )}
        </button>
      </div>

      {/* Explanation Text Box */}
      <div className="p-3.5 sm:p-4 rounded-xl bg-white border border-slate-200 leading-relaxed text-slate-800 whitespace-pre-wrap font-sans text-xs sm:text-sm break-words overflow-x-auto">
        {currentText}
      </div>

      {/* Additional Clinical Details if present */}
      {data.findings && (
        <div className="p-3.5 rounded-xl bg-white/80 border border-teal-200 space-y-1">
          <div className="font-bold text-teal-900 flex items-center gap-1.5 text-xs sm:text-sm">
            <FileText className="w-4 h-4 text-teal-600 shrink-0" /> Key Clinical Findings:
          </div>
          <p className="text-slate-700 leading-normal text-xs sm:text-sm break-words">{data.findings}</p>
        </div>
      )}
    </div>
  );
};
