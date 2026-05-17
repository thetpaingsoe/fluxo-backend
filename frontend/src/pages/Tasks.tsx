import { useEffect, useState } from 'react';
import { getTasks, deleteTask, completeTask, type Task } from '../api/tasks';

const statusColors: Record<string, string> = {
  pending: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300',
  in_progress: 'bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300',
  completed: 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300',
};

function StatusTag({ status }: { status: string }) {
  const color = statusColors[status] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${color}`}>
      {status.replace('_', ' ')}
    </span>
  );
}

export default function Tasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  async function loadTasks() {
    try {
      const data = await getTasks();
      setTasks(data);
    } catch {
      console.error('Failed to load tasks');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadTasks();
  }, []);

  async function handleComplete(id: number) {
    try {
      await completeTask(id);
      await loadTasks();
    } catch {
      console.error('Failed to complete task');
    }
  }

  async function handleDelete(id: number) {
    try {
      await deleteTask(id);
      await loadTasks();
    } catch {
      console.error('Failed to delete task');
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-800 dark:text-white">Tasks</h1>
        <button className="px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors text-sm">
          + Add Task
        </button>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-gray-200 dark:border-gray-700 text-sm text-gray-500 dark:text-gray-400">
              <th className="px-6 py-4 font-medium">Name</th>
              <th className="px-6 py-4 font-medium">Category</th>
              <th className="px-6 py-4 font-medium">Status</th>
              <th className="px-6 py-4 font-medium">Start</th>
              <th className="px-6 py-4 font-medium">End</th>
              <th className="px-6 py-4 font-medium" />
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={6} className="px-6 py-12 text-center text-gray-400">Loading...</td>
              </tr>
            ) : tasks.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-6 py-12 text-center text-gray-400">No tasks yet.</td>
              </tr>
            ) : (
              tasks.map((task) => (
                <tr key={task.id} className="border-b border-gray-100 dark:border-gray-700/50 last:border-0">
                  <td className="px-6 py-4 text-gray-800 dark:text-white font-medium">{task.name}</td>
                  <td className="px-6 py-4 text-gray-500 dark:text-gray-400">{task.category || '—'}</td>
                  <td className="px-6 py-4"><StatusTag status={task.status} /></td>
                  <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">{new Date(task.start_time).toLocaleDateString()}</td>
                  <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">{task.end_time ? new Date(task.end_time).toLocaleDateString() : '—'}</td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      {task.status !== 'completed' && (
                        <button
                          onClick={() => handleComplete(task.id)}
                          className="text-sm text-green-600 hover:text-green-700 dark:text-green-400 dark:hover:text-green-300"
                        >
                          Complete
                        </button>
                      )}
                      <button
                        onClick={() => handleDelete(task.id)}
                        className="text-sm text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300"
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
