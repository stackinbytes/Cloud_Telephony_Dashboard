import React, { useState } from 'react';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000'; // Connecting to the backend

const CallForm = ({ onSuccess }) => {
  const [form, setForm] = useState({
    from_number: '',
    to_number: '',
    status: 'ringing',
    direction: 'outbound',
    recording_url: '',
    notes: '',
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = {
        ...form,
        recording_url: form.recording_url || null,
        notes: form.notes || null,
      };
      await axios.post(`${API_BASE}/calls`, payload);
      setForm({
        from_number: '',
        to_number: '',
        status: 'ringing',
        direction: 'outbound',
        recording_url: '',
        notes: '',
      });
      onSuccess(); // Refresh call list
    } catch (err) {
      console.error('Call initiation error:', err);
      const detail = err.response?.data?.detail || 'Unknown error occurred';
      alert(`Call initiation failed: ${detail}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-4 rounded-lg shadow space-y-4">
      <h2 className="text-xl font-semibold">📞 Initiate New Call</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <input
          type="text"
          name="from_number"
          placeholder="From Number"
          value={form.from_number}
          onChange={handleChange}
          className="border p-2 rounded"
          required
        />
        <input
          type="text"
          name="to_number"
          placeholder="To Number"
          value={form.to_number}
          onChange={handleChange}
          className="border p-2 rounded"
          required
        />

        <select name="status" value={form.status} onChange={handleChange} className="border p-2 rounded">
          <option value="ringing">Ringing</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
          <option value="failed">Failed</option>
          <option value="missed">Missed</option>
          <option value="queued">Queued</option>
        </select>

        <select name="direction" value={form.direction} onChange={handleChange} className="border p-2 rounded">
          <option value="inbound">Inbound</option>
          <option value="outbound">Outbound</option>
        </select>

        <input
          type="url"
          name="recording_url"
          placeholder="Recording URL (optional)"
          value={form.recording_url}
          onChange={handleChange}
          className="border p-2 rounded col-span-1 md:col-span-2"
        />

        <textarea
          name="notes"
          placeholder="Notes (optional)"
          value={form.notes}
          onChange={handleChange}
          className="border p-2 rounded col-span-1 md:col-span-2"
          rows={3}
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? 'Submitting...' : 'Initiate Call'}
      </button>
    </form>
  );
};

export default CallForm;
