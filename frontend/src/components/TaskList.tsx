import React from 'react';
import { Task } from '../types';

interface TaskListProps {
  tasks: Task[];
  onTaskComplete: (taskId: number) => void;
  isLoading: boolean;
}

export const TaskList: React.FC<TaskListProps> = ({ 
  tasks, 
  onTaskComplete, 
  isLoading 
}) => {
  if (tasks.length === 0) {
    return null;
  }

  return (
    <div className="w-full max-w-2xl mx-auto p-4">
      <div className="pixel-border bg-black p-6">
        <h2 className="text-white font-mono text-lg mb-4 text-center">
          ▼ 任务清单 ▼
        </h2>
        
        <div className="space-y-3">
          {tasks.map((task, index) => (
            <div
              key={task.id}
              className={`border-2 p-4 transition-all ${
                task.completed
                  ? 'border-pixel-gray bg-pixel-gray bg-opacity-20'
                  : 'border-white bg-black'
              }`}
            >
              <div className="flex items-start gap-3">
                {/* 复选框 */}
                <button
                  onClick={() => !task.completed && onTaskComplete(task.id)}
                  disabled={task.completed || isLoading}
                  className={`flex-shrink-0 w-6 h-6 border-2 flex items-center justify-center font-mono text-sm ${
                    task.completed
                      ? 'border-pixel-gray bg-white text-black'
                      : 'border-white bg-black text-white hover:bg-white hover:text-black'
                  } ${isLoading ? 'cursor-not-allowed' : 'cursor-pointer'}`}
                >
                  {task.completed ? '✓' : ''}
                </button>

                {/* 任务内容 */}
                <div className="flex-grow">
                  <div className="flex items-start justify-between gap-2">
                    <h3 className={`font-mono text-sm ${
                      task.completed ? 'text-pixel-gray line-through' : 'text-white'
                    }`}>
                      {index + 1}. {task.title}
                    </h3>
                    {task.estimated_time && (
                      <span className="text-pixel-light-gray font-mono text-xs flex-shrink-0">
                        ⏱ {task.estimated_time}
                      </span>
                    )}
                  </div>
                  
                  {task.description && (
                    <p className={`mt-2 font-mono text-xs ${
                      task.completed ? 'text-pixel-gray' : 'text-pixel-light-gray'
                    }`}>
                      {task.description}
                    </p>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* 进度统计 */}
        <div className="mt-4 pt-4 border-t-2 border-white">
          <p className="text-white font-mono text-sm text-center">
            进度: {tasks.filter(t => t.completed).length} / {tasks.length} 已完成
          </p>
          
          {/* 进度条 */}
          <div className="mt-2 h-4 border-2 border-white bg-black">
            <div
              className="h-full bg-white transition-all duration-300"
              style={{
                width: `${(tasks.filter(t => t.completed).length / tasks.length) * 100}%`
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

