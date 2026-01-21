import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  Task,
  TaskCreate,
  TaskUpdate,
  TaskList,
  TaskQuery,
  ApiError
} from '@/types/api';

// API base URL
const API_BASE = '/api/v1';

// Query keys
export const taskKeys = {
  all: ['tasks'] as const,
  lists: () => [...taskKeys.all, 'list'] as const,
  list: (filters: TaskQuery) => [...taskKeys.lists(), filters] as const,
  details: () => [...taskKeys.all, 'detail'] as const,
  detail: (id: string) => [...taskKeys.details(), id] as const,
};

// API functions
const api = {
  async getTasks(query: TaskQuery = {}): Promise<TaskList> {
    const params = new URLSearchParams();

    Object.entries(query).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params.append(key, String(value));
      }
    });

    const url = `${API_BASE}/tasks${params.toString() ? `?${params.toString()}` : ''}`;
    const response = await fetch(url);

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.error.message);
    }

    return response.json();
  },

  async getTask(id: string): Promise<Task> {
    const response = await fetch(`${API_BASE}/tasks/${id}`);

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.error.message);
    }

    return response.json();
  },

  async createTask(task: TaskCreate): Promise<Task> {
    const response = await fetch(`${API_BASE}/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(task),
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.error.message);
    }

    return response.json();
  },

  async updateTask(id: string, task: TaskUpdate): Promise<Task> {
    const response = await fetch(`${API_BASE}/tasks/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(task),
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.error.message);
    }

    return response.json();
  },

  async deleteTask(id: string): Promise<Task> {
    const response = await fetch(`${API_BASE}/tasks/${id}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new Error(error.error.message);
    }

    return response.json();
  },
};

// React Query hooks
export function useTasks(query: TaskQuery = {}) {
  return useQuery({
    queryKey: taskKeys.list(query),
    queryFn: () => api.getTasks(query),
    staleTime: 30000, // 30 seconds
    gcTime: 300000, // 5 minutes
  });
}

export function useTask(id: string) {
  return useQuery({
    queryKey: taskKeys.detail(id),
    queryFn: () => api.getTask(id),
    enabled: !!id,
    staleTime: 30000,
    gcTime: 300000,
  });
}

export function useCreateTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: api.createTask,
    onSuccess: (newTask) => {
      // Invalidate and refetch task lists
      queryClient.invalidateQueries({ queryKey: taskKeys.lists() });

      // Add the new task to the cache
      queryClient.setQueryData(taskKeys.detail(newTask.id), newTask);
    },
  });
}

export function useUpdateTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, task }: { id: string; task: TaskUpdate }) =>
      api.updateTask(id, task),
    onSuccess: (updatedTask) => {
      // Update the task in cache
      queryClient.setQueryData(taskKeys.detail(updatedTask.id), updatedTask);

      // Invalidate task lists to refetch
      queryClient.invalidateQueries({ queryKey: taskKeys.lists() });
    },
  });
}

export function useDeleteTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: api.deleteTask,
    onSuccess: (deletedTask) => {
      // Remove from cache
      queryClient.removeQueries({ queryKey: taskKeys.detail(deletedTask.id) });

      // Invalidate task lists
      queryClient.invalidateQueries({ queryKey: taskKeys.lists() });
    },
  });
}
