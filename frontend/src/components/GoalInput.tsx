import React, { useState } from 'react';

interface GoalInputProps {
  onSubmit: (goalText: string, background: string) => void;
  isLoading: boolean;
}

export const GoalInput: React.FC<GoalInputProps> = ({ onSubmit, isLoading }) => {
  const [goalText, setGoalText] = useState('');
  const [background, setBackground] = useState('');
  const [showBackgroundInput, setShowBackgroundInput] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (goalText.trim()) {
      onSubmit(goalText.trim(), background.trim());
      setGoalText('');
      setBackground('');
      setShowBackgroundInput(false);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-4">
      <div className="pixel-border bg-black p-6">
        <h2 className="text-white font-mono text-lg mb-4 text-center">
          ▼ 输入你的目标 ▼
        </h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* 目标输入 */}
          <div>
            <label className="block text-white font-mono text-sm mb-2">
              目标:
            </label>
            <textarea
              value={goalText}
              onChange={(e) => setGoalText(e.target.value)}
              className="w-full bg-black text-white border-2 border-white p-3 font-mono text-sm focus:outline-none focus:border-pixel-light-gray"
              placeholder="例如: 完成简历并海投 20 家公司..."
              rows={3}
              disabled={isLoading}
            />
          </div>

          {/* 背景信息切换按钮 */}
          <button
            type="button"
            onClick={() => setShowBackgroundInput(!showBackgroundInput)}
            className="text-white font-mono text-xs underline hover:text-pixel-light-gray"
            disabled={isLoading}
          >
            {showBackgroundInput ? '▲ 隐藏背景信息' : '▼ 添加个人背景信息（可选）'}
          </button>

          {/* 背景信息输入 */}
          {showBackgroundInput && (
            <div>
              <label className="block text-white font-mono text-sm mb-2">
                个人背景:
              </label>
              <textarea
                value={background}
                onChange={(e) => setBackground(e.target.value)}
                className="w-full bg-black text-white border-2 border-white p-3 font-mono text-sm focus:outline-none focus:border-pixel-light-gray"
                placeholder="例如: 我是计算机专业大四学生，擅长 Python 和前端开发..."
                rows={3}
                disabled={isLoading}
              />
            </div>
          )}

          {/* 提交按钮 */}
          <button
            type="submit"
            disabled={isLoading || !goalText.trim()}
            className={`w-full bg-white text-black font-mono text-sm py-3 px-6 pixel-border-thin
              ${isLoading || !goalText.trim() 
                ? 'opacity-50 cursor-not-allowed' 
                : 'hover:bg-pixel-light-gray active:translate-x-1 active:translate-y-1'
              }`}
          >
            {isLoading ? '▶ AI 生成中...' : '▶ 开始冒险'}
          </button>
        </form>

        {/* 提示信息 */}
        <div className="mt-4 text-center">
          <p className="text-pixel-gray font-mono text-xs">
            AI 会根据你的目标生成游戏故事和任务清单
          </p>
        </div>
      </div>
    </div>
  );
};

