import { useEffect, useState } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { apiService } from '../services/api';
import type { HealthCheck, GmailStatus, WhatsAppStatus, ChannelMetrics, ActivityData } from '../types';

// Circular Progress Component
const CircularProgress = ({ percentage, label }: { percentage: number; label: string }) => {
  const radius = 70;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (percentage / 100) * circumference;

  return (
    <div className="flex flex-col items-center">
      <div className="relative w-40 h-40">
        <svg className="transform -rotate-90 w-40 h-40">
          <circle
            cx="80"
            cy="80"
            r={radius}
            stroke="#e5e7eb"
            strokeWidth="12"
            fill="none"
          />
          <circle
            cx="80"
            cy="80"
            r={radius}
            stroke="url(#gradient)"
            strokeWidth="12"
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
          <defs>
            <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#06b6d4" />
              <stop offset="100%" stopColor="#3b82f6" />
            </linearGradient>
          </defs>
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <div className="text-3xl font-bold text-white">{percentage}%</div>
            <div className="text-sm text-gray-300">{label}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Dummy data for customer satisfaction
const satisfactionData = [
  { day: 'Mon', satisfaction: 85 },
  { day: 'Tue', satisfaction: 92 },
  { day: 'Wed', satisfaction: 88 },
  { day: 'Thu', satisfaction: 95 },
  { day: 'Fri', satisfaction: 90 },
  { day: 'Sat', satisfaction: 87 },
  { day: 'Sun', satisfaction: 93 },
];

const Dashboard = () => {
  const [health, setHealth] = useState<HealthCheck | null>(null);
  const [gmailStatus, setGmailStatus] = useState<GmailStatus | null>(null);
  const [whatsappStatus, setWhatsappStatus] = useState<WhatsAppStatus | null>(null);
  const [metrics, setMetrics] = useState<ChannelMetrics | null>(null);
  const [activity, setActivity] = useState<ActivityData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStatus();
    const interval = setInterval(loadStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadStatus = async () => {
    try {
      const [healthData, gmailData, whatsappData, metricsData, activityData] = await Promise.all([
        apiService.getHealth(),
        apiService.getGmailStatus(),
        apiService.getWhatsAppStatus(),
        apiService.getChannelMetrics(),
        apiService.getActivityMetrics(7),
      ]);
      setHealth(healthData);
      setGmailStatus(gmailData);
      setWhatsappStatus(whatsappData);
      setMetrics(metricsData);
      setActivity(activityData);
    } catch (error) {
      console.error('Error loading status:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
      </div>
    );
  }

  return (
    <div className="space-y-16">
      {/* Status Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-12 px-4 py-12">
        <div className="text-center">
          <div className="flex items-center justify-center mb-4">
            <div className="w-16 h-16 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <span className={`ml-3 w-3 h-3 rounded-full ${health?.status === 'healthy' ? 'bg-emerald-500' : 'bg-red-500'} shadow-lg`}></span>
          </div>
          <h3 className="text-xl font-bold text-white mb-2">API Status</h3>
          <p className="text-3xl font-bold text-indigo-400 mb-2">{health?.status || 'Unknown'}</p>
          <p className="text-sm text-gray-300">Version {health?.version}</p>
        </div>

        <div className="text-center">
          <div className="flex items-center justify-center mb-4">
            <div className="w-16 h-16 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-2xl flex items-center justify-center shadow-lg">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <span className={`ml-3 w-3 h-3 rounded-full ${gmailStatus?.status === 'connected' ? 'bg-emerald-500' : 'bg-red-500'} shadow-lg`}></span>
          </div>
          <h3 className="text-xl font-bold text-white mb-2">Gmail</h3>
          <p className="text-3xl font-bold text-cyan-400 mb-2">{gmailStatus?.status || 'Unknown'}</p>
          <p className="text-sm text-gray-300">Email Integration</p>
        </div>

        <div className="text-center">
          <div className="flex items-center justify-center mb-4">
            <div className="w-16 h-16 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-2xl flex items-center justify-center shadow-lg">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <span className={`ml-3 w-3 h-3 rounded-full ${whatsappStatus?.status === 'configured' ? 'bg-emerald-500' : 'bg-red-500'} shadow-lg`}></span>
          </div>
          <h3 className="text-xl font-bold text-white mb-2">WhatsApp</h3>
          <p className="text-3xl font-bold text-emerald-400 mb-2">{whatsappStatus?.status || 'Unknown'}</p>
          <p className="text-sm text-gray-300">Messaging Integration</p>
        </div>
      </div>

      {/* A) Key Benefits Section - Horizontal */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-12 px-4 py-12">
        <div className="text-center">
          <div className="w-16 h-16 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-2xl flex items-center justify-center shadow-lg mx-auto mb-4">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 className="text-xl font-bold text-white mb-3">Cost Reduction</h3>
          <p className="text-sm text-gray-300">
            Reduce operational costs by up to 70% with AI-powered automation. Eliminate the need for large support teams while maintaining high-quality customer service and faster response times.
          </p>
        </div>

        <div className="text-center">
          <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center shadow-lg mx-auto mb-4">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <h3 className="text-xl font-bold text-white mb-3">AI Intelligence</h3>
          <p className="text-sm text-gray-300">
            Powered by advanced Gemini AI technology, our system understands context, sentiment, and intent to provide human-like responses. Continuously learns from interactions to improve accuracy.
          </p>
        </div>

        <div className="text-center">
          <div className="w-16 h-16 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-2xl flex items-center justify-center shadow-lg mx-auto mb-4">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <h3 className="text-xl font-bold text-white mb-3">Enterprise Ready</h3>
          <p className="text-sm text-gray-300">
            Built for scale with enterprise-grade security, multi-channel support, and seamless integrations. Handles thousands of conversations simultaneously with 99.9% uptime guarantee.
          </p>
        </div>
      </div>

      {/* B) Communication Channels - Quick Actions */}
      <div className="py-12">
        <h2 className="text-4xl font-bold text-white mb-8 text-center">Communication Channels</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 px-4">
          <a href="/gmail" className="group text-center transition-all duration-300 hover:-translate-y-2">
            <div className="w-20 h-20 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-2xl flex items-center justify-center shadow-xl mx-auto mb-4 group-hover:shadow-2xl group-hover:shadow-cyan-500/50">
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 className="font-semibold text-xl text-white mb-2">Check Emails</h3>
            <p className="text-sm text-gray-300">Process and respond to emails</p>
          </a>

          <a href="/whatsapp" className="group text-center transition-all duration-300 hover:-translate-y-2">
            <div className="w-20 h-20 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-2xl flex items-center justify-center shadow-xl mx-auto mb-4 group-hover:shadow-2xl group-hover:shadow-emerald-500/50">
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <h3 className="font-semibold text-xl text-white mb-2">Send WhatsApp</h3>
            <p className="text-sm text-gray-300">Send messages to customers</p>
          </a>
        </div>
      </div>

      {/* Success Rate Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-12 px-4 py-12">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-white mb-6">Gmail Success Rate</h2>
          <div className="flex justify-center">
            <CircularProgress
              percentage={metrics?.email.success_rate || 0}
              label="Success Rate"
            />
          </div>
          <div className="mt-6 grid grid-cols-3 gap-1 text-center">
            <div>
              <p className="text-2xl font-bold text-cyan-400">{metrics?.email.total_conversations || 0}</p>
              <p className="text-sm text-gray-300">Total Emails</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-emerald-400">{metrics?.email.resolved_count || 0}</p>
              <p className="text-sm text-gray-300">Responded</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-red-400">{metrics?.email.failed_count || 0}</p>
              <p className="text-sm text-gray-300">Failed</p>
            </div>
          </div>
        </div>

        <div className="text-center">
          <h2 className="text-2xl font-bold text-white mb-6">WhatsApp Success Rate</h2>
          <div className="flex justify-center">
            <CircularProgress
              percentage={metrics?.whatsapp.success_rate || 0}
              label="Success Rate"
            />
          </div>
          <div className="mt-6 grid grid-cols-3 gap-1 text-center">
            <div>
              <p className="text-2xl font-bold text-cyan-400">{metrics?.whatsapp.total_conversations || 0}</p>
              <p className="text-sm text-gray-300">Total Messages</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-emerald-400">{metrics?.whatsapp.resolved_count || 0}</p>
              <p className="text-sm text-gray-300">Delivered</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-red-400">{metrics?.whatsapp.failed_count || 0}</p>
              <p className="text-sm text-gray-300">Failed</p>
            </div>
          </div>
        </div>
      </div>

      {/* C) Real-time Success Analytics */}
      <div className="py-12">
        <h2 className="text-4xl font-bold text-white mb-2 text-center">Real-time Success Analytics</h2>
        <p className="text-sm text-gray-300 mb-8 text-center max-w-3xl mx-auto">
          Monitor your customer support performance in real-time. Track message volumes, response times, and success rates across all communication channels.
        </p>

        {/* Activity Graphs */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8 px-4">
          <div>
            <h3 className="text-2xl font-bold text-white mb-4 text-center">Gmail Activity (Last 7 Hours)</h3>
            <div className="p-6 bg-gradient-to-br from-gray-800/50 to-gray-900/50 rounded-2xl border border-gray-700">
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={activity?.email || []}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="time" stroke="#9ca3af" />
                  <YAxis stroke="#9ca3af" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1f2937',
                      border: '1px solid #374151',
                      borderRadius: '8px',
                      color: '#fff'
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="emails"
                    stroke="#06b6d4"
                    strokeWidth={3}
                    dot={{ fill: '#06b6d4', r: 5 }}
                    activeDot={{ r: 7 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div>
            <h3 className="text-2xl font-bold text-white mb-4 text-center">WhatsApp Activity (Last 7 Hours)</h3>
            <div className="p-6 bg-gradient-to-br from-gray-800/50 to-gray-900/50 rounded-2xl border border-gray-700">
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={activity?.whatsapp || []}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="time" stroke="#9ca3af" />
                  <YAxis stroke="#9ca3af" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1f2937',
                      border: '1px solid #374151',
                      borderRadius: '8px',
                      color: '#fff'
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="messages"
                    stroke="#10b981"
                    strokeWidth={3}
                    dot={{ fill: '#10b981', r: 5 }}
                    activeDot={{ r: 7 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Customer Satisfaction Trends */}
        <div className="px-4 mt-24">
          <h3 className="text-3xl font-bold text-white mb-6 text-center">Customer Satisfaction Trends</h3>
          <div className="p-6 bg-gradient-to-br from-gray-800/50 to-gray-900/50 rounded-2xl border border-gray-700">
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={satisfactionData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="day" stroke="#9ca3af" />
                <YAxis stroke="#9ca3af" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1f2937',
                    border: '1px solid #374151',
                    borderRadius: '8px',
                    color: '#fff'
                  }}
                />
                <Bar dataKey="satisfaction" fill="url(#barGradient)" radius={[8, 8, 0, 0]} />
                <defs>
                  <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#8b5cf6" />
                    <stop offset="100%" stopColor="#ec4899" />
                  </linearGradient>
                </defs>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* D) Business Impact */}
      <div className="py-12">
        <h2 className="text-4xl font-bold text-white mb-2 text-center">Business Impact</h2>
        <p className="text-sm text-gray-300 mb-8 text-center max-w-3xl mx-auto">
          Measure the tangible impact of AI-powered customer support on your business operations and customer experience.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 px-4">
          {/* Operational Efficiency */}
          <div className="p-6 bg-gradient-to-br from-cyan-900/30 to-blue-900/30 rounded-2xl border-2 border-cyan-500/30">
            <h3 className="text-xl font-bold text-white mb-4">Operational Efficiency</h3>
            <ul className="space-y-3">
              <li className="flex items-start gap-3">
                <svg className="w-5 h-5 text-cyan-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="text-sm text-gray-300">70% reduction in response time with instant AI replies</span>
              </li>
              <li className="flex items-start gap-3">
                <svg className="w-5 h-5 text-cyan-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="text-sm text-gray-300">24/7 availability without additional staffing costs</span>
              </li>
              <li className="flex items-start gap-3">
                <svg className="w-5 h-5 text-cyan-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="text-sm text-gray-300">Handle 10x more conversations simultaneously</span>
              </li>
              <li className="flex items-start gap-3">
                <svg className="w-5 h-5 text-cyan-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="text-sm text-gray-300">Automated ticket routing and prioritization</span>
              </li>
              <li className="flex items-start gap-3">
                <svg className="w-5 h-5 text-cyan-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="text-sm text-gray-300">Consistent quality across all customer interactions</span>
              </li>
            </ul>
          </div>

          {/* AI Capabilities */}
          <div className="p-6 bg-gradient-to-br from-purple-900/30 to-pink-900/30 rounded-2xl border-2 border-purple-500/30">
            <h3 className="text-xl font-bold text-white mb-4">AI Capabilities</h3>
            <ul className="space-y-3">
              <li className="flex items-start gap-3">
                <svg className="w-5 h-5 text-purple-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="text-sm text-gray-300">Natural language understanding with context awareness</span>
              </li>
              <li className="flex items-start gap-3">
                <svg className="w-5 h-5 text-purple-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="text-sm text-gray-300">Sentiment analysis for emotional intelligence</span>
              </li>
              <li className="flex items-start gap-3">
                <svg className="w-5 h-5 text-purple-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="text-sm text-gray-300">Multi-language support for global customers</span>
              </li>
              <li className="flex items-start gap-3">
                <svg className="w-5 h-5 text-purple-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="text-sm text-gray-300">Continuous learning from customer interactions</span>
              </li>
              <li className="flex items-start gap-3">
                <svg className="w-5 h-5 text-purple-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="text-sm text-gray-300">Smart escalation to human agents when needed</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* System Info */}
      <div className="py-12">
        <h2 className="text-4xl font-bold text-white mb-8 text-center">System Information</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 px-4">
          <div className="text-center">
            <p className="text-sm text-gray-400 uppercase tracking-wide mb-2">API Server</p>
            <p className="font-semibold text-white">http://localhost:8001</p>
          </div>
          <div className="text-center">
            <p className="text-sm text-gray-400 uppercase tracking-wide mb-2">Email Channel</p>
            <p className="font-semibold text-emerald-400">{health?.channels.email ? 'Enabled' : 'Disabled'}</p>
          </div>
          <div className="text-center">
            <p className="text-sm text-gray-400 uppercase tracking-wide mb-2">WhatsApp Channel</p>
            <p className="font-semibold text-emerald-400">{health?.channels.whatsapp ? 'Enabled' : 'Disabled'}</p>
          </div>
          <div className="text-center">
            <p className="text-sm text-gray-400 uppercase tracking-wide mb-2">AI Model</p>
            <p className="font-semibold text-white">Grok AI</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
