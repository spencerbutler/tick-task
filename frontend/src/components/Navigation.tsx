import { Link, useLocation } from 'react-router-dom';

const navigation = [
  { name: 'Today', href: '/', shortcut: '1' },
  { name: 'Inbox', href: '/inbox', shortcut: '2' },
  { name: 'Contexts', href: '/contexts', shortcut: '3' },
  { name: 'Tags', href: '/tags', shortcut: '4' },
];

export function Navigation() {
  const location = useLocation();

  return (
    <nav className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
      <div className="container mx-auto px-4">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                FIN-tasks
              </h1>
            </div>
            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
              {navigation.map((item) => {
                const isActive = location.pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                      isActive
                        ? 'border-primary-500 text-gray-900 dark:text-white'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
                    }`}
                  >
                    {item.name}
                  </Link>
                );
              })}
            </div>
          </div>

          {/* Plus button moved to TodayView */}
        </div>
      </div>
    </nav>
  );
}
