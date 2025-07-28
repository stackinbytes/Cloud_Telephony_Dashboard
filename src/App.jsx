import React, { useState } from 'react';
import CallForm from './components/CallForm';
import CallTable from './components/CallTable';

const App = () => {
  const [refreshKey, setRefreshKey] = useState(0);

  const refreshCalls = () => {
    setRefreshKey(prev => prev + 1);
  };

  return (
    <div className="min-h-screen bg-gray-100 text-gray-800">
      <header className="bg-white shadow p-4">
        <h1 className="text-3xl font-bold text-center">📞 Cloud Telephony Dashboard</h1>
      </header>
      <main className="max-w-6xl mx-auto py-6 px-4 space-y-8">
        <CallForm onSuccess={refreshCalls} />
        <CallTable key={refreshKey} />
      </main>
    </div>
  );
};

export default App;
