import apiClient from './client';

export interface Task {
  id: number;
  user_id: number;
  name: string;
  category: string | null;
  status: string;
  start_time: string;
  end_time: string | null;
  completed_at: string | null;
  created_at: string;
}

export interface TaskCreate {
  user_id: number;
  name: string;
  category?: string;
  start_time: string;
  end_time?: string;
}

export interface TaskUpdate {
  name?: string;
  category?: string;
  status?: string;
  start_time?: string;
  end_time?: string;
}

export async function getTasks(): Promise<Task[]> {
  const resp = await apiClient.get<Task[]>('/tasks/');
  return resp.data;
}

export async function getTask(id: number): Promise<Task> {
  const resp = await apiClient.get<Task>(`/tasks/${id}`);
  return resp.data;
}

export async function createTask(task: TaskCreate): Promise<Task> {
  const resp = await apiClient.post<Task>('/tasks/', task);
  return resp.data;
}

export async function updateTask(id: number, task: TaskUpdate): Promise<Task> {
  const resp = await apiClient.put<Task>(`/tasks/${id}`, task);
  return resp.data;
}

export async function deleteTask(id: number): Promise<Task> {
  const resp = await apiClient.delete<Task>(`/tasks/${id}`);
  return resp.data;
}

export async function completeTask(id: number): Promise<Task> {
  const resp = await apiClient.post<Task>(`/tasks/${id}/complete`);
  return resp.data;
}
