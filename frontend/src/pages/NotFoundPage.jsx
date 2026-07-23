import React from 'react';
import { Link } from 'react-router-dom';
import { Activity, ArrowLeft } from 'lucide-react';

export const NotFoundPage = () => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center p-6 text-center">
      <div className="glass-panel rounded-3xl p-10 max-w-md w-full border border-white/10 space-y-4">
        <div className="w-16 h-16 mx-auto rounded-full bg-brand-500/10 border border-brand-500/30 flex items-center justify-center text-brand-400">
          <Activity className="w-8 h-8" />
        </div>
        <h1 className="text-6xl font-extrabold text-white">404</h1>
        <h2 className="text-xl font-bold text-slate-200">Page Not Found</h2>
        <p className="text-xs text-slate-400">
          The hospital portal link or resource you requested could not be located.
        </p>
        <Link
          to="/"
          className="inline-flex items-center gap-2 px-6 py-3 rounded-full font-bold text-white bg-brand-500 hover:bg-brand-400 shadow-lg text-xs transition-all"
        >
          <ArrowLeft className="w-4 h-4" /> Return to Homepage
        </Link>
      </div>
    </div>
  );
};
