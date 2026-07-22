import { taskAPI } from '../services/api';

export default function TaskCard({ task, onTaskUpdated, onTaskDeleted }) {
  const markComplete = async () => {
    try {
      await taskAPI.markComplete(task.id);
      onTaskUpdated({ ...task, status: 'completed' });
    } catch (error) {
      console.error('Error marking task complete:', error);
    }
  };

  const deleteTask = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await taskAPI.delete(task.id);
        onTaskDeleted(task.id);
      } catch (error) {
        console.error('Error deleting task:', error);
      }
    }
  };

  const isCompleted = task.status === 'completed';
  
  const difficultyColor = {
    'Easy': 'bg-green-100 text-green-700',
    'Medium': 'bg-yellow-100 text-yellow-700',
    'Hard': 'bg-red-100 text-red-700'
  };

  return (
    <div className={`border-l-4 ${isCompleted ? 'border-l-green-500 bg-green-50' : 'border-l-blue-500 bg-white'} rounded-lg p-4 shadow-sm hover:shadow-md transition`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h3 className={`font-semibold text-lg ${isCompleted ? 'line-through text-gray-600' : 'text-gray-800'}`}>
              {task.title}
            </h3>
            <span className={`px-2 py-1 rounded text-xs font-semibold ${difficultyColor[task.difficulty]}`}>
              {task.difficulty}
            </span>
          </div>

          {task.description && (
            <p className="text-gray-600 text-sm mb-2">{task.description}</p>
          )}

          <div className="flex gap-4 text-xs text-gray-500 mb-3">
            <span>⏱️ {task.estimated_hours}h</span>
            {task.deadline && (
              <span>📅 {new Date(task.deadline).toLocaleDateString()}</span>
            )}
          </div>

          <div className="flex gap-2">
            {!isCompleted && (
              <button
                onClick={markComplete}
                className="text-xs bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded transition"
              >
                ✓ Mark Complete
              </button>
            )}
            <button
              onClick={deleteTask}
              className="text-xs bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded transition"
            >
              🗑️ Delete
            </button>
          </div>
        </div>

        {isCompleted && (
          <span className="text-2xl">✅</span>
        )}
      </div>
    </div>
  );
}