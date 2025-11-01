export interface User {
  id: number;
  name: string;
  background?: string;
  created_at: string;
}

export interface Task {
  id: number;
  goal_id: number;
  title: string;
  description: string;
  estimated_time: string;
  order: number;
  completed: boolean;
  completed_at?: string;
  created_at: string;
}

export interface Goal {
  id: number;
  user_id: number;
  goal_text: string;
  story: string;
  tasks: Task[];
  stats_data: Record<string, number>;
  created_at: string;
  completed: boolean;
}

export interface TaskCompleteResponse {
  task_id: number;
  completed: boolean;
  rewards: Record<string, number>;
  updated_stats: Record<string, number>;
  character_state: 'celebrating' | 'idle' | 'thinking';
}

export interface UserStats {
  id: number;
  user_id: number;
  stats_data: Record<string, number>;
  updated_at: string;
}

export type CharacterState = 'idle' | 'thinking' | 'celebrating';

