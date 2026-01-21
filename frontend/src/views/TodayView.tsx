import { useTasks, useUpdateTask } from '../hooks/useTasks';

interface TodayViewProps {
  onAddTask: () => void;
}

export function TodayView({ onAddTask }: TodayViewProps) {
  // Create date range for today
  const today = new Date();
  const startOfDay = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  const endOfDay = new Date(today.getFullYear(), today.getMonth(), today.getDate(), 23, 59, 59, 999);

  const { data: tasksData, isLoading, error } = useTasks({
    status: 'todo,doing,blocked',
    due_before: endOfDay.toISOString(),
    due_after: startOfDay.toISOString(),
    sort: 'due_at',
    order: 'asc',
  });

  const updateTaskMutation = useUpdateTask();

  const handleTaskStatusChange = (taskId: string, currentStatus: string) => {
    // Toggle between 'todo' and 'done'
    const newStatus = currentStatus === 'done' ? 'todo' : 'done';
    updateTaskMutation.mutate({ id: taskId, task: { status: newStatus } });
  };

  if (isLoading) {
    return (
      <div className="text-center py-12">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mx-auto mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-gray-200 rounded w-3/4 mx-auto"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2 mx-auto"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 mb-4">
          <svg className="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
        </div>
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
          Error Loading Tasks
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          {error instanceof Error ? error.message : 'An unexpected error occurred'}
        </p>
      </div>
    );
  }

  const tasks = tasksData?.tasks || [];

  return (
    <div>
      <div className="mb-8 flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Today</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Tasks due today and overdue items
          </p>
        </div>
        <button
          type="button"
          className="btn btn-primary"
          onClick={onAddTask}
          title="Add New Task"
        >
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          <span className="ml-2">Add Task</span>
        </button>
      </div>

      {tasks.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-success-600 mb-4">
            <svg className="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            All caught up!
          </h2>
          <p className="text-gray-600 dark:text-gray-400">
            No tasks due today. Great job staying on top of things!
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {tasks.map((task) => (
            <div
              key={task.id}
              className="card hover:shadow-md transition-shadow cursor-pointer"
            >
              <div className="flex items-start space-x-3">
                <input
                  type="checkbox"
                  className="mt-1 h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded cursor-pointer"
                  checked={task.status === 'done'}
                  onChange={() => handleTaskStatusChange(task.id, task.status)}
                  disabled={updateTaskMutation.isPending}
                />
                <div className="flex-1 min-w-0">
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white truncate">
                    {task.title}
                  </h3>
                  {task.description && (
                    <p className="text-gray-600 dark:text-gray-400 text-sm mt-1 line-clamp-2">
                      {task.description}
                    </p>
                  )}
                  <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500 dark:text-gray-400">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      task.priority === 'urgent' ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200' :
                      task.priority === 'high' ? 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200' :
                      task.priority === 'medium' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200' :
                      'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
                    }`}>
                      {task.priority}
                    </span>
                    <span>{task.context}</span>
                    {task.tags.length > 0 && (
                      <div className="flex space-x-1">
                        {task.tags.slice(0, 3).map((tag) => (
                          <span key={tag} className="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded text-xs">
                            #{tag}
                          </span>
                        ))}
                        {task.tags.length > 3 && (
                          <span className="text-xs">+{task.tags.length - 3} more</span>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
