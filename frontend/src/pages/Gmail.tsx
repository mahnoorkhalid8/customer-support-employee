import { useState } from 'react';
import { apiService } from '../services/api';

const Gmail = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ type: 'success' | 'error' | 'info'; message: string; preview?: string } | null>(null);

  // Form state
  const [formData, setFormData] = useState({
    user_email: '',
    user_name: '',
    query: ''
  });

  const handleSubmitQuery = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const response = await apiService.submitQuery(formData);
      setResult({
        type: 'success',
        message: response.message,
        preview: response.response_preview
      });

      // Clear form on success
      setFormData({
        user_email: '',
        user_name: '',
        query: ''
      });
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
          <div className="w-16 h-16 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-2xl flex items-center justify-center shadow-lg shadow-cyan-500/50">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
        </div>
        <div className="text-center">
          <h1 className="text-4xl font-bold text-white mb-2">Gmail Support Dashboard</h1>
          <p className="text-gray-300">Submit customer queries and get AI-powered email responses</p>
        </div>
      </div>

      {/* Query Submission Form */}
      <div className="py-12">
        <h2 className="text-3xl font-bold text-white mb-8 text-center">Submit Customer Query</h2>

        <form onSubmit={handleSubmitQuery} className="space-y-6 max-w-3xl mx-auto px-4">
          <div className="p-6 bg-gradient-to-br from-cyan-900/30 to-blue-900/30 rounded-2xl border-2 border-cyan-500/30 mb-6">
            <h3 className="text-xl font-semibold text-white mb-4">How It Works</h3>
            <ul className="space-y-3 text-gray-300">
              <li className="flex items-start gap-2">
                <span className="text-cyan-400 font-bold">1.</span>
                <span>User enters their email, name, and query in the form below</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-cyan-400 font-bold">2.</span>
                <span>Grok AI analyzes the query and generates an appropriate response</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-cyan-400 font-bold">3.</span>
                <span>AI-generated response is sent directly to the user's email</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-cyan-400 font-bold">4.</span>
                <span>User receives professional support response in their inbox</span>
              </li>
            </ul>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Customer Email *
            </label>
            <input
              type="email"
              required
              value={formData.user_email}
              onChange={(e) => setFormData({ ...formData, user_email: e.target.value })}
              placeholder="customer@example.com"
              className="w-full px-4 py-3 bg-gray-800/50 border-2 border-gray-600 rounded-xl focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/50 transition-all text-white placeholder-gray-400"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Customer Name (Optional)
            </label>
            <input
              type="text"
              value={formData.user_name}
              onChange={(e) => setFormData({ ...formData, user_name: e.target.value })}
              placeholder="John Doe"
              className="w-full px-4 py-3 bg-gray-800/50 border-2 border-gray-600 rounded-xl focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/50 transition-all text-white placeholder-gray-400"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Customer Query *
            </label>
            <textarea
              required
              value={formData.query}
              onChange={(e) => setFormData({ ...formData, query: e.target.value })}
              placeholder="Hi, I need help with my order. Can you assist me with tracking information?"
              rows={6}
              className="w-full px-4 py-3 bg-gray-800/50 border-2 border-gray-600 rounded-xl focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/50 transition-all resize-none text-white placeholder-gray-400"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-primary flex items-center gap-2 w-full justify-center"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                <span>Generating AI Response & Sending Email...</span>
              </>
            ) : (
              <>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
                <span>Submit Query & Send AI Response</span>
              </>
            )}
          </button>
        </form>

        {/* Result Display */}
        {result && (
          <div className="max-w-3xl mx-auto px-4 mt-6">
            <div
              className={`p-6 rounded-2xl animate-fade-in border-2 ${
                result.type === 'success'
                  ? 'bg-emerald-900/30 border-emerald-500/50 text-emerald-300'
                  : result.type === 'error'
                  ? 'bg-red-900/30 border-red-500/50 text-red-300'
                  : 'bg-cyan-900/30 border-cyan-500/50 text-cyan-300'
              }`}
            >
              <p className="font-medium mb-2">{result.message}</p>
              {result.preview && (
                <div className="mt-3 p-4 bg-gray-800/50 rounded-xl border border-gray-600">
                  <p className="text-sm font-semibold mb-2 text-white">AI Response Preview:</p>
                  <p className="text-sm text-gray-300">{result.preview}</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Features */}
      <div className="py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 px-4">
          <div className="text-center">
            <div className="w-16 h-16 bg-cyan-500 rounded-2xl flex items-center justify-center mb-4 shadow-lg shadow-cyan-500/50 mx-auto">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Instant Responses</h3>
            <p className="text-sm text-gray-300">AI generates and sends replies within seconds</p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-indigo-500 rounded-2xl flex items-center justify-center mb-4 shadow-lg shadow-indigo-500/50 mx-auto">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Smart Context</h3>
            <p className="text-sm text-gray-300">Understands query context and customer intent</p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-emerald-500 rounded-2xl flex items-center justify-center mb-4 shadow-lg shadow-emerald-500/50 mx-auto">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Email Delivery</h3>
            <p className="text-sm text-gray-300">Responses sent directly to customer's inbox</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Gmail;
