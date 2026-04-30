import { useState, useEffect } from 'react';

interface ActivityItem {
  id: string;
  type: 'email' | 'whatsapp';
  timestamp: string;
  recipient: string;
  message: string;
  status: 'sent' | 'failed' | 'delivered';
}

// Mock data - in production, this would come from your API
const mockActivities: ActivityItem[] = [
  {
    id: '1',
    type: 'email',
    timestamp: '2026-04-26 10:30:45',
    recipient: 'khalidmahnoor889@gmail.com',
    message: 'what is the capital of pakistan?',
    status: 'sent'
  },
  {
    id: '2',
    type: 'whatsapp',
    timestamp: '2026-04-26 09:15:22',
    recipient: '+923332455342',
    message: 'Hello, I need help with my order',
    status: 'delivered'
  },
  {
    id: '3',
    type: 'email',
    timestamp: '2026-04-26 08:45:10',
    recipient: 'customer@example.com',
    message: 'How do I reset my password?',
    status: 'sent'
  },
  {
    id: '4',
    type: 'whatsapp',
    timestamp: '2026-04-25 23:20:33',
    recipient: '+923001234567',
    message: 'What are your business hours?',
    status: 'failed'
  },
  {
    id: '5',
    type: 'email',
    timestamp: '2026-04-25 22:10:15',
    recipient: 'support@company.com',
    message: 'I have a question about billing',
    status: 'sent'
  },
];

const Activity = () => {
  const [activities, setActivities] = useState<ActivityItem[]>(mockActivities);
  const [filter, setFilter] = useState<'all' | 'email' | 'whatsapp'>('all');
  const [searchTerm, setSearchTerm] = useState('');

  const filteredActivities = activities.filter(activity => {
    const matchesFilter = filter === 'all' || activity.type === filter;
    const matchesSearch =
      activity.recipient.toLowerCase().includes(searchTerm.toLowerCase()) ||
      activity.message.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  return (
    <div className="space-y-16">
      {/* Header */}
      <div className="py-12">
        <div className="flex items-center justify-center gap-4 mb-4">
          <div className="w-16 h-16 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg shadow-indigo-500/50">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
            </svg>
          </div>
        </div>
        <div className="text-center">
          <h1 className="text-4xl font-bold text-white mb-2">Activity Log</h1>
          <p className="text-gray-300">Track all email and WhatsApp communications</p>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="py-12">
        <div className="flex flex-col md:flex-row gap-4 max-w-5xl mx-auto px-4">
          {/* Filter Buttons */}
          <div className="flex gap-2">
            <button
              onClick={() => setFilter('all')}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                filter === 'all'
                  ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg'
                  : 'bg-gray-800/50 text-gray-300 hover:bg-gray-700/50 border border-gray-600'
              }`}
            >
              All
            </button>
            <button
              onClick={() => setFilter('email')}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                filter === 'email'
                  ? 'bg-gradient-to-r from-cyan-500 to-blue-500 text-white shadow-lg'
                  : 'bg-gray-800/50 text-gray-300 hover:bg-gray-700/50 border border-gray-600'
              }`}
            >
              Email
            </button>
            <button
              onClick={() => setFilter('whatsapp')}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                filter === 'whatsapp'
                  ? 'bg-gradient-to-r from-emerald-500 to-teal-500 text-white shadow-lg'
                  : 'bg-gray-800/50 text-gray-300 hover:bg-gray-700/50 border border-gray-600'
              }`}
            >
              WhatsApp
            </button>
          </div>

          {/* Search */}
          <div className="flex-1">
            <input
              type="text"
              placeholder="Search by recipient or message..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-4 py-2 bg-gray-800/50 border-2 border-gray-600 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/50 transition-all text-white placeholder-gray-400"
            />
          </div>
        </div>
      </div>

      {/* Activity Stats */}
      <div className="py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 px-4">
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-2xl flex items-center justify-center shadow-lg mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <p className="text-3xl font-bold text-white mb-2">{activities.length}</p>
            <p className="text-sm text-gray-300">Total Activities</p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-2xl flex items-center justify-center shadow-lg mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <p className="text-3xl font-bold text-white mb-2">
              {activities.filter(a => a.type === 'email').length}
            </p>
            <p className="text-sm text-gray-300">Emails Sent</p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-2xl flex items-center justify-center shadow-lg mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <p className="text-3xl font-bold text-white mb-2">
              {activities.filter(a => a.type === 'whatsapp').length}
            </p>
            <p className="text-sm text-gray-300">WhatsApp Sent</p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-r from-emerald-500 to-green-500 rounded-2xl flex items-center justify-center shadow-lg mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <p className="text-3xl font-bold text-white mb-2">
              {activities.filter(a => a.status === 'sent' || a.status === 'delivered').length}
            </p>
            <p className="text-sm text-gray-300">Successful</p>
          </div>
        </div>
      </div>

      {/* Activity List */}
      <div className="py-12">
        <h2 className="text-3xl font-bold text-white mb-8 text-center">Recent Activity</h2>

        {filteredActivities.length === 0 ? (
          <div className="text-center py-12">
            <svg className="w-16 h-16 text-gray-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            <p className="text-gray-400">No activities found</p>
          </div>
        ) : (
          <div className="space-y-4 max-w-5xl mx-auto px-4">
            {filteredActivities.map((activity) => (
              <div
                key={activity.id}
                className="p-6 bg-gradient-to-br from-gray-800/50 to-gray-900/50 rounded-2xl border border-gray-700 hover:shadow-lg hover:border-gray-600 transition-all"
              >
                <div className="flex items-start gap-4">
                  {/* Icon */}
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center shadow-lg flex-shrink-0 ${
                    activity.type === 'email'
                      ? 'bg-gradient-to-r from-cyan-500 to-blue-500'
                      : 'bg-gradient-to-r from-emerald-500 to-teal-500'
                  }`}>
                    {activity.type === 'email' ? (
                      <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                      </svg>
                    ) : (
                      <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                      </svg>
                    )}
                  </div>

                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-3">
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          activity.type === 'email'
                            ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/30'
                            : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                        }`}>
                          {activity.type.toUpperCase()}
                        </span>
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          activity.status === 'sent' || activity.status === 'delivered'
                            ? 'bg-green-500/20 text-green-300 border border-green-500/30'
                            : 'bg-red-500/20 text-red-300 border border-red-500/30'
                        }`}>
                          {activity.status.toUpperCase()}
                        </span>
                      </div>
                      <span className="text-sm text-gray-400">{activity.timestamp}</span>
                    </div>

                    <p className="font-semibold text-white mb-1">
                      To: {activity.recipient}
                    </p>

                    <p className="text-sm text-gray-300 truncate">
                      Message: {activity.message}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Activity;
