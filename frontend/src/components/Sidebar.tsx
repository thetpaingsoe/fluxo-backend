import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const menuItems = [
  { label: 'Dashboard', icon: '📊', path: '/' },
  { label: 'Tasks', icon: '📋', path: '/tasks' },
  { label: 'Settings', icon: '⚙️', path: '/settings' },
];

export default function Sidebar() {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <aside className="w-64 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 flex flex-col">
      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item) => (
          <button
            key={item.label}
            onClick={() => navigate(item.path)}
            className={`w-full cursor-pointer text-left px-4 py-3 rounded-lg transition-colors flex items-center gap-3 ${
              location.pathname === item.path
                ? 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white'
                : 'hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300'
            }`}
          >
            <span>{item.icon}</span>
            <span>{item.label}</span>
          </button>
        ))}
      </nav>
      <div className="p-4 border-t border-gray-200 dark:border-gray-800">
        <button
          onClick={logout}
          className="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors text-red-500"
        >
          Logout
        </button>
      </div>
    </aside>
  );
}
