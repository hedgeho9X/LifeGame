import React from 'react';
import { CharacterState } from '../types';

interface CharacterProps {
  state: CharacterState;
}

export const Character: React.FC<CharacterProps> = ({ state }) => {
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

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <div className="pixel-border bg-black p-6">
        {getCharacterArt()}
      </div>
      <div className="mt-4 text-center">
        <p className="text-white font-mono text-xs">
          {state === 'idle' && '待命中...'}
          {state === 'thinking' && '思考中...'}
          {state === 'celebrating' && '太棒了！'}
        </p>
      </div>
    </div>
  );
};

