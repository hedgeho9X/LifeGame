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
      <div className="absolute inset-0 bg-black bg-opacity-70 animate-pulse" />
      
      {/* 粒子效果 */}
      <div className="absolute inset-0">
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="absolute w-2 h-2 bg-white rounded-full animate-ping"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 2}s`,
              animationDuration: `${1 + Math.random() * 2}s`,
            }}
          />
        ))}
      </div>
      
      {/* 奖励显示 */}
      <div className="relative pixel-border bg-gradient-to-br from-black via-pixel-dark-gray to-black p-8 animate-bounce shadow-2xl">
        <h2 className="text-white font-mono text-2xl mb-4 text-center animate-pulse">
          ★ 🎉 获得奖励！🎉 ★
        </h2>
        
        <div className="space-y-3">
          {Object.entries(rewards).map(([key, value], index) => (
            <div 
              key={key} 
              className="flex items-center justify-between gap-4 animate-slide-in"
              style={{
                animationDelay: `${index * 0.1}s`,
              }}
            >
              <span className="text-white font-mono text-lg">{key}</span>
              <span className="text-white font-mono text-3xl font-bold animate-bounce"
                style={{
                  animationDelay: `${index * 0.15}s`,
                  textShadow: '0 0 10px rgba(255,255,255,0.8)',
                }}
              >
                +{value}
              </span>
            </div>
          ))}
        </div>
        
        {/* 装饰性星星 */}
        <div className="mt-4 text-center text-white font-mono text-3xl animate-spin-slow">
          ✦ ✧ ✦ ✧ ✦
        </div>
      </div>

      <style>{`
        @keyframes slide-in {
          from {
            opacity: 0;
            transform: translateX(-20px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }
        
        @keyframes spin-slow {
          from {
            transform: rotate(0deg);
          }
          to {
            transform: rotate(360deg);
          }
        }

        .animate-slide-in {
          animation: slide-in 0.5s ease-out forwards;
          opacity: 0;
        }

        .animate-spin-slow {
          animation: spin-slow 3s linear infinite;
        }
      `}</style>
    </div>
  );
};

