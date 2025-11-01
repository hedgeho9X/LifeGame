import { create } from 'zustand';
import { User, Goal, CharacterState } from '../types';

interface GameState {
  // User state
  user: User | null;
  stats: Record<string, number>;
  
  // Current goal and tasks
  currentGoal: Goal | null;
  
  // UI state
  characterState: CharacterState;
  isLoading: boolean;
  showRewards: boolean;
  recentRewards: Record<string, number>;
  
  // Actions
  setUser: (user: User) => void;
  setStats: (stats: Record<string, number>) => void;
  setCurrentGoal: (goal: Goal | null) => void;
  setCharacterState: (state: CharacterState) => void;
  setLoading: (loading: boolean) => void;
  updateStats: (newStats: Record<string, number>) => void;
  showRewardAnimation: (rewards: Record<string, number>) => void;
  hideRewardAnimation: () => void;
  reset: () => void;
}

export const useGameStore = create<GameState>((set) => ({
  // Initial state
  user: null,
  stats: {},
  currentGoal: null,
  characterState: 'idle',
  isLoading: false,
  showRewards: false,
  recentRewards: {},

  // Actions
  setUser: (user) => set({ user }),
  
  setStats: (stats) => set({ stats }),
  
  setCurrentGoal: (goal) => set({ currentGoal: goal }),
  
  setCharacterState: (state) => set({ characterState: state }),
  
  setLoading: (loading) => set({ isLoading: loading }),
  
  updateStats: (newStats) => set({ stats: newStats }),
  
  showRewardAnimation: (rewards) => 
    set({ showRewards: true, recentRewards: rewards }),
  
  hideRewardAnimation: () => 
    set({ showRewards: false, recentRewards: {} }),
  
  reset: () => 
    set({
      user: null,
      stats: {},
      currentGoal: null,
      characterState: 'idle',
      isLoading: false,
      showRewards: false,
      recentRewards: {},
    }),
}));

