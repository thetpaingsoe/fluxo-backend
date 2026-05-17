import { useAuth } from '../contexts/AuthContext';

const menuItems = [
  { label: 'Dashboard', icon: '📊' },
  { label: 'Tasks', icon: '📋' },
  { label: 'Settings', icon: '⚙️' },
];

export default function Sidebar() {
  const { logout } = useAuth();

  return (
    <aside className="w-64 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 flex flex-col">
      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item) => (
          <button
            key={item.label}
            className="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors flex items-center gap-3 text-gray-700 dark:text-gray-300"
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
