import Sidebar from '../components/Sidebar';

export default function Dashboard() {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 bg-gray-50 p-8">
        <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>
        <p className="text-gray-500 mt-2">Welcome to Fluxo. Select a menu item to get started.</p>
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          {['Total Tasks', 'Completed', 'Pending'].map((label) => (
            <div key={label} className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
              <p className="text-sm text-gray-500">{label}</p>
              <p className="text-3xl font-bold text-gray-800 mt-2">0</p>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
