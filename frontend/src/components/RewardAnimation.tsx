import React, { useEffect } from 'react';

interface RewardAnimationProps {
  rewards: Record<string, number>;
  onComplete: () => void;
}

export const RewardAnimation: React.FC<RewardAnimationProps> = ({ 
  rewards, 
  onComplete 
}) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onComplete();
    }, 2500);

    return () => clearTimeout(timer);
  }, [onComplete]);

  if (Object.keys(rewards).length === 0) {
    return null;
  }

  return (
    <div className="fixed inset-0 flex items-center justify-center z-50 pointer-events-none">
      {/* 背景遮罩 */}
      <div className="absolute inset-0 bg-black bg-opacity-70" />
      
      {/* 奖励显示 */}
      <div className="relative pixel-border bg-black p-8 animate-bounce">
        <h2 className="text-white font-mono text-xl mb-4 text-center">
          ★ 获得奖励！ ★
        </h2>
        
        <div className="space-y-3">
          {Object.entries(rewards).map(([key, value]) => (
            <div key={key} className="flex items-center justify-between gap-4">
              <span className="text-white font-mono text-lg">{key}</span>
              <span className="text-white font-mono text-2xl font-bold">
                +{value}
              </span>
            </div>
          ))}
        </div>
        
        {/* 装饰性星星 */}
        <div className="mt-4 text-center text-white font-mono text-2xl">
          ✦ ✧ ✦
        </div>
      </div>
    </div>
  );
};

