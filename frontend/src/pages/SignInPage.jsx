import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  Mail,
  Lock,
  ArrowRight,
  ShieldCheck,
  AlertCircle,
} from 'lucide-react';
import logoImg from '../assets/logo.png';

export const SignInPage = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const redirectMessage = location.state?.message;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email || !password) {
      setError('Please fill in both email and password.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      await login(email.trim(), password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message || 'Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center py-24 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      {/* Background ambient light blobs */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[400px] bg-brand-500/10 rounded-full blur-[140px] pointer-events-none -z-10" />

      <div className="max-w-md w-full space-y-8 glass-panel bg-white/95 rounded-3xl p-8 sm:p-10 border border-slate-200 shadow-xl relative z-10">
        {/* Header */}
        <div className="text-center space-y-3">
          <Link to="/" className="inline-flex items-center gap-3 group mb-2">
            <div className="w-12 h-12 rounded-full bg-slate-50 border border-brand-200 p-1 flex items-center justify-center shadow-md group-hover:scale-105 transition-transform">
              <img src={logoImg} alt="Niramaya Logo" className="w-full h-full object-cover rounded-full" />
            </div>
            <span className="font-extrabold text-2xl tracking-tight text-slate-900 group-hover:text-brand-600 transition-colors">
              NIRAMAYA
            </span>
          </Link>
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Sign in to your portal</h2>
          <p className="text-xs text-slate-500">
            Access your secure NIRAMAYA Healthcare account
          </p>
        </div>

        {redirectMessage && (
          <div className="p-3.5 rounded-2xl bg-brand-50 border border-brand-200 text-xs text-brand-700 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0 text-brand-600" />
            <span>{redirectMessage}</span>
          </div>
        )}

        {error && (
          <div className="p-3.5 rounded-2xl bg-rose-50 border border-rose-200 text-xs text-rose-700 flex items-center gap-2 animate-in fade-in">
            <AlertCircle className="w-4 h-4 shrink-0 text-rose-600" />
            <span>{error}</span>
          </div>
        )}

        {/* Credentials Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Email Address
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                <Mail className="w-4 h-4" />
              </div>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="w-full pl-10 pr-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:border-brand-600 focus:ring-1 focus:ring-brand-600 text-sm text-slate-900 placeholder-slate-400 outline-none transition-all"
              />
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
                Password
              </label>
            </div>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                <Lock className="w-4 h-4" />
              </div>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-10 pr-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:border-brand-600 focus:ring-1 focus:ring-brand-600 text-sm text-slate-900 placeholder-slate-400 outline-none transition-all"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 rounded-xl font-bold text-white bg-brand-600 hover:bg-brand-700 shadow-md shadow-brand-600/20 disabled:opacity-50 transition-all flex items-center justify-center gap-2 text-sm"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Signing In...
              </>
            ) : (
              <>
                Sign In to Account <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* Footer link */}
        <div className="text-center pt-4 border-t border-slate-100 text-xs text-slate-600">
          Don't have a Niramaya account?{' '}
          <Link to="/signup" className="font-bold text-brand-600 hover:text-brand-700 underline">
            Register here
          </Link>
        </div>
      </div>
    </div>
  );
};
