import axios from 'axios';
import { User, Goal, TaskCompleteResponse, UserStats } from '../types';

const API_BASE_URL = '/api';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // User APIs
  createUser: async (name: string, background?: string): Promise<User> => {
    const response = await client.post('/users', { name, background });
    return response.data;
  },

  getUser: async (userId: number): Promise<User> => {
    const response = await client.get(`/users/${userId}`);
    return response.data;
  },

  getUserStats: async (userId: number): Promise<UserStats> => {
    const response = await client.get(`/users/${userId}/stats`);
    return response.data;
  },

  // Goal APIs
  createGoal: async (
    userId: number,
    goalText: string,
    userBackground?: string
  ): Promise<Goal> => {
    const response = await client.post('/goals', {
      user_id: userId,
      goal_text: goalText,
      user_background: userBackground,
    });
    return response.data;
  },

  getGoal: async (goalId: number): Promise<Goal> => {
    const response = await client.get(`/goals/${goalId}`);
    return response.data;
  },

  getUserGoals: async (userId: number): Promise<Goal[]> => {
    const response = await client.get(`/users/${userId}/goals`);
    return response.data;
  },

  // Task APIs
  completeTask: async (taskId: number): Promise<TaskCompleteResponse> => {
    const response = await client.post(`/tasks/${taskId}/complete`);
    return response.data;
  },
};

