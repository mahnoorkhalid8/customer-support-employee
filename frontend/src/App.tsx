import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Gmail from './pages/Gmail';
import WhatsApp from './pages/WhatsApp';
import Activity from './pages/Activity';
import Reports from './pages/Reports';
import Settings from './pages/Settings';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/gmail" element={<Gmail />} />
          <Route path="/whatsapp" element={<WhatsApp />} />
          <Route path="/activity" element={<Activity />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
