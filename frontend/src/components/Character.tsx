import React from 'react';
import { CharacterState } from '../types';

interface CharacterProps {
  state: CharacterState;
  position?: 'left' | 'right' | 'center';
  fixed?: boolean;
}

export const Character: React.FC<CharacterProps> = ({ state, position = 'center', fixed = false }) => {
  // 使用 ASCII 艺术来创建像素风格的角色
  const getCharacterArt = () => {
    switch (state) {
      case 'idle':
        return (
          <div className="text-white font-mono text-sm leading-tight">
            <pre>{`
    ▓▓▓▓▓▓
  ▓▓░░░░░░▓▓
  ▓░░●░░●░░▓
  ▓░░░░░░░░▓
  ▓░░░▬▬▬░░▓
    ▓▓▓▓▓▓
      ▓▓
    ▓▓▓▓▓▓
    ▓    ▓
  ▓▓      ▓▓
  ▓        ▓
`}</pre>
          </div>
        );
      case 'thinking':
        return (
          <div className="text-white font-mono text-sm leading-tight pixel-animate">
            <pre>{`
    ▓▓▓▓▓▓
  ▓▓░░░░░░▓▓
  ▓░░●░░●░░▓
  ▓░░░░░░░░▓
  ▓░░░○○○░░▓
    ▓▓▓▓▓▓  ....
      ▓▓
    ▓▓▓▓▓▓
    ▓    ▓
  ▓▓      ▓▓
  ▓        ▓
`}</pre>
          </div>
        );
      case 'celebrating':
        return (
          <div className="text-white font-mono text-sm leading-tight">
            <pre>{`
    ▓▓▓▓▓▓
  ▓▓░░░░░░▓▓
  ▓░░◆░░◆░░▓
  ▓░░░░░░░░▓
  ▓░░▬▬▬▬░░▓
    ▓▓▓▓▓▓
  ▓▓  ▓▓  ▓▓
    ▓▓▓▓▓▓
  ▓▓  ▓  ▓▓
▓▓          ▓▓
  ★  ★  ★
`}</pre>
          </div>
        );
      default:
        return null;
    }
  };

  const getPositionClasses = () => {
    if (!fixed) return 'flex flex-col items-center justify-center p-4';
    
    const baseClasses = 'fixed bottom-4 z-30 flex flex-col items-center';
    switch (position) {
      case 'left':
        return `${baseClasses} left-4`;
      case 'right':
        return `${baseClasses} right-4`;
      default:
        return baseClasses;
    }
  };

  return (
    <div className={getPositionClasses()}>
      <div className="pixel-border bg-black p-6 hover:scale-105 transition-transform cursor-pointer">
        {getCharacterArt()}
      </div>
      <div className="mt-2 text-center">
        <p className="text-white font-mono text-xs pixel-border-thin bg-black px-2 py-1">
          {state === 'idle' && '待命中...'}
          {state === 'thinking' && '思考中...'}
          {state === 'celebrating' && '太棒了！'}
        </p>
      </div>
    </div>
  );
};

