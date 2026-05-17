import Sidebar from '../components/Sidebar';
import ThemeToggle from '../components/ThemeToggle';

export default function Dashboard() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-950">
      <header className="h-14 flex items-center justify-between bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 shrink-0 text-gray-700 dark:text-gray-200">
        <div className="flex items-center gap-3 pl-8">
          <span className="text-lg font-bold text-gray-800 dark:text-white">Fluxo</span>
        </div>
        <div className="pr-6">
          <ThemeToggle />
        </div>
      </header>
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 p-8">
          <h1 className="text-3xl font-bold text-gray-800 dark:text-white">Dashboard</h1>
          <p className="text-gray-500 dark:text-gray-400 mt-2">Welcome to Fluxo. Select a menu item to get started.</p>
          <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
            {['Total Tasks', 'Completed', 'Pending'].map((label) => (
              <div key={label} className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
                <p className="text-sm text-gray-500 dark:text-gray-400">{label}</p>
                <p className="text-3xl font-bold text-gray-800 dark:text-white mt-2">0</p>
              </div>
            ))}
          </div>
        </main>
      </div>
    </div>
  );
}
