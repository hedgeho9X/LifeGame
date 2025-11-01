import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { TherapyTicket } from '../types';
import { api } from '../api/client';

interface TherapyPanelProps {
  ticket: TherapyTicket;
  isVisible: boolean;
  onClose: () => void;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export const TherapyPanel: React.FC<TherapyPanelProps> = ({
  ticket,
  isVisible,
  onClose,
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [initialized, setInitialized] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 初始化 - 获取AI的开场白
  useEffect(() => {
    if (isVisible && !initialized) {
      initializeChat();
    }
  }, [isVisible]);

  // 自动滚动
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const initializeChat = async () => {
    setIsLoading(true);
    try {
      // 第一次调用，不传user_message，AI会主动开场
      const response = await api.therapyChat({
        ticket_id: ticket.id,
        user_message: undefined,
      });
      
      setMessages([{
        role: 'assistant',
        content: response.message,
      }]);
      
      setInitialized(true);
    } catch (error) {
      console.error('Failed to initialize therapy chat:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setIsLoading(true);

    // 添加用户消息到界面
    const newMessages = [...messages, {
      role: 'user' as const,
      content: userMessage,
    }];
    setMessages(newMessages);

    try {
      const response = await api.therapyChat({
        ticket_id: ticket.id,
        user_message: userMessage,
      });
      
      // 添加AI回复
      setMessages([...newMessages, {
        role: 'assistant',
        content: response.message,
      }]);
    } catch (error) {
      console.error('Failed to send message:', error);
      // 显示错误消息
      setMessages([...newMessages, {
        role: 'assistant',
        content: '抱歉，我遇到了一些问题。请稍后再试。',
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-80">
      <div className="pixel-border bg-black w-[90vw] max-w-4xl h-[85vh] flex flex-col">
        {/* 标题栏 */}
        <div className="p-4 border-b-2 border-white">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-white font-mono text-xl">💝 话疗时刻</h2>
              <p className="text-pixel-gray font-mono text-xs mt-1">
                完成"{ticket.goal_text}"的奖励
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

        {/* 对话区域 */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {!initialized && isLoading ? (
            <div className="text-center text-white font-mono py-8">
              <div className="pixel-animate">AI话疗师正在准备...</div>
            </div>
          ) : (
            messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] p-4 ${
                    msg.role === 'user'
                      ? 'bg-white text-black pixel-border-thin'
                      : 'bg-gradient-to-br from-purple-900 to-pink-900 text-white pixel-border-thin'
                  }`}
                >
                  <div className="font-mono text-xs mb-2 opacity-70">
                    {msg.role === 'user' ? '👤 你' : '💝 AI话疗师'}
                  </div>
                  {/* Markdown渲染 */}
                  <div className="font-mono text-sm prose prose-invert max-w-none therapy-content">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {msg.content}
                    </ReactMarkdown>
                  </div>
                </div>
              </div>
            ))
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* 输入区 */}
        <div className="p-4 border-t-2 border-white">
          <form onSubmit={handleSendMessage} className="space-y-2">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="分享你的感受..."
              disabled={isLoading || !initialized}
              rows={3}
              className="w-full bg-black text-white border-2 border-white p-3 font-mono text-sm focus:outline-none focus:border-purple-400 disabled:opacity-50 resize-none"
              onKeyDown={(e) => {
                if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
                  handleSendMessage(e);
                }
              }}
            />
            <button
              type="submit"
              disabled={isLoading || !inputMessage.trim() || !initialized}
              className={`w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white font-mono text-sm py-3 px-4 pixel-border-thin
                ${isLoading || !inputMessage.trim() || !initialized
                  ? 'opacity-50 cursor-not-allowed'
                  : 'hover:from-purple-700 hover:to-pink-700 active:translate-x-1 active:translate-y-1'
                }`}
            >
              {isLoading ? '💭 回复中...' : '💬 发送 (Cmd/Ctrl+Enter)'}
            </button>
          </form>
          <p className="text-pixel-gray font-mono text-xs text-center mt-2">
            这是你的专属奖励时刻，尽情享受吧 ✨
          </p>
        </div>
      </div>

      {/* Markdown样式 */}
      <style>{`
        .therapy-content {
          color: inherit;
        }
        .therapy-content p {
          margin: 0.5em 0;
        }
        .therapy-content ul, .therapy-content ol {
          margin: 0.5em 0;
          padding-left: 1.5em;
        }
        .therapy-content li {
          margin: 0.25em 0;
        }
        .therapy-content strong {
          font-weight: bold;
        }
        .therapy-content code {
          background: rgba(255, 255, 255, 0.1);
          padding: 0.2em 0.4em;
          border-radius: 2px;
          font-family: monospace;
        }
        .therapy-content pre {
          background: rgba(255, 255, 255, 0.05);
          padding: 0.5em;
          margin: 0.5em 0;
          overflow-x: auto;
        }
        .therapy-content blockquote {
          border-left: 3px solid rgba(255, 255, 255, 0.3);
          padding-left: 1em;
          margin: 0.5em 0;
          font-style: italic;
        }
        .therapy-content h1, .therapy-content h2, .therapy-content h3 {
          margin: 0.5em 0 0.3em 0;
          font-weight: bold;
        }
      `}</style>
    </div>
  );
};

