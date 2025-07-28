import React, { useEffect, useState } from 'react';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000';

const CallTable = () => {
  const [calls, setCalls] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState('');
  const [sortOrder, setSortOrder] = useState('desc');
  const [searchNumber, setSearchNumber] = useState('');

  const fetchCalls = async () => {
    try {
      const res = await axios.get(`${API_BASE}/calls`);
      setCalls(res.data);
    } catch (err) {
      console.error('Failed to fetch calls:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCalls(); // initial load
    const interval = setInterval(fetchCalls, 10000); // auto-refresh every 10s
    return () => clearInterval(interval); // cleanup
  }, []);

  const handlePlayAudio = async (callId) => {
    await axios.post(`${API_BASE}/actions/call/${callId}/play_audio`, {
      audio_url: 'https://example.com/audio.mp3',
    });
    alert(`🔊 Simulated audio playback for call ${callId}`);
  };

  const handleTransfer = async (callId) => {
    const number = prompt('Enter number to transfer:');
    if (!number) return;
    await axios.post(`${API_BASE}/actions/call/${callId}/transfer`, {
      target_number: number,
    });
    fetchCalls();
  };

  const handleHangup = async (callId) => {
    await axios.post(`${API_BASE}/actions/call/${callId}/hangup`);
    fetchCalls();
  };

  const filteredCalls = calls
    .filter(call =>
      (!filterStatus || call.status === filterStatus) &&
      (!searchNumber ||
        call.from_number.includes(searchNumber) ||
        call.to_number.includes(searchNumber))
    )
    .sort((a, b) =>
      sortOrder === 'asc'
        ? new Date(a.start_time) - new Date(b.start_time)
        : new Date(b.start_time) - new Date(a.start_time)
    );

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4">📋 Call Log</h2>

      <div className="flex flex-col md:flex-row md:items-center gap-4 mb-4 flex-wrap">
        <div>
          <label className="mr-2 font-medium">Filter by status:</label>
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="border p-2 rounded"
          >
            <option value="">All</option>
            <option value="ringing">Ringing</option>
            <option value="in_progress">In Progress</option>
            <option value="completed">Completed</option>
            <option value="failed">Failed</option>
            <option value="missed">Missed</option>
            <option value="queued">Queued</option>
          </select>
        </div>

        <div>
          <label className="mr-2 font-medium">Sort by time:</label>
          <select
            value={sortOrder}
            onChange={(e) => setSortOrder(e.target.value)}
            className="border p-2 rounded"
          >
            <option value="desc">Newest First</option>
            <option value="asc">Oldest First</option>
          </select>
        </div>

        <div>
          <label className="mr-2 font-medium">Search number:</label>
          <input
            type="text"
            value={searchNumber}
            onChange={(e) => setSearchNumber(e.target.value)}
            placeholder="From or To number"
            className="border p-2 rounded w-64"
          />
        </div>
      </div>

      {loading ? (
        <p>Loading calls...</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="table-auto w-full border-collapse border border-gray-200">
            <thead className="bg-gray-100">
              <tr>
                <th className="border px-4 py-2">From</th>
                <th className="border px-4 py-2">To</th>
                <th className="border px-4 py-2">Status</th>
                <th className="border px-4 py-2">Start Time</th>
                <th className="border px-4 py-2">Duration (s)</th>
                <th className="border px-4 py-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredCalls.map((call) => (
                <tr key={call.call_id} className="text-center hover:bg-gray-50">
                  <td className="border px-4 py-2">{call.from_number}</td>
                  <td className="border px-4 py-2">{call.to_number}</td>
                  <td className="border px-4 py-2">{call.status}</td>
                  <td className="border px-4 py-2">{new Date(call.start_time).toLocaleString()}</td>
                  <td className="border px-4 py-2">{call.duration ?? '-'}</td>
                  <td className="border px-4 py-2 space-x-2">
                    <button
                      className="bg-blue-500 text-white px-2 py-1 rounded hover:bg-blue-600"
                      onClick={() => handlePlayAudio(call.call_id)}
                    >
                      ▶️ Play
                    </button>
                    <button
                      className="bg-yellow-500 text-white px-2 py-1 rounded hover:bg-yellow-600"
                      onClick={() => handleTransfer(call.call_id)}
                    >
                      🔁 Transfer
                    </button>
                    <button
                      className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                      onClick={() => handleHangup(call.call_id)}
                    >
                      🔴 Hangup
                    </button>
                  </td>
                </tr>
              ))}
              {filteredCalls.length === 0 && (
                <tr>
                  <td colSpan="6" className="text-center py-4 text-gray-500">No calls found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default CallTable;
