export default function Dashboard() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-800 dark:text-white">Dashboard</h1>
      <p className="text-gray-500 dark:text-gray-400 mt-2">Welcome to Fluxo. Select a menu item to get started.</p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {['Total Tasks', 'Completed', 'Pending'].map((label) => (
          <div key={label} className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
            <p className="text-sm text-gray-500 dark:text-gray-400">{label}</p>
            <p className="text-3xl font-bold text-gray-800 dark:text-white mt-2">0</p>
          </div>
        ))}
      </div>
    </div>
  );
}
