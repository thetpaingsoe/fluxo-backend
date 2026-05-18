import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import ThemeToggle from './ThemeToggle';

export default function PageLayout() {
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
          <Outlet />
        </main>
      </div>
    </div>
  );
}
