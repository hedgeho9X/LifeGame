import React from 'react';

interface StoryDisplayProps {
  story: string;
  goalText: string;
}

export const StoryDisplay: React.FC<StoryDisplayProps> = ({ story, goalText }) => {
  return (
    <div className="w-full max-w-2xl mx-auto p-4">
      <div className="pixel-border bg-black p-6">
        <h2 className="text-white font-mono text-lg mb-4 text-center">
          ▼ 你的冒险故事 ▼
        </h2>
        
        {/* 原始目标 */}
        <div className="mb-4 pb-4 border-b-2 border-white">
          <p className="text-pixel-light-gray font-mono text-xs mb-1">目标:</p>
          <p className="text-white font-mono text-sm">{goalText}</p>
        </div>
        
        {/* 游戏故事 */}
        <div className="bg-pixel-gray bg-opacity-10 border-2 border-white p-4">
          <p className="text-white font-mono text-sm leading-relaxed whitespace-pre-wrap">
            {story}
          </p>
        </div>
        
        {/* 装饰性元素 */}
        <div className="mt-4 text-center">
          <p className="text-pixel-light-gray font-mono text-xs">
            ═══════════════════════════════
          </p>
        </div>
      </div>
    </div>
  );
};

