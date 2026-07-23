import React from 'react';
import { Link } from 'react-router-dom';
import { Heart, Sparkles, Activity, ShieldCheck, Code } from 'lucide-react';
import logoImg from '../../assets/logo.png';

export const Footer = () => {
  return (
    <footer className="bg-slate-900 text-slate-300 pt-12 pb-8 border-t border-slate-800 relative overflow-hidden">
      {/* Top Gradient Bar */}
      <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-brand-500 via-teal-500 to-emerald-500" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-start">
          
          {/* Column 1: Website Branding & Developer Credits */}
          <div className="space-y-3">
            <Link to="/" className="inline-flex items-center gap-3 group">
              <div className="w-10 h-10 rounded-full bg-white border border-brand-300 p-0.5 flex items-center justify-center overflow-hidden">
                <img src={logoImg} alt="Niramaya Logo" className="w-full h-full object-cover rounded-full" />
              </div>
              <span className="font-extrabold text-2xl tracking-tight text-white group-hover:text-brand-400 transition-colors">
                NIRAMAYA
              </span>
            </Link>

            <p className="text-xs text-slate-400 leading-relaxed max-w-sm">
              AI-Powered Healthcare Web Platform featuring clinical symptom triage and Vaidya AI diagnostic report narrations.
            </p>

            <div className="pt-2 flex items-center gap-2 text-xs font-bold text-teal-400">
              <Code className="w-4 h-4 text-teal-400 shrink-0" />
              <span>Developed by <span className="text-white underline font-extrabold">Jhalak Verma</span></span>
            </div>
          </div>

          {/* Column 2: Platform Navigation */}
          <div className="space-y-3">
            <h4 className="text-sm font-extrabold uppercase tracking-wider text-white">Platform Features</h4>
            <ul className="space-y-2 text-xs text-slate-400">
              <li>
                <Link to="/doctors" className="hover:text-white transition-colors flex items-center gap-2">
                  <Activity className="w-3.5 h-3.5 text-brand-400" /> Specialist Doctors Directory
                </Link>
              </li>
              <li>
                <a href="#symptom-checker" className="hover:text-white transition-colors flex items-center gap-2">
                  <Activity className="w-3.5 h-3.5 text-emerald-400" /> Free AI Symptom Checker
                </a>
              </li>
              <li>
                <a href="#vaidya-ai" className="hover:text-white transition-colors flex items-center gap-2">
                  <Sparkles className="w-3.5 h-3.5 text-teal-400" /> Free Vaidya AI Report File Analyzer (हिंदी / English)
                </a>
              </li>
            </ul>
          </div>

          {/* Column 3: Quick Portal Access */}
          <div className="space-y-3">
            <h4 className="text-sm font-extrabold uppercase tracking-wider text-white">User Workspaces</h4>
            <ul className="space-y-2 text-xs text-slate-400">
              <li>
                <Link to="/signin" className="hover:text-white transition-colors flex items-center gap-2">
                  <ShieldCheck className="w-3.5 h-3.5 text-amber-400" /> Patient Workspace Portal
                </Link>
              </li>
              <li>
                <Link to="/signin" className="hover:text-white transition-colors flex items-center gap-2">
                  <ShieldCheck className="w-3.5 h-3.5 text-teal-400" /> Doctor Clinical Workspace
                </Link>
              </li>
              <li>
                <Link to="/signin" className="hover:text-white transition-colors flex items-center gap-2">
                  <ShieldCheck className="w-3.5 h-3.5 text-brand-400" /> Executive Admin Workspace
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Copyright & Credit Bar */}
        <div className="pt-6 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
          <p>© {new Date().getFullYear()} Niramaya Healthcare Platform. Designed & Developed by <strong className="text-slate-300">Jhalak Verma</strong>.</p>
          <div className="flex items-center gap-1 text-slate-400">
            <span>Built with</span>
            <Heart className="w-3.5 h-3.5 text-rose-500 fill-rose-500" />
            <span>by Jhalak Verma</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
