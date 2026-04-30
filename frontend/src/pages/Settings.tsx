const Settings = () => {
  return (
    <div className="space-y-16">
      {/* Header */}
      <div className="py-12">
        <div className="flex items-center justify-center gap-4 mb-4">
          <div className="w-16 h-16 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg shadow-indigo-500/50">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
        </div>
        <div className="text-center">
          <h1 className="text-4xl font-bold text-white mb-2">Settings</h1>
          <p className="text-gray-300">Configure your AI customer support system</p>
        </div>
      </div>

      {/* API Configuration */}
      <div className="py-12">
        <h2 className="text-3xl font-bold text-white mb-8 text-center">API Configuration</h2>
        <div className="max-w-4xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-300 mb-2">API Server URL</label>
              <input
                type="text"
                value="http://localhost:8001"
                readOnly
                className="w-full px-4 py-3 bg-gray-800/50 border-2 border-gray-600 rounded-xl text-white"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-300 mb-2">API Version</label>
              <input
                type="text"
                value="v2.0.0"
                readOnly
                className="w-full px-4 py-3 bg-gray-800/50 border-2 border-gray-600 rounded-xl text-white"
              />
            </div>
          </div>
        </div>
      </div>

      {/* AI Model Settings */}
      <div className="py-12">
        <h2 className="text-3xl font-bold text-white mb-8 text-center">AI Model Settings</h2>
        <div className="max-w-4xl mx-auto px-4 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-300 mb-2">AI Provider</label>
              <input
                type="text"
                value="Grok AI (xAI)"
                readOnly
                className="w-full px-4 py-3 bg-gray-800/50 border-2 border-gray-600 rounded-xl text-white"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-300 mb-2">Model</label>
              <input
                type="text"
                value="grok-1"
                readOnly
                className="w-full px-4 py-3 bg-gray-800/50 border-2 border-gray-600 rounded-xl text-white"
              />
            </div>
          </div>
          <div className="p-6 bg-gradient-to-br from-cyan-900/30 to-blue-900/30 border-2 border-cyan-500/30 rounded-2xl">
            <p className="text-sm text-gray-300">
              <strong className="text-white">Note:</strong> AI model settings are configured in the <code className="bg-cyan-500/20 px-2 py-1 rounded text-cyan-300 border border-cyan-500/30">.env</code> file on the server.
            </p>
          </div>
        </div>
      </div>

      {/* Integration Status */}
      <div className="py-12">
        <h2 className="text-3xl font-bold text-white mb-8 text-center">Integration Status</h2>
        <div className="max-w-4xl mx-auto px-4 space-y-4">
          <div className="flex items-center justify-between p-6 bg-gradient-to-br from-cyan-900/30 to-blue-900/30 rounded-2xl border-2 border-cyan-500/30">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-cyan-500 rounded-xl flex items-center justify-center shadow-lg shadow-cyan-500/50">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <div>
                <h3 className="text-xl font-semibold text-white">Gmail Integration</h3>
                <p className="text-sm text-gray-300">OAuth2 authenticated</p>
              </div>
            </div>
            <span className="px-4 py-2 bg-emerald-500/20 text-emerald-300 rounded-full text-sm font-semibold border border-emerald-500/30">Active</span>
          </div>

          <div className="flex items-center justify-between p-6 bg-gradient-to-br from-emerald-900/30 to-teal-900/30 rounded-2xl border-2 border-emerald-500/30">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-emerald-500 rounded-xl flex items-center justify-center shadow-lg shadow-emerald-500/50">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <div>
                <h3 className="text-xl font-semibold text-white">WhatsApp Integration</h3>
                <p className="text-sm text-gray-300">Twilio configured</p>
              </div>
            </div>
            <span className="px-4 py-2 bg-emerald-500/20 text-emerald-300 rounded-full text-sm font-semibold border border-emerald-500/30">Active</span>
          </div>
        </div>
      </div>

      {/* Documentation Links */}
      <div className="py-12">
        <h2 className="text-3xl font-bold text-white mb-8 text-center">Documentation & Resources</h2>
        <div className="max-w-4xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <a
              href="http://localhost:8001/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="p-6 bg-gradient-to-br from-cyan-900/30 to-blue-900/30 rounded-2xl border-2 border-cyan-500/30 hover:border-cyan-400 transition-all hover:shadow-lg hover:shadow-cyan-500/20"
            >
              <h3 className="text-xl font-semibold text-white mb-2">API Documentation</h3>
              <p className="text-sm text-gray-300">Interactive Swagger UI</p>
            </a>

            <div className="p-6 bg-gradient-to-br from-emerald-900/30 to-teal-900/30 rounded-2xl border-2 border-emerald-500/30">
              <h3 className="text-xl font-semibold text-white mb-2">Setup Guides</h3>
              <p className="text-sm text-gray-300">COMPLETE_GUIDE.md, NGROK_SETUP.md</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
