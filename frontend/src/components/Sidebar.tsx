import { useAuth } from '../contexts/AuthContext';

const menuItems = [
  { label: 'Dashboard', icon: '📊' },
  { label: 'Tasks', icon: '📋' },
  { label: 'Settings', icon: '⚙️' },
];

export default function Sidebar() {
  const { logout } = useAuth();

  return (
    <aside className="w-64 bg-gray-900 text-white flex flex-col min-h-screen">
      <div className="p-6 text-xl font-bold border-b border-gray-700">
        Fluxo
      </div>
      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item) => (
          <button
            key={item.label}
            className="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-700 transition-colors flex items-center gap-3"
          >
            <span>{item.icon}</span>
            <span>{item.label}</span>
          </button>
        ))}
      </nav>
      <div className="p-4 border-t border-gray-700">
        <button
          onClick={logout}
          className="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-700 transition-colors text-red-400"
        >
          Logout
        </button>
      </div>
    </aside>
  );
}
