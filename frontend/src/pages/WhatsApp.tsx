import { useState } from 'react';
import { apiService } from '../services/api';
import type { WhatsAppSendRequest, WhatsAppQueryRequest } from '../types';

const WhatsApp = () => {
  const [activeTab, setActiveTab] = useState<'query' | 'manual'>('query');

  // AI Query form
  const [queryData, setQueryData] = useState<WhatsAppQueryRequest>({
    phone_number: '',
    query: '',
  });
  const [queryLoading, setQueryLoading] = useState(false);
  const [queryResult, setQueryResult] = useState<{ type: 'success' | 'error' | 'info'; message: string } | null>(null);

  // Manual send form
  const [formData, setFormData] = useState<WhatsAppSendRequest>({
    to: '',
    message: '',
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ type: 'success' | 'error' | 'info'; message: string } | null>(null);

  const handleQuerySubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!queryData.phone_number || !queryData.query) {
      setQueryResult({
        type: 'error',
        message: '❌ Please fill in both phone number and query',
      });
      return;
    }

    // Format phone number
    let phoneNumber = queryData.phone_number.trim();
    if (phoneNumber.startsWith('0')) {
      phoneNumber = '+92' + phoneNumber.substring(1);
    }
    if (!phoneNumber.startsWith('+')) {
      phoneNumber = '+92' + phoneNumber;
    }

    const phoneRegex = /^\+\d{10,15}$/;
    if (!phoneRegex.test(phoneNumber)) {
      setQueryResult({
        type: 'error',
        message: '❌ Invalid phone number format. Use format: +923332455342 or 03332455342',
      });
      return;
    }

    setQueryLoading(true);
    setQueryResult(null);

    try {
      const response = await apiService.submitWhatsAppQuery({
        phone_number: phoneNumber,
        query: queryData.query
      });
      setQueryResult({
        type: 'success',
        message: `✅ ${response.message}\n\nAI Response Preview:\n${response.response_preview}`,
      });
      setQueryData({ phone_number: '', query: '' });
    } catch (error: any) {
      setQueryResult({
        type: 'error',
        message: `❌ Error: ${error.response?.data?.detail || error.message}`,
      });
    } finally {
      setQueryLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.to || !formData.message) {
      setResult({
        type: 'error',
        message: '❌ Please fill in both phone number and message',
      });
      return;
    }

    // Format phone number to international format
    let phoneNumber = formData.to.trim();

    // If number starts with 0 (Pakistani local format), convert to international
    if (phoneNumber.startsWith('0')) {
      phoneNumber = '+92' + phoneNumber.substring(1);
    }

    // If number doesn't start with +, assume it needs +92 (Pakistan)
    if (!phoneNumber.startsWith('+')) {
      phoneNumber = '+92' + phoneNumber;
    }

    // Validate phone number format (should be +[country code][number])
    const phoneRegex = /^\+\d{10,15}$/;
    if (!phoneRegex.test(phoneNumber)) {
      setResult({
        type: 'error',
        message: '❌ Invalid phone number format. Use format: +923332455342 or 03332455342',
      });
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await apiService.sendWhatsApp({
        to: phoneNumber,
        message: formData.message
      });
      setResult({
        type: 'success',
        message: `✅ Message sent successfully to ${phoneNumber}! Message SID: ${response.message_sid}`,
      });
      setFormData({ to: '', message: '' });
    } catch (error: any) {
      setResult({
        type: 'error',
        message: `❌ Error: ${error.response?.data?.detail || error.message}`,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-16">
      {/* Header */}
      <div className="py-12">
        <div className="flex items-center justify-center gap-4 mb-4">
          <div className="w-16 h-16 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-2xl flex items-center justify-center shadow-lg shadow-emerald-500/50">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
        </div>
        <div className="text-center">
          <h1 className="text-4xl font-bold text-white mb-2">WhatsApp Integration</h1>
          <p className="text-gray-300">Send and receive WhatsApp messages via Twilio</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex justify-center gap-4 mb-8">
        <button
          onClick={() => setActiveTab('query')}
          className={`px-8 py-3 rounded-xl font-semibold transition-all ${
            activeTab === 'query'
              ? 'bg-gradient-to-r from-emerald-500 to-teal-500 text-white shadow-lg shadow-emerald-500/50'
              : 'bg-gray-800/50 text-gray-300 hover:bg-gray-700/50'
          }`}
        >
          AI Query
        </button>
        <button
          onClick={() => setActiveTab('manual')}
          className={`px-8 py-3 rounded-xl font-semibold transition-all ${
            activeTab === 'manual'
              ? 'bg-gradient-to-r from-emerald-500 to-teal-500 text-white shadow-lg shadow-emerald-500/50'
              : 'bg-gray-800/50 text-gray-300 hover:bg-gray-700/50'
          }`}
        >
          Manual Send
        </button>
      </div>

      {/* AI Query Form */}
      {activeTab === 'query' && (
        <div className="py-12">
          <h2 className="text-3xl font-bold text-white mb-8 text-center">AI-Powered Query Response</h2>

          <form onSubmit={handleQuerySubmit} className="space-y-6 max-w-3xl mx-auto px-4">
            <div>
              <label htmlFor="query-phone" className="block text-sm font-semibold text-gray-300 mb-2">
                Customer Phone Number
              </label>
              <input
                type="text"
                id="query-phone"
                value={queryData.phone_number}
                onChange={(e) => setQueryData({ ...queryData, phone_number: e.target.value })}
                placeholder="03001234567 or +923001234567"
                className="w-full px-4 py-3 bg-gray-800/50 border-2 border-gray-600 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/50 transition-all text-white placeholder-gray-400"
              />
              <p className="text-sm text-gray-400 mt-1">
                Format: Pakistani number (03001234567) or international (+923001234567)
              </p>
            </div>

            <div>
              <label htmlFor="query-text" className="block text-sm font-semibold text-gray-300 mb-2">
                Customer Query
              </label>
              <textarea
                id="query-text"
                value={queryData.query}
                onChange={(e) => setQueryData({ ...queryData, query: e.target.value })}
                placeholder="Enter your query..."
                rows={6}
                className="w-full px-4 py-3 bg-gray-800/50 border-2 border-gray-600 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/50 transition-all resize-none text-white placeholder-gray-400"
              />
              <p className="text-sm text-gray-400 mt-1">
                The AI will generate an answer and send it to the customer
              </p>
            </div>

            <div className="flex gap-4">
              <button
                type="submit"
                disabled={queryLoading}
                className="btn-primary flex items-center gap-2"
              >
                {queryLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    <span>Processing...</span>
                  </>
                ) : (
                  <>
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                    <span>Generate & Send AI Response</span>
                  </>
                )}
              </button>

              <button
                type="button"
                onClick={() => setQueryData({ phone_number: '', query: '' })}
                className="btn-secondary"
              >
                Clear
              </button>
            </div>

            {/* Query Result Display */}
            {queryResult && (
              <div
                className={`p-6 rounded-2xl animate-fade-in border-2 ${
                  queryResult.type === 'success'
                    ? 'bg-emerald-900/30 border-emerald-500/50 text-emerald-300'
                    : queryResult.type === 'error'
                    ? 'bg-red-900/30 border-red-500/50 text-red-300'
                    : 'bg-cyan-900/30 border-cyan-500/50 text-cyan-300'
                }`}
              >
                <p className="font-medium whitespace-pre-line">{queryResult.message}</p>
              </div>
            )}
          </form>
        </div>
      )}

      {/* Manual Send Form */}
      {activeTab === 'manual' && (
      <div className="py-12">
        <h2 className="text-3xl font-bold text-white mb-8 text-center">Send WhatsApp Message</h2>

        <form onSubmit={handleSubmit} className="space-y-6 max-w-3xl mx-auto px-4">
          <div>
            <label htmlFor="phone" className="block text-sm font-semibold text-gray-300 mb-2">
              Phone Number
            </label>
            <input
              type="text"
              id="phone"
              value={formData.to}
              onChange={(e) => setFormData({ ...formData, to: e.target.value })}
              placeholder="03001234567 or +923001234567"
              className="w-full px-4 py-3 bg-gray-800/50 border-2 border-gray-600 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/50 transition-all text-white placeholder-gray-400"
            />
            <p className="text-sm text-gray-400 mt-1">
              Format: Pakistani number (03001234567) or international (+923001234567)
            </p>
          </div>

          <div>
            <label htmlFor="message" className="block text-sm font-semibold text-gray-300 mb-2">
              Message
            </label>
            <textarea
              id="message"
              value={formData.message}
              onChange={(e) => setFormData({ ...formData, message: e.target.value })}
              placeholder="Type your message here..."
              rows={6}
              className="w-full px-4 py-3 bg-gray-800/50 border-2 border-gray-600 rounded-xl focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/50 transition-all resize-none text-white placeholder-gray-400"
            />
            <p className="text-sm text-gray-400 mt-1">
              Characters: {formData.message.length} / 1600
            </p>
          </div>

          <div className="flex gap-4">
            <button
              type="submit"
              disabled={loading}
              className="btn-primary flex items-center gap-2"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  <span>Sending...</span>
                </>
              ) : (
                <>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                  <span>Send Message</span>
                </>
              )}
            </button>

            <button
              type="button"
              onClick={() => setFormData({ to: '', message: '' })}
              className="btn-secondary"
            >
              Clear
            </button>
          </div>

          {/* Result Display */}
          {result && (
            <div
              className={`p-6 rounded-2xl animate-fade-in border-2 ${
                result.type === 'success'
                  ? 'bg-emerald-900/30 border-emerald-500/50 text-emerald-300'
                  : result.type === 'error'
                  ? 'bg-red-900/30 border-red-500/50 text-red-300'
                  : 'bg-cyan-900/30 border-cyan-500/50 text-cyan-300'
              }`}
            >
              <p className="font-medium">{result.message}</p>
            </div>
          )}
        </form>
      </div>
      )}

      {/* How It Works */}
      <div className="py-12">
        <h2 className="text-3xl font-bold text-white mb-8 text-center">How WhatsApp Integration Works</h2>

        <div className="space-y-6 max-w-4xl mx-auto px-4">
          <div className="flex items-start gap-4 p-6 bg-gradient-to-br from-emerald-900/30 to-teal-900/30 rounded-2xl border-2 border-emerald-500/30">
            <div className="w-12 h-12 bg-emerald-500 text-white rounded-full flex items-center justify-center font-bold flex-shrink-0 text-xl">
              1
            </div>
            <div>
              <h3 className="text-xl font-semibold text-white mb-2">Customer Sends Message</h3>
              <p className="text-sm text-gray-300">Customer sends a WhatsApp message to your Twilio number</p>
            </div>
          </div>

          <div className="flex items-start gap-4 p-6 bg-gradient-to-br from-cyan-900/30 to-blue-900/30 rounded-2xl border-2 border-cyan-500/30">
            <div className="w-12 h-12 bg-cyan-500 text-white rounded-full flex items-center justify-center font-bold flex-shrink-0 text-xl">
              2
            </div>
            <div>
              <h3 className="text-xl font-semibold text-white mb-2">Webhook Receives Message</h3>
              <p className="text-sm text-gray-300">Twilio forwards the message to your API webhook endpoint</p>
            </div>
          </div>

          <div className="flex items-start gap-4 p-6 bg-gradient-to-br from-purple-900/30 to-pink-900/30 rounded-2xl border-2 border-purple-500/30">
            <div className="w-12 h-12 bg-purple-500 text-white rounded-full flex items-center justify-center font-bold flex-shrink-0 text-xl">
              3
            </div>
            <div>
              <h3 className="text-xl font-semibold text-white mb-2">AI Generates Response</h3>
              <p className="text-sm text-gray-300">Grok AI analyzes the message and generates an appropriate response</p>
            </div>
          </div>

          <div className="flex items-start gap-4 p-6 bg-gradient-to-br from-emerald-900/30 to-teal-900/30 rounded-2xl border-2 border-emerald-500/30">
            <div className="w-12 h-12 bg-emerald-500 text-white rounded-full flex items-center justify-center font-bold flex-shrink-0 text-xl">
              4
            </div>
            <div>
              <h3 className="text-xl font-semibold text-white mb-2">Reply Sent Automatically</h3>
              <p className="text-sm text-gray-300">The AI response is sent back to the customer via Twilio</p>
            </div>
          </div>
        </div>
      </div>

      {/* Features */}
      <div className="py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 px-4">
          <div className="text-center">
            <div className="w-16 h-16 bg-emerald-500 rounded-2xl flex items-center justify-center mb-4 shadow-lg shadow-emerald-500/50 mx-auto">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Real-Time Messaging</h3>
            <p className="text-sm text-gray-300">Instant message delivery and responses</p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-cyan-500 rounded-2xl flex items-center justify-center mb-4 shadow-lg shadow-cyan-500/50 mx-auto">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Twilio Integration</h3>
            <p className="text-sm text-gray-300">Powered by reliable Twilio infrastructure</p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-purple-500 rounded-2xl flex items-center justify-center mb-4 shadow-lg shadow-purple-500/50 mx-auto">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Secure & Reliable</h3>
            <p className="text-sm text-gray-300">End-to-end encrypted messaging</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WhatsApp;
