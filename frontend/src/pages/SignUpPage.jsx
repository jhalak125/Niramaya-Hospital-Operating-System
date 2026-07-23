import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  User,
  Mail,
  Lock,
  Phone,
  ArrowRight,
  CheckCircle,
  AlertCircle,
  Stethoscope,
  ShieldCheck,
} from 'lucide-react';
import logoImg from '../assets/logo.png';

export const SignUpPage = () => {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    password: '',
    phone: '',
    role: 'patient',
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.full_name || !formData.email || !formData.password || !formData.phone) {
      setError('Please fill in all required fields.');
      return;
    }

    setLoading(true);
    setError('');
    setSuccessMsg('');

    try {
      await register(formData);
      setSuccessMsg('Account registered successfully! Redirecting to sign in...');
      setTimeout(() => {
        navigate('/signin', { state: { message: 'Registration successful! Please sign in.' } });
      }, 1200);
    } catch (err) {
      setError(err.message || 'Registration failed. Please check your details.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center py-24 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      <div className="max-w-xl w-full space-y-8 glass-panel bg-white/95 rounded-3xl p-8 sm:p-10 border border-slate-200 shadow-xl relative z-10">
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
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Create your account</h2>
          <p className="text-xs text-slate-500">
            Join Niramaya Hospital System for intelligent healthcare management
          </p>
        </div>

        {error && (
          <div className="p-3.5 rounded-2xl bg-rose-50 border border-rose-200 text-xs text-rose-700 flex items-center gap-2 animate-in fade-in">
            <AlertCircle className="w-4 h-4 shrink-0 text-rose-600" />
            <span>{error}</span>
          </div>
        )}

        {successMsg && (
          <div className="p-3.5 rounded-2xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-700 flex items-center gap-2 animate-in fade-in">
            <CheckCircle className="w-4 h-4 shrink-0 text-emerald-600" />
            <span>{successMsg}</span>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Account Role Badge (Patient Only) */}
          <div className="p-3.5 rounded-2xl bg-brand-50 border border-brand-200 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-xl bg-brand-600 text-white flex items-center justify-center font-bold">
                <User className="w-4 h-4" />
              </div>
              <div>
                <p className="text-xs font-bold text-slate-900">Patient Registration</p>
                <p className="text-[11px] text-slate-500">Access medical records & book doctor consultations</p>
              </div>
            </div>
            <span className="px-2.5 py-1 rounded-full text-[10px] uppercase font-extrabold tracking-wider bg-brand-600 text-white">
              Patient
            </span>
          </div>

          {/* Full Name */}
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Full Name
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                <User className="w-4 h-4" />
              </div>
              <input
                type="text"
                required
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
                placeholder="Dr. Eleanor Vance / Jane Doe"
                className="w-full pl-10 pr-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:border-brand-600 focus:ring-1 focus:ring-brand-600 text-sm text-slate-900 placeholder-slate-400 outline-none transition-all"
              />
            </div>
          </div>

          {/* Email & Phone grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
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
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="name@niramaya.org"
                  className="w-full pl-10 pr-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:border-brand-600 focus:ring-1 focus:ring-brand-600 text-sm text-slate-900 placeholder-slate-400 outline-none transition-all"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Phone Number
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                  <Phone className="w-4 h-4" />
                </div>
                <input
                  type="tel"
                  required
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                  placeholder="+91 98765 43210"
                  className="w-full pl-10 pr-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:border-brand-600 focus:ring-1 focus:ring-brand-600 text-sm text-slate-900 placeholder-slate-400 outline-none transition-all"
                />
              </div>
            </div>
          </div>

          {/* Password */}
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Password
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                <Lock className="w-4 h-4" />
              </div>
              <input
                type="password"
                required
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="At least 6 characters"
                className="w-full pl-10 pr-4 py-3 rounded-xl bg-slate-50 border border-slate-200 focus:border-brand-600 focus:ring-1 focus:ring-brand-600 text-sm text-slate-900 placeholder-slate-400 outline-none transition-all"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full mt-2 py-3.5 rounded-xl font-bold text-white bg-brand-600 hover:bg-brand-700 shadow-md shadow-brand-600/20 disabled:opacity-50 transition-all flex items-center justify-center gap-2 text-sm"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Creating Account...
              </>
            ) : (
              <>
                Register Account <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* Footer link */}
        <div className="text-center text-xs text-slate-600">
          Already have a Niramaya account?{' '}
          <Link to="/signin" className="font-bold text-brand-600 hover:text-brand-700 underline">
            Sign in here
          </Link>
        </div>
      </div>
    </div>
  );
};
