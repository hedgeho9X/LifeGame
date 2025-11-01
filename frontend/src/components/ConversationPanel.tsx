import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { ConversationMessage, Task } from '../types';
import { api } from '../api/client';

interface ConversationPanelProps {
  goalId: number;
  goalText: string;
  currentTasks: Task[];
  isVisible: boolean;
  onClose: () => void;
  onTasksUpdated: (tasks: Task[], summary: string) => void;
}

export const ConversationPanel: React.FC<ConversationPanelProps> = ({
  goalId,
  goalText,
  currentTasks,
  isVisible,
  onClose,
  onTasksUpdated,
}) => {
  const [messages, setMessages] = useState<ConversationMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isApplying, setIsApplying] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 加载对话历史
  useEffect(() => {
    if (isVisible && goalId) {
      loadConversations();
    }
  }, [isVisible, goalId]);

  // 自动滚动到底部
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadConversations = async () => {
    try {
      const conversations = await api.getConversations(goalId);
      setMessages(conversations);
    } catch (error) {
      console.error('Failed to load conversations:', error);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setIsLoading(true);

    // 添加用户消息到界面
    const userMsg: ConversationMessage = {
      role: 'user',
      content: userMessage,
      created_at: new Date().toISOString(),
    };
    setMessages(prev => [...prev, userMsg]);

    try {
      const response = await api.sendMessage(goalId, userMessage);
      
      // 添加AI回复
      setMessages(prev => [...prev, response.message]);
    } catch (error) {
      console.error('Failed to send message:', error);
      // 显示错误消息
      const errorMsg: ConversationMessage = {
        role: 'assistant',
        content: '抱歉，我遇到了一些问题。请稍后再试。',
        created_at: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleApplyUpdates = async () => {
    if (messages.length === 0) {
      alert('还没有对话历史，无法应用更新');
      return;
    }

    setIsApplying(true);
    try {
      const result = await api.applyTaskUpdates(goalId);
      if (result.success) {
        onTasksUpdated(result.tasks, result.summary);
        // 添加一条系统消息
        const systemMsg: ConversationMessage = {
          role: 'assistant',
          content: `✅ **任务已更新！**\n\n${result.summary}`,
          created_at: new Date().toISOString(),
        };
        setMessages(prev => [...prev, systemMsg]);
      }
    } catch (error) {
      console.error('Failed to apply updates:', error);
      alert('应用更新失败，请重试');
    } finally {
      setIsApplying(false);
    }
  };

  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-70">
      <div className="pixel-border bg-black w-[95vw] h-[90vh] flex flex-col">
        {/* 标题栏 */}
        <div className="flex justify-between items-center p-4 border-b-2 border-white">
          <h2 className="text-white font-mono text-lg">💬 与AI助手对话 - 细化任务规划</h2>
          <button
            onClick={onClose}
            className="text-white font-mono text-sm hover:text-pixel-light-gray px-3 py-1 pixel-border-thin"
          >
            ✕ 关闭
          </button>
        </div>

        {/* 分屏主体 */}
        <div className="flex-1 flex overflow-hidden">
          {/* 左侧：对话区 */}
          <div className="w-1/2 flex flex-col border-r-2 border-white">
            {/* 对话历史 */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {messages.length === 0 ? (
                <div className="text-center text-pixel-gray font-mono text-sm py-8">
                  💡 在这里与AI讨论你的任务规划<br/>
                  可以要求添加、删除或修改任务
                </div>
              ) : (
                messages.map((msg, index) => (
                  <div
                    key={index}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[85%] p-3 ${
                        msg.role === 'user'
                          ? 'bg-white text-black pixel-border-thin'
                          : 'bg-pixel-dark-gray text-white pixel-border-thin'
                      }`}
                    >
                      <div className="font-mono text-xs mb-1 opacity-70">
                        {msg.role === 'user' ? '👤 你' : '🤖 AI助手'}
                      </div>
                      {/* Markdown渲染 */}
                      <div className="font-mono text-sm prose prose-invert max-w-none markdown-content">
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
                  placeholder="例如：第一个任务太复杂了，能不能拆分成两个更简单的任务？"
                  disabled={isLoading}
                  rows={3}
                  className="w-full bg-black text-white border-2 border-white p-3 font-mono text-sm focus:outline-none focus:border-pixel-light-gray disabled:opacity-50 resize-none"
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
                      handleSendMessage(e);
                    }
                  }}
                />
                <div className="flex gap-2">
                  <button
                    type="submit"
                    disabled={isLoading || !inputMessage.trim()}
                    className={`flex-1 bg-white text-black font-mono text-sm py-2 px-4 pixel-border-thin
                      ${isLoading || !inputMessage.trim()
                        ? 'opacity-50 cursor-not-allowed'
                        : 'hover:bg-pixel-light-gray active:translate-x-1 active:translate-y-1'
                      }`}
                  >
                    {isLoading ? '⏳ 发送中...' : '📤 发送 (Cmd/Ctrl+Enter)'}
                  </button>
                </div>
              </form>
            </div>
          </div>

          {/* 右侧：当前任务列表 */}
          <div className="w-1/2 flex flex-col">
            <div className="p-4 border-b-2 border-white">
              <h3 className="text-white font-mono text-md">📋 当前任务列表</h3>
              <p className="text-pixel-gray font-mono text-xs mt-1">
                目标：{goalText}
              </p>
            </div>
            
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {currentTasks.map((task, index) => (
                <div
                  key={task.id}
                  className={`border-2 p-3 ${
                    task.completed
                      ? 'border-pixel-gray bg-pixel-gray bg-opacity-20'
                      : 'border-white bg-black'
                  }`}
                >
                  <div className="flex items-start gap-2">
                    <span className="text-white font-mono text-sm flex-shrink-0">
                      {index + 1}.
                    </span>
                    <div className="flex-grow">
                      <h4 className={`font-mono text-sm ${
                        task.completed ? 'text-pixel-gray line-through' : 'text-white'
                      }`}>
                        {task.title}
                      </h4>
                      {task.description && (
                        <p className={`mt-1 font-mono text-xs ${
                          task.completed ? 'text-pixel-gray' : 'text-pixel-light-gray'
                        }`}>
                          {task.description}
                        </p>
                      )}
                      <div className="mt-2 flex items-center gap-2 text-xs">
                        {task.estimated_time && (
                          <span className="text-pixel-light-gray font-mono">
                            ⏱ {task.estimated_time}
                          </span>
                        )}
                        {task.skill_rewards && Object.keys(task.skill_rewards).length > 0 && (
                          <div className="flex flex-wrap gap-1">
                            {Object.entries(task.skill_rewards).map(([skill, value]) => (
                              <span
                                key={skill}
                                className="pixel-border-thin px-1 py-0.5 font-mono text-xs bg-white text-black"
                              >
                                {skill} +{value}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* 应用更新按钮 */}
            <div className="p-4 border-t-2 border-white">
              <button
                onClick={handleApplyUpdates}
                disabled={isApplying || messages.length === 0}
                className={`w-full bg-white text-black font-mono text-sm py-3 px-4 pixel-border-thin
                  ${isApplying || messages.length === 0
                    ? 'opacity-50 cursor-not-allowed'
                    : 'hover:bg-pixel-light-gray active:translate-x-1 active:translate-y-1'
                  }`}
              >
                {isApplying ? '⏳ 应用中...' : '✅ 应用修改到任务列表'}
              </button>
              <p className="text-pixel-gray font-mono text-xs text-center mt-2">
                {messages.length === 0 
                  ? '先与AI讨论，然后点击此按钮更新任务'
                  : '点击后AI会根据对话内容更新你的任务列表'
                }
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Markdown样式 */}
      <style>{`
        .markdown-content {
          color: inherit;
        }
        .markdown-content p {
          margin: 0.5em 0;
        }
        .markdown-content ul, .markdown-content ol {
          margin: 0.5em 0;
          padding-left: 1.5em;
        }
        .markdown-content li {
          margin: 0.25em 0;
        }
        .markdown-content strong {
          font-weight: bold;
          color: white;
        }
        .markdown-content code {
          background: rgba(255, 255, 255, 0.1);
          padding: 0.2em 0.4em;
          border-radius: 2px;
          font-family: monospace;
        }
        .markdown-content pre {
          background: rgba(255, 255, 255, 0.05);
          padding: 0.5em;
          margin: 0.5em 0;
          overflow-x: auto;
        }
        .markdown-content blockquote {
          border-left: 3px solid rgba(255, 255, 255, 0.3);
          padding-left: 1em;
          margin: 0.5em 0;
          font-style: italic;
        }
        .markdown-content h1, .markdown-content h2, .markdown-content h3 {
          margin: 0.5em 0 0.3em 0;
          font-weight: bold;
        }
      `}</style>
    </div>
  );
};
