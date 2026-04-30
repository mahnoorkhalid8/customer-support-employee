import type { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';

interface LayoutProps {
  children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <div className="min-h-screen p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm rounded-2xl shadow-2xl p-6 mb-8 border border-gray-700">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/50">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
                  Customer Success AI
                </h1>
                <p className="text-sm text-gray-400">24/7 AI-Powered Support</p>
              </div>
            </div>

            {/* Navigation */}
            <nav className="flex gap-2">
              <Link
                to="/"
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  isActive('/')
                    ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg shadow-indigo-500/50'
                    : 'text-gray-300 hover:bg-gray-700/50 hover:text-white'
                }`}
              >
                Dashboard
              </Link>
              <Link
                to="/gmail"
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  isActive('/gmail')
                    ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg shadow-indigo-500/50'
                    : 'text-gray-300 hover:bg-gray-700/50 hover:text-white'
                }`}
              >
                Gmail
              </Link>
              <Link
                to="/whatsapp"
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  isActive('/whatsapp')
                    ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg shadow-indigo-500/50'
                    : 'text-gray-300 hover:bg-gray-700/50 hover:text-white'
                }`}
              >
                WhatsApp
              </Link>
              <Link
                to="/activity"
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  isActive('/activity')
                    ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg shadow-indigo-500/50'
                    : 'text-gray-300 hover:bg-gray-700/50 hover:text-white'
                }`}
              >
                Activity
              </Link>
              <Link
                to="/reports"
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  isActive('/reports')
                    ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg shadow-indigo-500/50'
                    : 'text-gray-300 hover:bg-gray-700/50 hover:text-white'
                }`}
              >
                Reports
              </Link>
              <Link
                to="/settings"
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  isActive('/settings')
                    ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg shadow-indigo-500/50'
                    : 'text-gray-300 hover:bg-gray-700/50 hover:text-white'
                }`}
              >
                Settings
              </Link>
            </nav>
          </div>
        </header>

        {/* Main Content */}
        <main>{children}</main>

        {/* Footer */}
        <footer className="mt-8 text-center text-gray-400 text-sm">
          <p>Powered by Grok AI • Built with React + TypeScript + Tailwind CSS</p>
        </footer>
      </div>
    </div>
  );
};

export default Layout;
