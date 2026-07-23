import React, { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { notificationService } from '../../services/notificationService';
import {
  Bell,
  LogOut,
  LayoutDashboard,
  Menu,
  X,
  Sparkles,
  ChevronDown,
  Check,
  Trash2,
} from 'lucide-react';
import logoImg from '../../assets/logo.png';

export const Navbar = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [userDropdownOpen, setUserDropdownOpen] = useState(false);
  const [notifDropdownOpen, setNotifDropdownOpen] = useState(false);
  const [notifications, setNotifications] = useState([]);

  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Fetch notifications if logged in
  useEffect(() => {
    if (isAuthenticated) {
      const fetchNotifs = async () => {
        try {
          const res = await notificationService.getMyNotifications();
          setNotifications(Array.isArray(res) ? res : res?.data || []);
        } catch (err) {
          // Silent catch for notifications
        }
      };
      fetchNotifs();
    }
  }, [isAuthenticated, location]);

  const navigateToSection = (sectionId) => {
    setMobileMenuOpen(false);
    if (location.pathname !== '/') {
      navigate('/');
      setTimeout(() => {
        const el = document.getElementById(sectionId);
        if (el) {
          el.scrollIntoView({ behavior: 'smooth' });
        }
      }, 150);
    } else {
      const el = document.getElementById(sectionId);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  const handleLogout = () => {
    logout();
    setUserDropdownOpen(false);
    navigate('/');
  };

  const handleMarkRead = async (id) => {
    try {
      await notificationService.markAsRead(id);
      setNotifications((prev) =>
        prev.map((n) => (n._id === id ? { ...n, is_read: true } : n))
      );
    } catch (err) {}
  };

  const handleDeleteNotif = async (id) => {
    try {
      await notificationService.deleteNotification(id);
      setNotifications((prev) => prev.filter((n) => n._id !== id));
    } catch (err) {}
  };

  const unreadCount = notifications.filter((n) => !n.is_read).length;

  return (
    <header className="fixed top-4 left-1/2 -translate-x-1/2 z-50 w-[94%] max-w-7xl">
      <nav
        className={`glass-nav transition-all duration-300 px-4 sm:px-6 py-2.5 ${
          mobileMenuOpen ? 'rounded-3xl bg-white/98 shadow-2xl border-slate-300' : 'rounded-full'
        } ${
          isScrolled ? 'shadow-xl bg-white/95 border-slate-300' : 'bg-white/85 border-slate-200'
        }`}
      >
        <div className="flex items-center justify-between">
          {/* Logo Branding */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="relative flex items-center justify-center w-10 h-10 rounded-full bg-white border border-brand-200 shadow-md group-hover:scale-105 transition-transform overflow-hidden">
              <img
                src={logoImg}
                alt="Niramaya Hospital Logo"
                className="w-full h-full object-cover"
              />
            </div>
            <div className="flex flex-col">
              <span className="font-extrabold text-lg sm:text-xl tracking-tight text-slate-900 group-hover:text-brand-600 transition-colors">
                NIRAMAYA
              </span>
              <span className="text-[9px] uppercase tracking-widest text-brand-600 font-bold -mt-1 hidden sm:inline">
                Hospital System
              </span>
            </div>
          </Link>

          {/* Desktop Navigation Links */}
          <div className="hidden md:flex items-center gap-1 lg:gap-2 bg-slate-100/80 p-1.5 rounded-full border border-slate-200">
            <Link
              to="/"
              className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all duration-200 ${
                location.pathname === '/'
                  ? 'bg-white text-brand-700 shadow-sm font-semibold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
              }`}
            >
              Home
            </Link>
            <Link
              to="/doctors"
              className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all duration-200 ${
                location.pathname === '/doctors'
                  ? 'bg-white text-brand-700 shadow-sm font-semibold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
              }`}
            >
              Doctors
            </Link>
            <button
              onClick={() => navigateToSection('symptom-checker')}
              className="px-4 py-1.5 rounded-full text-sm font-medium text-slate-600 hover:text-slate-900 hover:bg-white/60 transition-all duration-200"
            >
              Symptom Checker
            </button>
            <button
              onClick={() => navigateToSection('vaidya-ai')}
              className="px-4 py-1.5 rounded-full text-sm font-semibold text-teal-700 hover:bg-teal-50 flex items-center gap-1.5 transition-all duration-200"
            >
              <Sparkles className="w-3.5 h-3.5 text-teal-600 animate-pulse" />
              Vaidya AI
            </button>
          </div>

          {/* Notifications & User Profile */}
          <div className="hidden md:flex items-center gap-3">
            {isAuthenticated ? (
              <div className="flex items-center gap-2">
                {/* Notification Bell Dropdown */}
                <div className="relative">
                  <button
                    onClick={() => {
                      setNotifDropdownOpen(!notifDropdownOpen);
                      setUserDropdownOpen(false);
                    }}
                    className="p-2 rounded-full bg-slate-100 hover:bg-slate-200 border border-slate-300 text-slate-700 relative transition-all"
                  >
                    <Bell className="w-4 h-4" />
                    {unreadCount > 0 && (
                      <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-rose-600 text-white text-[9px] font-bold flex items-center justify-center animate-pulse">
                        {unreadCount}
                      </span>
                    )}
                  </button>

                  {/* Notification Dropdown Drawer */}
                  {notifDropdownOpen && (
                    <div className="absolute right-0 mt-3 w-80 glass-panel rounded-2xl p-3 shadow-xl border border-slate-200 text-xs z-50 bg-white space-y-2">
                      <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                        <span className="font-bold text-slate-900 text-sm">Notifications System</span>
                        <span className="text-[10px] bg-brand-50 text-brand-700 font-bold px-2 py-0.5 rounded-full border border-brand-200">
                          {notifications.length} Total
                        </span>
                      </div>

                      <div className="max-h-60 overflow-y-auto divide-y divide-slate-100">
                        {notifications.length === 0 ? (
                          <div className="text-center py-4 text-slate-400">No active notifications.</div>
                        ) : (
                          notifications.map((n) => (
                            <div key={n._id} className="py-2 space-y-1">
                              <div className="flex items-start justify-between gap-2">
                                <span className={`font-bold ${n.is_read ? 'text-slate-600' : 'text-slate-900'}`}>
                                  {n.title || 'System Notification'}
                                </span>
                                <div className="flex items-center gap-1">
                                  {!n.is_read && (
                                    <button
                                      onClick={() => handleMarkRead(n._id)}
                                      className="p-1 text-emerald-600 hover:bg-emerald-50 rounded"
                                      title="Mark read"
                                    >
                                      <Check className="w-3.5 h-3.5" />
                                    </button>
                                  )}
                                  <button
                                    onClick={() => handleDeleteNotif(n._id)}
                                    className="p-1 text-rose-600 hover:bg-rose-50 rounded"
                                    title="Delete"
                                  >
                                    <Trash2 className="w-3.5 h-3.5" />
                                  </button>
                                </div>
                              </div>
                              <p className="text-[11px] text-slate-600 leading-tight">{n.message}</p>
                            </div>
                          ))
                        )}
                      </div>
                    </div>
                  )}
                </div>

                {/* User Dropdown */}
                <div className="relative">
                  <button
                    onClick={() => {
                      setUserDropdownOpen(!userDropdownOpen);
                      setNotifDropdownOpen(false);
                    }}
                    className="flex items-center gap-2.5 px-3.5 py-1.5 rounded-full bg-slate-100 hover:bg-slate-200/80 border border-slate-300 text-slate-800 transition-all shadow-sm"
                  >
                    <div className="w-7 h-7 rounded-full bg-brand-600 text-white flex items-center justify-center text-xs font-bold uppercase">
                      {user?.full_name?.charAt(0) || 'U'}
                    </div>
                    <div className="text-left hidden lg:block">
                      <p className="text-xs font-bold text-slate-900 leading-tight">
                        {user?.full_name?.split(' ')[0]}
                      </p>
                      <p className="text-[10px] text-brand-600 uppercase tracking-wider font-mono font-bold">
                        {user?.role}
                      </p>
                    </div>
                    <ChevronDown className="w-4 h-4 text-slate-500" />
                  </button>

                  {userDropdownOpen && (
                    <div className="absolute right-0 mt-3 w-56 glass-panel rounded-2xl p-2 shadow-xl border border-slate-200 text-sm z-50 animate-in fade-in zoom-in-95 duration-150 bg-white">
                      <div className="px-3 py-2 border-b border-slate-100">
                        <p className="font-bold text-slate-900 truncate">{user?.full_name}</p>
                        <p className="text-xs text-slate-500 truncate">{user?.email}</p>
                        <span className="inline-block mt-1 px-2.5 py-0.5 text-[10px] uppercase font-bold tracking-wider rounded-full bg-brand-50 text-brand-700 border border-brand-200">
                          Role: {user?.role}
                        </span>
                      </div>

                      <div className="py-1">
                        <Link
                          to="/dashboard"
                          onClick={() => setUserDropdownOpen(false)}
                          className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-slate-700 hover:bg-brand-50 hover:text-brand-700 transition-colors text-xs font-semibold"
                        >
                          <LayoutDashboard className="w-4 h-4 text-brand-600" />
                          Dashboard Workspace
                        </Link>
                      </div>

                      <div className="pt-1 border-t border-slate-100">
                        <button
                          onClick={handleLogout}
                          className="w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-rose-600 hover:bg-rose-50 transition-colors text-xs font-semibold"
                        >
                          <LogOut className="w-4 h-4" />
                          Sign Out
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  to="/signin"
                  className="px-4 py-1.5 rounded-full text-sm font-semibold text-slate-700 hover:text-slate-900 hover:bg-slate-100 transition-all"
                >
                  Sign In
                </Link>
                <Link
                  to="/signup"
                  className="px-5 py-1.5 rounded-full text-sm font-semibold bg-brand-600 hover:bg-brand-700 text-white shadow-md shadow-brand-600/20 hover:scale-105 transition-all"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Toggle */}
          <div className="flex md:hidden items-center gap-2">
            {isAuthenticated && (
              <Link
                to="/dashboard"
                className="p-2 rounded-full bg-brand-50 text-brand-700 border border-brand-200"
              >
                <LayoutDashboard className="w-4 h-4" />
              </Link>
            )}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-full bg-slate-100 text-slate-700 border border-slate-300"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation Drawer */}
        {mobileMenuOpen && (
          <div className="md:hidden mt-4 pt-4 border-t border-slate-200 flex flex-col gap-2 pb-2">
            <Link
              to="/"
              onClick={() => setMobileMenuOpen(false)}
              className="px-4 py-2 rounded-xl text-slate-700 hover:bg-slate-100"
            >
              Home
            </Link>
            <Link
              to="/doctors"
              onClick={() => setMobileMenuOpen(false)}
              className="px-4 py-2 rounded-xl text-slate-700 hover:bg-slate-100"
            >
              Doctors Directory
            </Link>
            <button
              onClick={() => navigateToSection('symptom-checker')}
              className="px-4 py-2 rounded-xl text-slate-700 hover:bg-slate-100 text-left"
            >
              Symptom Checker
            </button>
            <button
              onClick={() => navigateToSection('vaidya-ai')}
              className="px-4 py-2 rounded-xl text-teal-700 font-semibold hover:bg-teal-50 flex items-center gap-2 text-left"
            >
              <Sparkles className="w-4 h-4" />
              Vaidya AI Assistant
            </button>

            {!isAuthenticated ? (
              <div className="mt-2 pt-2 border-t border-slate-200 flex flex-col gap-2">
                <Link
                  to="/signin"
                  onClick={() => setMobileMenuOpen(false)}
                  className="w-full text-center py-2 rounded-xl border border-slate-300 text-slate-800 font-medium"
                >
                  Sign In
                </Link>
                <Link
                  to="/signup"
                  onClick={() => setMobileMenuOpen(false)}
                  className="w-full text-center py-2 rounded-xl bg-brand-600 text-white font-semibold shadow-md"
                >
                  Sign Up
                </Link>
              </div>
            ) : (
              <div className="mt-2 pt-2 border-t border-slate-200 flex flex-col gap-2">
                <Link
                  to="/dashboard"
                  onClick={() => setMobileMenuOpen(false)}
                  className="flex items-center gap-2 px-4 py-2 rounded-xl bg-brand-50 text-brand-700 font-semibold"
                >
                  <LayoutDashboard className="w-4 h-4" />
                  Open {user?.role?.toUpperCase()} Workspace
                </Link>
                <button
                  onClick={() => {
                    handleLogout();
                    setMobileMenuOpen(false);
                  }}
                  className="flex items-center gap-2 px-4 py-2 rounded-xl text-rose-600 hover:bg-rose-50"
                >
                  <LogOut className="w-4 h-4" />
                  Sign Out
                </button>
              </div>
            )}
          </div>
        )}
      </nav>
    </header>
  );
};
