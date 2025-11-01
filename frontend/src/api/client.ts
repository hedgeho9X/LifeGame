import axios from 'axios';
import { User, Goal, TaskCompleteResponse, UserStats, ConversationMessage, ConversationResponse, TherapyTicket, TherapyChatRequest, TherapyChatResponse } from '../types';

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

  // Conversation APIs
  sendMessage: async (goalId: number, userMessage: string): Promise<ConversationResponse> => {
    const response = await client.post('/conversations', {
      goal_id: goalId,
      user_message: userMessage,
    });
    return response.data;
  },

  getConversations: async (goalId: number): Promise<ConversationMessage[]> => {
    const response = await client.get(`/goals/${goalId}/conversations`);
    return response.data;
  },

  applyTaskUpdates: async (goalId: number): Promise<{ success: boolean; summary: string; tasks: any[] }> => {
    const response = await client.post(`/goals/${goalId}/apply-updates`);
    return response.data;
  },

  // Therapy Ticket APIs
  getTherapyTickets: async (userId: number): Promise<TherapyTicket[]> => {
    const response = await client.get(`/users/${userId}/therapy-tickets`);
    return response.data;
  },

  therapyChat: async (request: TherapyChatRequest): Promise<TherapyChatResponse> => {
    const response = await client.post('/therapy/chat', request);
    return response.data;
  },

  // Reset Stats API
  resetStats: async (userId: number): Promise<{ success: boolean; message: string }> => {
    const response = await client.post(`/users/${userId}/reset-stats`);
    return response.data;
  },
};

