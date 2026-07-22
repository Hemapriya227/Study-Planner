import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { subjectAPI, taskAPI, scheduleAPI } from '../services/api';
import AddTaskModal from '../components/AddTaskModal';
import TaskCard from '../components/TaskCard';

export default function SubjectDetail() {
  const { subjectId } = useParams();
  const navigate = useNavigate();
  const [subject, setSubject] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddTask, setShowAddTask] = useState(false);
  const [generatingSchedule, setGeneratingSchedule] = useState(false);

  useEffect(() => {
    loadData();
  }, [subjectId]);

  const loadData = async () => {
    try {
      const [subjectRes, tasksRes] = await Promise.all([
        subjectAPI.getOne(subjectId),
        taskAPI.getAll(subjectId),
      ]);
      setSubject(subjectRes.data);
      setTasks(tasksRes.data);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTaskAdded = (newTask) => {
    setTasks([...tasks, newTask]);
  };

  const handleTaskUpdated = (updatedTask) => {
    setTasks(tasks.map(t => t.id === updatedTask.id ? updatedTask : t));
  };

  const handleTaskDeleted = (taskId) => {
    setTasks(tasks.filter(t => t.id !== taskId));
  };

  const handleGenerateSchedule = async () => {
    setGeneratingSchedule(true);
    try {
      const response = await scheduleAPI.generate();
      alert(`Schedule generated! ${response.data.schedules_created} tasks scheduled.`);
    } catch (error) {
      alert('Failed to generate schedule');
    } finally {
      setGeneratingSchedule(false);
    }
  };

  const handleDeleteSubject = async () => {
    if (window.confirm('Delete this subject and all its tasks?')) {
      try {
        await subjectAPI.delete(subjectId);
        navigate('/dashboard');
      } catch (error) {
        alert('Failed to delete subject');
      }
    }
  };

  if (loading) return <div className="p-8">Loading...</div>;
  if (!subject) return <div className="p-8">Subject not found</div>;

  const pendingTasks = tasks.filter(t => t.status === 'pending').length;
  const completedTasks = tasks.filter(t => t.status === 'completed').length;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <button
            onClick={() => navigate('/dashboard')}
            className="text-blue-500 hover:text-blue-600 mb-4"
          >
            ← Back to Dashboard
          </button>
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold text-gray-800">{subject.name}</h1>
              {subject.description && (
                <p className="text-gray-600 mt-2">{subject.description}</p>
              )}
              {subject.exam_date && (
                <p className="text-sm text-gray-500 mt-2">
                  📅 Exam: {new Date(subject.exam_date).toLocaleDateString()}
                </p>
              )}
            </div>
            <button
              onClick={handleDeleteSubject}
              className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition"
            >
              Delete Subject
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-gray-600 text-sm font-semibold mb-2">Total Tasks</h3>
            <p className="text-3xl font-bold text-blue-500">{tasks.length}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-gray-600 text-sm font-semibold mb-2">Pending</h3>
            <p className="text-3xl font-bold text-yellow-500">{pendingTasks}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-gray-600 text-sm font-semibold mb-2">Completed</h3>
            <p className="text-3xl font-bold text-green-500">{completedTasks}</p>
          </div>
        </div>

        {/* Actions */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <div className="flex gap-4">
            <button
              onClick={() => setShowAddTask(true)}
              className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition"
            >
              + Add Task
            </button>
            <button
              onClick={handleGenerateSchedule}
              disabled={generatingSchedule || tasks.length === 0}
              className="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              {generatingSchedule ? 'Generating...' : '🤖 Generate Schedule'}
            </button>
          </div>
        </div>

        {/* Tasks List */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-6">Tasks</h2>

          {tasks.length === 0 ? (
            <p className="text-gray-600 text-center py-8">No tasks yet. Add one to get started!</p>
          ) : (
            <div className="space-y-4">
              {tasks.map(task => (
                <TaskCard
                  key={task.id}
                  task={task}
                  onTaskUpdated={handleTaskUpdated}
                  onTaskDeleted={handleTaskDeleted}
                />
              ))}
            </div>
          )}
        </div>
      </main>

      <AddTaskModal
        isOpen={showAddTask}
        onClose={() => setShowAddTask(false)}
        subjectId={parseInt(subjectId)}
        onTaskAdded={handleTaskAdded}
      />
    </div>
  );
}