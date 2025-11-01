import React, { useState, useEffect } from 'react';
import { useGameStore } from './store/gameStore';
import { api } from './api/client';
import { Character } from './components/Character';
import { GoalInput } from './components/GoalInput';
import { StoryDisplay } from './components/StoryDisplay';
import { TaskList } from './components/TaskList';
import { StatsDisplay } from './components/StatsDisplay';
import { RewardAnimation } from './components/RewardAnimation';

function App() {
  const {
    user,
    stats,
    currentGoal,
    characterState,
    isLoading,
    showRewards,
    recentRewards,
    setUser,
    setStats,
    setCurrentGoal,
    setCharacterState,
    setLoading,
    updateStats,
    showRewardAnimation,
    hideRewardAnimation,
  } = useGameStore();

  const [error, setError] = useState<string | null>(null);
  const [initialized, setInitialized] = useState(false);

  // 初始化用户
  useEffect(() => {
    const initUser = async () => {
      try {
        // 检查是否有保存的用户 ID
        const savedUserId = localStorage.getItem('userId');
        
        if (savedUserId) {
          const userData = await api.getUser(parseInt(savedUserId));
          const userStats = await api.getUserStats(parseInt(savedUserId));
          setUser(userData);
          setStats(userStats.stats_data);
        } else {
          // 创建新用户
          const newUser = await api.createUser('玩家');
          localStorage.setItem('userId', newUser.id.toString());
          setUser(newUser);
          setStats({ '等级': 1, '经验值': 0 });
        }
        setInitialized(true);
      } catch (err) {
        console.error('Failed to initialize user:', err);
        setError('初始化失败，请刷新页面重试');
      }
    };

    initUser();
  }, [setUser, setStats]);

  // 提交目标
  const handleGoalSubmit = async (goalText: string, background: string) => {
    if (!user) return;

    setLoading(true);
    setCharacterState('thinking');
    setError(null);

    try {
      const goal = await api.createGoal(user.id, goalText, background);
      setCurrentGoal(goal);
      setStats(goal.stats_data);
      setCharacterState('idle');
    } catch (err) {
      console.error('Failed to create goal:', err);
      setError('创建目标失败，请重试');
      setCharacterState('idle');
    } finally {
      setLoading(false);
    }
  };

  // 完成任务
  const handleTaskComplete = async (taskId: number) => {
    setLoading(true);
    setError(null);

    try {
      const response = await api.completeTask(taskId);
      
      // 更新任务状态
      if (currentGoal) {
        const updatedTasks = currentGoal.tasks.map(task =>
          task.id === taskId
            ? { ...task, completed: true, completed_at: new Date().toISOString() }
            : task
        );
        setCurrentGoal({
          ...currentGoal,
          tasks: updatedTasks,
        });
      }

      // 更新数值
      updateStats(response.updated_stats);
      
      // 显示奖励动画
      setCharacterState('celebrating');
      showRewardAnimation(response.rewards);
      
      // 2.5 秒后恢复正常状态
      setTimeout(() => {
        setCharacterState('idle');
      }, 2500);
      
    } catch (err) {
      console.error('Failed to complete task:', err);
      setError('完成任务失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  // 重新开始
  const handleReset = () => {
    setCurrentGoal(null);
    setCharacterState('idle');
  };

  if (!initialized) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-white font-mono text-lg pixel-animate">
          加载中...
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black py-8 px-4">
      {/* 错误提示 */}
      {error && (
        <div className="fixed top-4 left-1/2 transform -translate-x-1/2 z-50">
          <div className="pixel-border bg-black p-4">
            <p className="text-white font-mono text-sm">❌ {error}</p>
            <button
              onClick={() => setError(null)}
              className="mt-2 text-pixel-light-gray font-mono text-xs underline"
            >
              关闭
            </button>
          </div>
        </div>
      )}

      {/* 数值显示 */}
      {Object.keys(stats).length > 0 && <StatsDisplay stats={stats} />}

      {/* 奖励动画 */}
      {showRewards && (
        <RewardAnimation
          rewards={recentRewards}
          onComplete={hideRewardAnimation}
        />
      )}

      <div className="container mx-auto max-w-6xl">
        {/* 标题 */}
        <div className="text-center mb-8">
          <h1 className="text-white font-mono text-3xl mb-2 pixel-text-shadow">
            LIFE GAME
          </h1>
          <p className="text-pixel-light-gray font-mono text-sm">
            生活游戏化人生管理系统
          </p>
          <div className="mt-2 text-pixel-gray font-mono text-xs">
            ═══════════════════════════════
          </div>
        </div>

        {/* 角色显示 */}
        <div className="mb-8">
          <Character state={characterState} />
        </div>

        {/* 主内容区域 */}
        <div className="space-y-6">
          {!currentGoal ? (
            /* 目标输入 */
            <GoalInput onSubmit={handleGoalSubmit} isLoading={isLoading} />
          ) : (
            /* 显示故事和任务 */
            <>
              {/* 重新开始按钮 */}
              <div className="text-center">
                <button
                  onClick={handleReset}
                  className="text-pixel-light-gray font-mono text-xs underline hover:text-white"
                  disabled={isLoading}
                >
                  ← 重新开始
                </button>
              </div>

              {/* 故事显示 */}
              <StoryDisplay
                story={currentGoal.story}
                goalText={currentGoal.goal_text}
              />

              {/* 任务列表 */}
              <TaskList
                tasks={currentGoal.tasks}
                onTaskComplete={handleTaskComplete}
                isLoading={isLoading}
              />

              {/* 完成提示 */}
              {currentGoal.tasks.every(t => t.completed) && (
                <div className="text-center">
                  <div className="pixel-border bg-black p-6 inline-block">
                    <p className="text-white font-mono text-xl mb-4">
                      ★★★ 恭喜完成所有任务！★★★
                    </p>
                    <button
                      onClick={handleReset}
                      className="bg-white text-black font-mono text-sm py-2 px-6 pixel-border-thin hover:bg-pixel-light-gray"
                    >
                      开始新的冒险
                    </button>
                  </div>
                </div>
              )}
            </>
          )}
        </div>

        {/* 页脚 */}
        <div className="mt-12 text-center">
          <p className="text-pixel-gray font-mono text-xs">
            Powered by AI × Gamification
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;

