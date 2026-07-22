import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { subjectAPI, taskAPI } from '../services/api';
import AddSubjectModal from '../components/AddSubjectModal';

export default function Dashboard() {
  const [subjects, setSubjects] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showNewSubject, setShowNewSubject] = useState(false);
  
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [subjectsRes, tasksRes] = await Promise.all([
        subjectAPI.getAll(),
        taskAPI.getAll(),
      ]);
      setSubjects(subjectsRes.data);
      setTasks(tasksRes.data);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleSubjectAdded = (newSubject) => {
    setSubjects([...subjects, newSubject]);
  };

  const completedTasks = tasks.filter(t => t.status === 'completed').length;
  const pendingTasks = tasks.filter(t => t.status === 'pending').length;

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center">
          <p className="text-gray-600 text-lg">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-800">📚 Study Planner</h1>
          <div className="flex items-center gap-4">
            <span className="text-gray-600">{user?.full_name}</span>
            <button
              onClick={handleLogout}
              className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition">
            <h3 className="text-gray-600 text-sm font-semibold mb-2">Total Subjects</h3>
            <p className="text-3xl font-bold text-blue-500">{subjects.length}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition">
            <h3 className="text-gray-600 text-sm font-semibold mb-2">Total Tasks</h3>
            <p className="text-3xl font-bold text-purple-500">{tasks.length}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition">
            <h3 className="text-gray-600 text-sm font-semibold mb-2">Pending</h3>
            <p className="text-3xl font-bold text-yellow-500">{pendingTasks}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition">
            <h3 className="text-gray-600 text-sm font-semibold mb-2">Completed</h3>
            <p className="text-3xl font-bold text-green-500">{completedTasks}</p>
          </div>
        </div>

        {/* Navigation Buttons */}
        <div className="mb-8 flex gap-4">
          <button
            onClick={() => setShowNewSubject(true)}
            className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg transition font-semibold"
          >
            + Add Subject
          </button>
          <button
            onClick={() => navigate('/schedule')}
            className="bg-purple-500 hover:bg-purple-600 text-white px-6 py-2 rounded-lg transition font-semibold"
          >
            📅 View Schedule
          </button>
        </div>

        {/* Subjects Section */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-bold text-gray-800 mb-6">Your Subjects</h2>

          {subjects.length === 0 ? (
            <div className="text-center py-12 bg-gray-50 rounded-lg">
              <p className="text-gray-600 text-lg mb-4">No subjects yet. Create one to get started!</p>
              <button
                onClick={() => setShowNewSubject(true)}
                className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg"
              >
                Create Your First Subject
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {subjects.map(subject => (
                <div
                  key={subject.id}
                  onClick={() => navigate(`/subject/${subject.id}`)}
                  className="border border-gray-200 rounded-lg p-4 hover:shadow-lg hover:border-blue-300 transition cursor-pointer"
                >
                  <h3 className="font-semibold text-gray-800 text-lg mb-2">{subject.name}</h3>
                  <p className="text-sm text-gray-600 mb-3">{subject.description || 'No description'}</p>
                  {subject.exam_date && (
                    <p className="text-xs text-gray-500 bg-gray-50 px-2 py-1 rounded w-fit">
                      📅 Exam: {new Date(subject.exam_date).toLocaleDateString()}
                    </p>
                  )}
                  <p className="text-xs text-blue-500 mt-3 font-semibold">Click to manage tasks →</p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent Tasks Section */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-6">Recent Tasks</h2>

          {tasks.length === 0 ? (
            <p className="text-gray-600 text-center py-8">No tasks yet. Add subjects and create tasks to get started!</p>
          ) : (
            <div className="space-y-3">
              {tasks.slice(0, 5).map(task => (
                <div key={task.id} className="flex items-center justify-between border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition">
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-800">{task.title}</h3>
                    <p className="text-sm text-gray-600 mt-1">
                      {task.estimated_hours}h | {task.difficulty} | {task.status}
                    </p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                    task.status === 'completed' 
                      ? 'bg-green-100 text-green-700' 
                      : 'bg-yellow-100 text-yellow-700'
                  }`}>
                    {task.status}
                  </span>
                </div>
              ))}
              {tasks.length > 5 && (
                <p className="text-sm text-gray-500 text-center mt-4">
                  +{tasks.length - 5} more tasks in your subjects
                </p>
              )}
            </div>
          )}
        </div>
      </main>

      <AddSubjectModal
        isOpen={showNewSubject}
        onClose={() => setShowNewSubject(false)}
        onSubjectAdded={handleSubjectAdded}
      />
    </div>
  );
}