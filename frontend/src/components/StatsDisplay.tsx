import React from 'react';

interface StatsDisplayProps {
  stats: Record<string, number>;
}

export const StatsDisplay: React.FC<StatsDisplayProps> = ({ stats }) => {
  if (Object.keys(stats).length === 0) {
    return null;
  }

  return (
    <div className="fixed top-4 right-4 w-64">
      <div className="pixel-border bg-black p-4">
        <h3 className="text-white font-mono text-sm mb-3 text-center">
          ▼ 角色数值 ▼
        </h3>
        
        <div className="space-y-2">
          {Object.entries(stats).map(([key, value]) => (
            <div key={key} className="border-2 border-white p-2">
              <div className="flex justify-between items-center">
                <span className="text-white font-mono text-xs">{key}</span>
                <span className="text-white font-mono text-sm font-bold">
                  {value}
                </span>
              </div>
              
              {/* 特殊处理经验值进度条 */}
              {key === '经验值' && stats['等级'] && (
                <div className="mt-1 h-2 border border-white bg-black">
                  <div
                    className="h-full bg-white transition-all duration-300"
                    style={{
                      width: `${(value / (stats['等级'] * 100)) * 100}%`
                    }}
                  />
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

