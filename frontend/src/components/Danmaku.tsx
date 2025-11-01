import React, { useEffect, useState } from 'react';

interface DanmakuItem {
  id: number;
  text: string;
  top: number;
  duration: number;
  delay: number;
}

interface DanmakuProps {
  messages: string[];
  onComplete?: () => void;
}

export const Danmaku: React.FC<DanmakuProps> = ({ messages, onComplete }) => {
  const [danmakuItems, setDanmakuItems] = useState<DanmakuItem[]>([]);

  useEffect(() => {
    if (messages.length === 0) return;

    // 为每条消息创建弹幕项
    const items: DanmakuItem[] = messages.map((msg, index) => ({
      id: Date.now() + index,
      text: msg,
      top: 50 + (index * 70) % 500, // 分散在不同高度
      duration: 12 + Math.random() * 4, // 12-16秒，更慢
      delay: index * 1.5, // 错开出现时间
    }));

    setDanmakuItems(items);

    // 在所有弹幕完成后清理
    const maxDuration = Math.max(...items.map(item => item.duration + item.delay));
    const timer = setTimeout(() => {
      setDanmakuItems([]);
      onComplete?.();
    }, maxDuration * 1000);

    return () => clearTimeout(timer);
  }, [messages, onComplete]);

  if (danmakuItems.length === 0) return null;

  return (
    <div className="fixed inset-0 pointer-events-none z-40 overflow-hidden">
      {danmakuItems.map((item) => (
        <div
          key={item.id}
          className="absolute whitespace-nowrap font-mono text-2xl font-bold"
          style={{
            top: `${item.top}px`,
            right: '-100%',
            color: '#ffffff',
            animation: `danmaku-slide ${item.duration}s linear ${item.delay}s`,
            textShadow: '3px 3px 6px rgba(0,0,0,0.9), -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000',
          }}
        >
          {item.text}
        </div>
      ))}
      <style>{`
        @keyframes danmaku-slide {
          from {
            right: -100%;
          }
          to {
            right: 100%;
          }
        }
      `}</style>
    </div>
  );
};


