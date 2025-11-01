import React, { useState, useEffect } from 'react';
import { TherapyTicket } from '../types';
import { api } from '../api/client';
import { TherapyPanel } from './TherapyPanel';

interface TherapyTicketListProps {
  userId: number;
  isVisible: boolean;
  onClose: () => void;
}

export const TherapyTicketList: React.FC<TherapyTicketListProps> = ({
  userId,
  isVisible,
  onClose,
}) => {
  const [tickets, setTickets] = useState<TherapyTicket[]>([]);
  const [selectedTicket, setSelectedTicket] = useState<TherapyTicket | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (isVisible) {
      loadTickets();
    }
  }, [isVisible, userId]);

  const loadTickets = async () => {
    setIsLoading(true);
    try {
      const data = await api.getTherapyTickets(userId);
      setTickets(data);
    } catch (error) {
      console.error('Failed to load therapy tickets:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUseTicket = (ticket: TherapyTicket) => {
    setSelectedTicket(ticket);
  };

  const handleCloseTherapy = () => {
    setSelectedTicket(null);
    loadTickets(); // 刷新列表
  };

  if (!isVisible) return null;

  // 如果选中了票，显示话疗界面
  if (selectedTicket) {
    return (
      <TherapyPanel
        ticket={selectedTicket}
        isVisible={true}
        onClose={handleCloseTherapy}
      />
    );
  }

  // 显示票券列表
  return (
    <div className="fixed inset-0 z-40 flex items-center justify-center bg-black bg-opacity-80">
      <div className="pixel-border bg-black w-[90vw] max-w-3xl max-h-[85vh] flex flex-col">
        {/* 标题栏 */}
        <div className="p-4 border-b-2 border-white">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-white font-mono text-xl">💝 话疗券</h2>
              <p className="text-pixel-gray font-mono text-xs mt-1">
                每完成一个目标，获得一张专属话疗券
              </p>
            </div>
            <button
              onClick={onClose}
              className="text-white font-mono text-sm hover:text-pixel-light-gray px-3 py-1 pixel-border-thin"
            >
              ✕ 关闭
            </button>
          </div>
        </div>

        {/* 票券列表 */}
        <div className="flex-1 overflow-y-auto p-6">
          {isLoading ? (
            <div className="text-center text-white font-mono py-8">
              <div className="pixel-animate">加载中...</div>
            </div>
          ) : tickets.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">🎯</div>
              <p className="text-white font-mono text-lg mb-2">暂无话疗券</p>
              <p className="text-pixel-gray font-mono text-sm">
                完成目标即可获得话疗券哦！
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {tickets.map((ticket) => (
                <div
                  key={ticket.id}
                  className={`p-5 pixel-border-thin ${
                    ticket.used
                      ? 'bg-gray-900 opacity-60'
                      : 'bg-gradient-to-br from-purple-900 to-pink-900'
                  }`}
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-2xl">
                          {ticket.used ? '✅' : '💝'}
                        </span>
                        <h3 className="text-white font-mono text-sm">
                          {ticket.used ? '已使用的话疗券' : '可用话疗券'}
                        </h3>
                      </div>
                      <p className="text-white font-mono text-base mb-2">
                        完成目标：{ticket.goal_text}
                      </p>
                      <div className="text-pixel-gray font-mono text-xs space-y-1">
                        <p>获得时间：{new Date(ticket.created_at).toLocaleString('zh-CN')}</p>
                        {ticket.used && ticket.used_at && (
                          <p>使用时间：{new Date(ticket.used_at).toLocaleString('zh-CN')}</p>
                        )}
                      </div>
                    </div>
                    {!ticket.used && (
                      <button
                        onClick={() => handleUseTicket(ticket)}
                        className="bg-gradient-to-r from-yellow-500 to-orange-500 text-black font-mono text-sm py-2 px-4 pixel-border-thin hover:from-yellow-600 hover:to-orange-600 active:translate-x-1 active:translate-y-1 whitespace-nowrap"
                      >
                        💬 开始话疗
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* 提示信息 */}
        <div className="p-4 border-t-2 border-white">
          <p className="text-pixel-gray font-mono text-xs text-center">
            💡 提示：每张话疗券可以和AI进行一次深度对话，珍惜每一次奖励时刻 ✨
          </p>
        </div>
      </div>
    </div>
  );
};

