import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { scheduleAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function Schedule() {
  const [schedules, setSchedules] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const { logout } = useAuth();

  useEffect(() => {
    loadSchedule();
  }, []);

  const loadSchedule = async () => {
    try {
      const response = await scheduleAPI.getWeek();
      setSchedules(response.data);
    } catch (error) {
      console.error('Error loading schedule:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleClearSchedule = async () => {
    if (window.confirm('Clear all scheduled items?')) {
      try {
        await scheduleAPI.clear();
        setSchedules([]);
      } catch (error) {
        alert('Failed to clear schedule');
      }
    }
  };

  if (loading) return <div className="p-8">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">Weekly Schedule</h1>
          </div>
          <div className="flex gap-4">
            <button
              onClick={() => navigate('/dashboard')}
              className="text-blue-500 hover:text-blue-600"
            >
              ← Back to Dashboard
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-gray-800">Your Schedule</h2>
            <button
              onClick={handleClearSchedule}
              className="text-red-500 hover:text-red-600 text-sm"
            >
              Clear Schedule
            </button>
          </div>

          {schedules.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-600 mb-4">No scheduled items yet.</p>
              <button
                onClick={() => navigate('/dashboard')}
                className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg"
              >
                Go Add Tasks & Generate Schedule
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {schedules.map(schedule => (
                <div key={schedule.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-lg transition">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold text-gray-800">{schedule.notes}</h3>
                      <p className="text-sm text-gray-600 mt-1">
                        📅 {new Date(schedule.scheduled_date).toLocaleDateString()} at {new Date(schedule.scheduled_date).toLocaleTimeString()}
                      </p>
                      <p className="text-sm text-gray-600">⏱️ Duration: {schedule.duration_hours} hours</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}