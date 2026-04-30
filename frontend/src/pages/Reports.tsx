import { useState } from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

// Mock data for reports
const monthlyData = [
  { month: 'Jan', emails: 245, whatsapp: 189, resolved: 398, escalated: 36 },
  { month: 'Feb', emails: 312, whatsapp: 234, resolved: 501, escalated: 45 },
  { month: 'Mar', emails: 289, whatsapp: 267, resolved: 512, escalated: 44 },
  { month: 'Apr', emails: 356, whatsapp: 298, resolved: 601, escalated: 53 },
];

const channelDistribution = [
  { name: 'Email', value: 1202, color: '#06b6d4' },
  { name: 'WhatsApp', value: 988, color: '#10b981' },
];

const responseTimeData = [
  { category: 'Instant (< 1min)', count: 1456 },
  { category: 'Fast (1-5min)', count: 534 },
  { category: 'Moderate (5-15min)', count: 156 },
  { category: 'Slow (> 15min)', count: 44 },
];

const satisfactionData = [
  { rating: '5 Stars', count: 1234 },
  { rating: '4 Stars', count: 678 },
  { rating: '3 Stars', count: 234 },
  { rating: '2 Stars', count: 89 },
  { rating: '1 Star', count: 45 },
];

const Reports = () => {
  const [dateRange, setDateRange] = useState('last-30-days');

  // Export to CSV
  const exportToCSV = () => {
    const csvData = [
      ['Customer Success AI - Reports & Analytics'],
      ['Date Range:', dateRange],
      [''],
      ['Key Metrics Summary'],
      ['Metric', 'Value', 'Change'],
      ['Total Conversations', '2,190', '+12.5%'],
      ['Resolution Rate', '94.2%', '+2.1%'],
      ['Avg Response Time', '45s', '-23%'],
      ['Satisfaction Score', '4.7/5', '+0.3'],
      [''],
      ['Monthly Trends'],
      ['Month', 'Emails', 'WhatsApp', 'Resolved', 'Escalated'],
      ...monthlyData.map(row => [row.month, row.emails, row.whatsapp, row.resolved, row.escalated]),
      [''],
      ['Channel Distribution'],
      ['Channel', 'Count'],
      ...channelDistribution.map(row => [row.name, row.value]),
      [''],
      ['Response Time Distribution'],
      ['Category', 'Count'],
      ...responseTimeData.map(row => [row.category, row.count]),
      [''],
      ['Customer Satisfaction'],
      ['Rating', 'Count'],
      ...satisfactionData.map(row => [row.rating, row.count]),
      [''],
      ['Performance Insights'],
      ['Top Performing'],
      ['Email Response Rate', '98.5%'],
      ['First Contact Resolution', '89.2%'],
      ['Customer Retention', '94.7%'],
      [''],
      ['Needs Attention'],
      ['Escalation Rate', '8.1%'],
      ['Avg Handle Time', '3.2 min'],
      ['Repeat Contact Rate', '12.3%'],
      [''],
      ['AI Performance'],
      ['AI Accuracy', '96.8%'],
      ['Auto-Resolution', '87.4%'],
      ['Learning Rate', '+15.2%'],
    ];

    const csvContent = csvData.map(row => row.join(',')).join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `customer-success-report-${dateRange}-${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Export to Excel (using CSV format with .xls extension for compatibility)
  const exportToExcel = () => {
    const csvData = [
      ['Customer Success AI - Reports & Analytics'],
      ['Date Range:', dateRange],
      [''],
      ['Key Metrics Summary'],
      ['Metric', 'Value', 'Change'],
      ['Total Conversations', '2,190', '+12.5%'],
      ['Resolution Rate', '94.2%', '+2.1%'],
      ['Avg Response Time', '45s', '-23%'],
      ['Satisfaction Score', '4.7/5', '+0.3'],
      [''],
      ['Monthly Trends'],
      ['Month', 'Emails', 'WhatsApp', 'Resolved', 'Escalated'],
      ...monthlyData.map(row => [row.month, row.emails, row.whatsapp, row.resolved, row.escalated]),
      [''],
      ['Channel Distribution'],
      ['Channel', 'Count'],
      ...channelDistribution.map(row => [row.name, row.value]),
      [''],
      ['Response Time Distribution'],
      ['Category', 'Count'],
      ...responseTimeData.map(row => [row.category, row.count]),
      [''],
      ['Customer Satisfaction'],
      ['Rating', 'Count'],
      ...satisfactionData.map(row => [row.rating, row.count]),
      [''],
      ['Performance Insights'],
      ['Top Performing'],
      ['Email Response Rate', '98.5%'],
      ['First Contact Resolution', '89.2%'],
      ['Customer Retention', '94.7%'],
      [''],
      ['Needs Attention'],
      ['Escalation Rate', '8.1%'],
      ['Avg Handle Time', '3.2 min'],
      ['Repeat Contact Rate', '12.3%'],
      [''],
      ['AI Performance'],
      ['AI Accuracy', '96.8%'],
      ['Auto-Resolution', '87.4%'],
      ['Learning Rate', '+15.2%'],
    ];

    const csvContent = csvData.map(row => row.join('\t')).join('\n');
    const blob = new Blob([csvContent], { type: 'application/vnd.ms-excel' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `customer-success-report-${dateRange}-${new Date().toISOString().split('T')[0]}.xls`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Export to PDF
  const exportToPDF = () => {
    const printContent = `
      <!DOCTYPE html>
      <html>
      <head>
        <title>Customer Success AI - Reports & Analytics</title>
        <style>
          body { font-family: Arial, sans-serif; padding: 20px; }
          h1 { color: #4f46e5; }
          h2 { color: #6366f1; margin-top: 30px; }
          table { width: 100%; border-collapse: collapse; margin: 20px 0; }
          th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
          th { background-color: #4f46e5; color: white; }
          .metric { display: inline-block; margin: 10px 20px 10px 0; }
          .metric-label { font-weight: bold; color: #666; }
          .metric-value { font-size: 24px; font-weight: bold; color: #4f46e5; }
        </style>
      </head>
      <body>
        <h1>Customer Success AI - Reports & Analytics</h1>
        <p><strong>Date Range:</strong> ${dateRange}</p>
        <p><strong>Generated:</strong> ${new Date().toLocaleString()}</p>

        <h2>Key Metrics Summary</h2>
        <div class="metric">
          <div class="metric-label">Total Conversations</div>
          <div class="metric-value">2,190</div>
          <div>↑ 12.5% from last period</div>
        </div>
        <div class="metric">
          <div class="metric-label">Resolution Rate</div>
          <div class="metric-value">94.2%</div>
          <div>↑ 2.1% from last period</div>
        </div>
        <div class="metric">
          <div class="metric-label">Avg Response Time</div>
          <div class="metric-value">45s</div>
          <div>↓ 23% faster</div>
        </div>
        <div class="metric">
          <div class="metric-label">Satisfaction Score</div>
          <div class="metric-value">4.7/5</div>
          <div>↑ 0.3 points</div>
        </div>

        <h2>Monthly Conversation Trends</h2>
        <table>
          <thead>
            <tr>
              <th>Month</th>
              <th>Emails</th>
              <th>WhatsApp</th>
              <th>Resolved</th>
              <th>Escalated</th>
            </tr>
          </thead>
          <tbody>
            ${monthlyData.map(row => `
              <tr>
                <td>${row.month}</td>
                <td>${row.emails}</td>
                <td>${row.whatsapp}</td>
                <td>${row.resolved}</td>
                <td>${row.escalated}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>

        <h2>Channel Distribution</h2>
        <table>
          <thead>
            <tr>
              <th>Channel</th>
              <th>Count</th>
            </tr>
          </thead>
          <tbody>
            ${channelDistribution.map(row => `
              <tr>
                <td>${row.name}</td>
                <td>${row.value}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>

        <h2>Response Time Distribution</h2>
        <table>
          <thead>
            <tr>
              <th>Category</th>
              <th>Count</th>
            </tr>
          </thead>
          <tbody>
            ${responseTimeData.map(row => `
              <tr>
                <td>${row.category}</td>
                <td>${row.count}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>

        <h2>Customer Satisfaction Breakdown</h2>
        <table>
          <thead>
            <tr>
              <th>Rating</th>
              <th>Count</th>
            </tr>
          </thead>
          <tbody>
            ${satisfactionData.map(row => `
              <tr>
                <td>${row.rating}</td>
                <td>${row.count}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>

        <h2>Performance Insights</h2>
        <h3>Top Performing</h3>
        <ul>
          <li>Email Response Rate: 98.5%</li>
          <li>First Contact Resolution: 89.2%</li>
          <li>Customer Retention: 94.7%</li>
        </ul>

        <h3>Needs Attention</h3>
        <ul>
          <li>Escalation Rate: 8.1%</li>
          <li>Avg Handle Time: 3.2 min</li>
          <li>Repeat Contact Rate: 12.3%</li>
        </ul>

        <h3>AI Performance</h3>
        <ul>
          <li>AI Accuracy: 96.8%</li>
          <li>Auto-Resolution: 87.4%</li>
          <li>Learning Rate: +15.2%</li>
        </ul>
      </body>
      </html>
    `;

    const printWindow = window.open('', '_blank');
    if (printWindow) {
      printWindow.document.write(printContent);
      printWindow.document.close();
      printWindow.focus();
      setTimeout(() => {
        printWindow.print();
        printWindow.close();
      }, 250);
    }
  };

  return (
    <div className="space-y-16">
      {/* Header */}
      <div className="py-12">
        <div className="flex items-center justify-center gap-4 mb-4">
          <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl flex items-center justify-center shadow-lg shadow-purple-500/50">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
        </div>
        <div className="text-center mb-6">
          <h1 className="text-4xl font-bold text-white mb-2">Reports & Analytics</h1>
          <p className="text-gray-300">Comprehensive insights into your customer support performance</p>
        </div>

        {/* Date Range Selector */}
        <div className="flex justify-center">
          <select
            value={dateRange}
            onChange={(e) => setDateRange(e.target.value)}
            className="px-4 py-2 bg-gray-800/50 border-2 border-gray-600 rounded-lg focus:border-purple-500 focus:ring-2 focus:ring-purple-500/50 transition-all text-white"
          >
            <option value="last-7-days">Last 7 Days</option>
            <option value="last-30-days">Last 30 Days</option>
            <option value="last-90-days">Last 90 Days</option>
            <option value="this-year">This Year</option>
          </select>
        </div>
      </div>

      {/* Key Metrics Summary */}
      <div className="py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 px-4">
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-2xl flex items-center justify-center shadow-lg mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <h3 className="text-sm font-semibold text-gray-400 mb-2">Total Conversations</h3>
            <p className="text-4xl font-bold text-white mb-1">2,190</p>
            <p className="text-sm text-emerald-400">↑ 12.5% from last period</p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-2xl flex items-center justify-center shadow-lg mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-sm font-semibold text-gray-400 mb-2">Resolution Rate</h3>
            <p className="text-4xl font-bold text-white mb-1">94.2%</p>
            <p className="text-sm text-emerald-400">↑ 2.1% from last period</p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center shadow-lg mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-sm font-semibold text-gray-400 mb-2">Avg Response Time</h3>
            <p className="text-4xl font-bold text-white mb-1">45s</p>
            <p className="text-sm text-emerald-400">↓ 23% faster</p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-2xl flex items-center justify-center shadow-lg mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
              </svg>
            </div>
            <h3 className="text-sm font-semibold text-gray-400 mb-2">Satisfaction Score</h3>
            <p className="text-4xl font-bold text-white mb-1">4.7/5</p>
            <p className="text-sm text-emerald-400">↑ 0.3 points</p>
          </div>
        </div>
      </div>

      {/* Monthly Trends */}
      <div className="py-12">
        <h2 className="text-3xl font-bold text-white mb-8 text-center">Monthly Conversation Trends</h2>
        <div className="px-4">
          <div className="p-6 bg-gradient-to-br from-gray-800/50 to-gray-900/50 rounded-2xl border border-gray-700">
            <ResponsiveContainer width="100%" height={350}>
              <LineChart data={monthlyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="month" stroke="#9ca3af" />
                <YAxis stroke="#9ca3af" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1f2937',
                    border: '1px solid #374151',
                    borderRadius: '8px',
                    color: '#fff'
                  }}
                />
                <Legend />
                <Line type="monotone" dataKey="emails" stroke="#06b6d4" strokeWidth={3} name="Emails" />
                <Line type="monotone" dataKey="whatsapp" stroke="#10b981" strokeWidth={3} name="WhatsApp" />
                <Line type="monotone" dataKey="resolved" stroke="#8b5cf6" strokeWidth={3} name="Resolved" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Channel Distribution & Response Time */}
      <div className="py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 px-4">
          <div>
            <h2 className="text-2xl font-bold text-white mb-6 text-center">Channel Distribution</h2>
            <div className="p-6 bg-gradient-to-br from-gray-800/50 to-gray-900/50 rounded-2xl border border-gray-700">
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={channelDistribution}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {channelDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px', color: '#fff' }} />
                </PieChart>
              </ResponsiveContainer>
              <div className="mt-4 grid grid-cols-2 gap-4">
                <div className="text-center p-3 bg-cyan-900/30 rounded-lg border border-cyan-500/30">
                  <p className="text-2xl font-bold text-cyan-400">1,202</p>
                  <p className="text-sm text-gray-300">Email Messages</p>
                </div>
                <div className="text-center p-3 bg-emerald-900/30 rounded-lg border border-emerald-500/30">
                  <p className="text-2xl font-bold text-emerald-400">988</p>
                  <p className="text-sm text-gray-300">WhatsApp Messages</p>
                </div>
              </div>
            </div>
          </div>

          <div>
            <h2 className="text-2xl font-bold text-white mb-6 text-center">Response Time Distribution</h2>
            <div className="p-6 bg-gradient-to-br from-gray-800/50 to-gray-900/50 rounded-2xl border border-gray-700">
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={responseTimeData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="category" stroke="#9ca3af" angle={-15} textAnchor="end" height={80} />
                  <YAxis stroke="#9ca3af" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1f2937',
                      border: '1px solid #374151',
                      borderRadius: '8px',
                      color: '#fff'
                    }}
                  />
                  <Bar dataKey="count" fill="url(#responseGradient)" radius={[8, 8, 0, 0]} />
                  <defs>
                    <linearGradient id="responseGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#06b6d4" />
                      <stop offset="100%" stopColor="#3b82f6" />
                    </linearGradient>
                  </defs>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>

      {/* Customer Satisfaction Breakdown */}
      <div className="py-12">
        <h2 className="text-3xl font-bold text-white mb-8 text-center">Customer Satisfaction Breakdown</h2>
        <div className="px-4">
          <div className="p-6 bg-gradient-to-br from-gray-800/50 to-gray-900/50 rounded-2xl border border-gray-700">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={satisfactionData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis type="number" stroke="#9ca3af" />
                <YAxis dataKey="rating" type="category" stroke="#9ca3af" width={100} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1f2937',
                    border: '1px solid #374151',
                    borderRadius: '8px',
                    color: '#fff'
                  }}
                />
                <Bar dataKey="count" fill="url(#satisfactionGradient)" radius={[0, 8, 8, 0]} />
                <defs>
                  <linearGradient id="satisfactionGradient" x1="0" y1="0" x2="1" y2="0">
                    <stop offset="0%" stopColor="#f59e0b" />
                    <stop offset="100%" stopColor="#ef4444" />
                  </linearGradient>
                </defs>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Performance Insights */}
      <div className="py-12">
        <h2 className="text-3xl font-bold text-white mb-8 text-center">Performance Insights</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 px-4">
          <div className="p-6 bg-gradient-to-br from-emerald-900/30 to-green-900/30 rounded-2xl border-2 border-emerald-500/30">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 bg-gradient-to-r from-emerald-500 to-green-500 rounded-xl flex items-center justify-center shadow-lg">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white">Top Performing</h3>
            </div>
            <ul className="space-y-2">
              <li className="flex justify-between items-center p-3 bg-emerald-500/10 rounded-lg border border-emerald-500/20">
                <span className="text-sm text-gray-300">Email Response Rate</span>
                <span className="font-bold text-emerald-400">98.5%</span>
              </li>
              <li className="flex justify-between items-center p-3 bg-emerald-500/10 rounded-lg border border-emerald-500/20">
                <span className="text-sm text-gray-300">First Contact Resolution</span>
                <span className="font-bold text-emerald-400">89.2%</span>
              </li>
              <li className="flex justify-between items-center p-3 bg-emerald-500/10 rounded-lg border border-emerald-500/20">
                <span className="text-sm text-gray-300">Customer Retention</span>
                <span className="font-bold text-emerald-400">94.7%</span>
              </li>
            </ul>
          </div>

          <div className="p-6 bg-gradient-to-br from-yellow-900/30 to-orange-900/30 rounded-2xl border-2 border-yellow-500/30">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-xl flex items-center justify-center shadow-lg">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white">Needs Attention</h3>
            </div>
            <ul className="space-y-2">
              <li className="flex justify-between items-center p-3 bg-yellow-500/10 rounded-lg border border-yellow-500/20">
                <span className="text-sm text-gray-300">Escalation Rate</span>
                <span className="font-bold text-yellow-400">8.1%</span>
              </li>
              <li className="flex justify-between items-center p-3 bg-yellow-500/10 rounded-lg border border-yellow-500/20">
                <span className="text-sm text-gray-300">Avg Handle Time</span>
                <span className="font-bold text-yellow-400">3.2 min</span>
              </li>
              <li className="flex justify-between items-center p-3 bg-yellow-500/10 rounded-lg border border-yellow-500/20">
                <span className="text-sm text-gray-300">Repeat Contact Rate</span>
                <span className="font-bold text-yellow-400">12.3%</span>
              </li>
            </ul>
          </div>

          <div className="p-6 bg-gradient-to-br from-purple-900/30 to-pink-900/30 rounded-2xl border-2 border-purple-500/30">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center shadow-lg">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white">AI Performance</h3>
            </div>
            <ul className="space-y-2">
              <li className="flex justify-between items-center p-3 bg-purple-500/10 rounded-lg border border-purple-500/20">
                <span className="text-sm text-gray-300">AI Accuracy</span>
                <span className="font-bold text-purple-400">96.8%</span>
              </li>
              <li className="flex justify-between items-center p-3 bg-purple-500/10 rounded-lg border border-purple-500/20">
                <span className="text-sm text-gray-300">Auto-Resolution</span>
                <span className="font-bold text-purple-400">87.4%</span>
              </li>
              <li className="flex justify-between items-center p-3 bg-purple-500/10 rounded-lg border border-purple-500/20">
                <span className="text-sm text-gray-300">Learning Rate</span>
                <span className="font-bold text-purple-400">+15.2%</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Export Options */}
      <div className="py-12">
        <h2 className="text-3xl font-bold text-white mb-4 text-center">Export Reports</h2>
        <p className="text-sm text-gray-300 mb-8 text-center">Download detailed reports in various formats for further analysis</p>
        <div className="flex justify-center gap-4 px-4">
          <button onClick={exportToPDF} className="btn-primary flex items-center gap-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Export as PDF
          </button>
          <button onClick={exportToCSV} className="btn-secondary flex items-center gap-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Export as CSV
          </button>
          <button onClick={exportToExcel} className="btn-secondary flex items-center gap-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Export as Excel
          </button>
        </div>
      </div>
    </div>
  );
};

export default Reports;
