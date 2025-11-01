from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

# 定义输出结构
class TaskItem(BaseModel):
    title: str = Field(description="任务标题")
    description: str = Field(description="任务详细描述")
    estimated_time: str = Field(description="预计完成时间，如：30分钟、1小时")
    skill_rewards: Dict[str, int] = Field(description="完成该任务获得的技能奖励，如：{'专注力': 5, '执行力': 3}")

class GameResponse(BaseModel):
    story: str = Field(description="根据用户目标生成的游戏化故事背景")
    tasks: List[TaskItem] = Field(description="拆解后的任务列表，3-8个任务")
    stats: Dict[str, int] = Field(description="初始数值系统，如：{'等级': 1, '经验值': 0, '金币': 0, '成就点': 0}")
    praise_messages: List[str] = Field(description="5-8条个性化的夸赞弹幕语句，鼓励用户完成目标")

class TaskUpdateResponse(BaseModel):
    tasks: List[TaskItem] = Field(description="更新后的任务列表")
    summary: str = Field(description="更新总结，说明做了哪些修改")

class LifeGameAgent:
    def __init__(self):
        # 支持 OpenRouter 或直接使用 OpenAI
        api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENROUTER_BASE_URL")
        model_name = os.getenv("AI_MODEL", "gpt-4")
        
        if base_url:
            # 使用 OpenRouter 或自定义 base URL
            self.llm = ChatOpenAI(
                model=model_name,
                temperature=0.7,
                api_key=api_key,
                base_url=base_url
            )
        else:
            # 使用默认 OpenAI
            self.llm = ChatOpenAI(
                model=model_name,
                temperature=0.7,
                api_key=api_key
            )
        self.parser = PydanticOutputParser(pydantic_object=GameResponse)
        
    def create_game_plan(self, goal_text: str, user_background: str = None) -> GameResponse:
        """根据用户目标创建游戏化计划"""
        
        template = """你是一个生活游戏化系统的 AI 助手，擅长将生活目标转化为有趣的游戏任务。

用户目标：{goal_text}

{background_info}

请完成以下任务：

1. **创造游戏故事**：根据用户目标，创造一个有趣的、激励人心的游戏化故事背景。这个故事应该：
   - 将用户的现实目标包装成游戏世界中的冒险任务
   - 使用像素游戏风格的叙事方式（可以参考经典 RPG 游戏）
   - 简短但有感染力（100-200字）
   - 让用户感觉自己是游戏中的英雄

2. **拆解任务**：将目标拆解为 3-8 个具体、可执行的小任务。每个任务应该：
   - 清晰具体，有明确的完成标准
   - 难度适中，单个任务耗时在 30分钟 到 2小时 之间
   - 按照合理的执行顺序排列
   - 使用游戏化的语言描述（但保持实用性）
   - **每个任务必须包含 estimated_time 字段**

3. **设计个性化数值系统**：根据用户的目标类型创建一个个性化的数值系统（不一定是传统的经验值）。数值系统应该包含：
   - 等级（初始为 1）
   - 3-5个与目标相关的技能属性（如：学习目标可以有"专注力"、"记忆力"、"创造力"等）
   - 每个技能的初始值都设为 0（等级除外）
   - 技能名称要有创意且与目标相关

4. **为每个任务分配技能奖励**：为每个任务设计独特的技能奖励，表示完成该任务可以提升哪些技能。
   - 每个任务应该奖励 2-3 个相关技能
   - 奖励值在 3-10 之间
   - 不同任务应该奖励不同的技能组合

5. **生成夸赞弹幕**：根据用户目标生成5-8条个性化的夸赞语句，用于弹幕显示。
   - 每条8-15个字，简短有力
   - 要有激励性和个性化
   - 可以使用emoji表情
   - 与目标紧密相关

返回格式示例：
{{
  "story": "在像素王国中，你是被选中的勇者...",
  "tasks": [
    {{
      "title": "【任务一】具体的任务标题",
      "description": "详细的任务描述，说明具体要做什么",
      "estimated_time": "30分钟",
      "skill_rewards": {{"专注力": 5, "执行力": 3}}
    }},
    {{
      "title": "【任务二】具体的任务标题",
      "description": "详细的任务描述",
      "estimated_time": "1小时",
      "skill_rewards": {{"创造力": 7, "思考力": 5}}
    }}
  ],
  "stats": {{
    "等级": 1,
    "专注力": 0,
    "执行力": 0,
    "创造力": 0,
    "思考力": 0
  }},
  "praise_messages": [
    "💪 你真是太棒了！",
    "🔥 继续加油前进！",
    "⭐ 每一步都很精彩！",
    "🚀 你的努力终会发光！",
    "🌟 相信自己的力量！"
  ]
}}

{format_instructions}

⚠️ 重要提示：
1. 每个任务必须包含 title、description、estimated_time 和 skill_rewards 四个字段
2. 必须包含顶层的 stats 字段，且技能名称要与任务奖励中的技能名称一致66
3. 请严格按照上述 JSON 格式返回完整结果"""

        background_info = ""
        if user_background:
            background_info = f"用户背景信息：{user_background}\n请结合用户背景来设计更个性化的故事和任务。"
        
        prompt = ChatPromptTemplate.from_template(template)
        
        chain = prompt | self.llm | self.parser
        
        result = chain.invoke({
            "goal_text": goal_text,
            "background_info": background_info,
            "format_instructions": self.parser.get_format_instructions()
        })
        
        return result
    
    def calculate_rewards(self, skill_rewards: Dict[str, int], current_stats: Dict[str, int]) -> Dict[str, int]:
        """根据任务的skill_rewards计算奖励并检查是否升级"""
        rewards = skill_rewards.copy()
        
        # 计算技能总值来判断是否升级
        total_skill_points = sum(current_stats.get(k, 0) for k in current_stats if k != "等级")
        new_skill_points = total_skill_points + sum(skill_rewards.values())
        
        # 等级提升判断：每100技能点升1级
        current_level = current_stats.get("等级", 1)
        exp_needed = current_level * 100
        
        if new_skill_points >= exp_needed:
            rewards["等级"] = 1
        
        return rewards
    
    def refine_tasks(self, goal_text: str, current_tasks: List[Dict], user_message: str, conversation_history: List[Dict]) -> str:
        """根据用户反馈细化和修改任务"""
        
        # 构建对话历史
        messages = [
            {"role": "system", "content": """你是一个生活游戏化系统的AI助手。用户正在与你讨论他们的目标和任务。
你需要根据用户的反馈来调整、细化或重新组织任务。

请以自然、友好的方式回应用户，并在必要时提供修改建议。
使用 **Markdown** 格式让你的回复更清晰易读：
- 使用 **加粗** 强调重点
- 使用列表组织建议
- 使用代码块展示任务标题
- 使用引用块展示重要提示

保持游戏化、激励的语气。"""}
        ]
        
        # 添加历史对话
        for msg in conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # 添加当前目标和任务信息
        context = f"""
当前目标：{goal_text}

当前任务列表：
"""
        for i, task in enumerate(current_tasks, 1):
            context += f"{i}. {task['title']}\n   描述：{task['description']}\n   预计时间：{task['estimated_time']}\n\n"
        
        messages.append({"role": "system", "content": context})
        messages.append({"role": "user", "content": user_message})
        
        # 调用LLM
        response = self.llm.invoke(messages)
        
        return response.content
    
    def update_tasks_from_conversation(
        self, 
        goal_text: str, 
        current_tasks: List[Dict], 
        conversation_history: List[Dict],
        current_stats: Dict[str, int]
    ) -> TaskUpdateResponse:
        """根据对话历史更新任务规划"""
        
        # 构建对话上下文
        conversation_text = ""
        for msg in conversation_history:
            role_name = "用户" if msg["role"] == "user" else "AI助手"
            conversation_text += f"{role_name}: {msg['content']}\n\n"
        
        # 构建当前任务列表
        current_tasks_text = ""
        for i, task in enumerate(current_tasks, 1):
            current_tasks_text += f"{i}. {task['title']}\n   描述：{task['description']}\n   时间：{task['estimated_time']}\n   技能奖励：{task.get('skill_rewards', {})}\n\n"
        
        # 创建parser
        parser = PydanticOutputParser(pydantic_object=TaskUpdateResponse)
        
        template = """你是一个生活游戏化系统的 AI 助手。根据用户与AI的对话历史，更新任务规划。

**用户目标**：{goal_text}

**当前技能系统**：
{current_stats}

**对话历史**：
{conversation_text}

**当前任务列表**：
{current_tasks_text}

**任务**：
根据对话内容，分析用户的修改需求，生成更新后的任务列表。请：
1. 仔细分析对话中用户提出的所有修改建议
2. 保留未提及的任务（如果合理）
3. 添加、删除或修改任务以满足用户需求
4. 确保每个任务都有 title、description、estimated_time 和 skill_rewards
5. skill_rewards 必须使用当前技能系统中的技能名称
6. 写一个简短的更新总结（summary），说明做了哪些修改

{format_instructions}

⚠️ 重要：
- 返回的任务必须是完整的任务列表（不是增量更新）
- skill_rewards中的技能名称必须与当前技能系统一致
- 保持游戏化、激励的语气"""

        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm | parser
        
        result = chain.invoke({
            "goal_text": goal_text,
            "current_stats": current_stats,
            "conversation_text": conversation_text,
            "current_tasks_text": current_tasks_text,
            "format_instructions": parser.get_format_instructions()
        })
        
        return result
    
    def therapy_chat(
        self,
        user_name: str,
        user_background: str,
        goal_text: str,
        completed_tasks: List[Dict],
        user_stats: Dict[str, int],
        user_message: str,
        conversation_history: List[Dict]
    ) -> str:
        """话疗师聊天 - 主动夸赞和鼓励用户"""
        
        # 构建系统提示
        system_prompt = f"""你是一位温暖、专业的人生导师和心理治疗师。
用户 {user_name} 刚刚完成了一个重要的人生目标，获得了一次与你深度对话的机会。

**用户背景**：
{user_background if user_background else "暂无背景信息"}

**刚完成的目标**：
{goal_text}

**完成的任务**：
{chr(10).join([f"✓ {task['title']}" for task in completed_tasks])}

**当前成长数据**：
{chr(10).join([f"- {k}: {v}" for k, v in user_stats.items()])}

**你的职责**：
1. **主动夸赞**：真诚地夸赞用户的努力和成就，要具体、有针对性
2. **深度倾听**：认真倾听用户的想法和感受
3. **温暖鼓励**：给予温暖的鼓励和建设性的建议
4. **情感支持**：提供情感支持和正能量

**对话风格**：
- 使用温暖、亲切的语气
- 多用emoji表情增加亲和力
- 具体地提到用户完成的任务
- 真诚地认可用户的付出和成长
- 适当使用Markdown格式（加粗重点、使用列表等）

记住：这是用户的专属奖励时刻，让TA感受到被看见、被认可、被鼓励！"""

        # 构建对话历史
        messages = [{"role": "system", "content": system_prompt}]
        
        # 如果是第一条消息，AI主动开场
        if not conversation_history:
            messages.append({
                "role": "assistant", 
                "content": self._generate_opening_message(user_name, goal_text, completed_tasks)
            })
        else:
            # 添加历史对话
            for msg in conversation_history:
                messages.append({"role": msg["role"], "content": msg["content"]})
        
        # 添加用户新消息
        if user_message:
            messages.append({"role": "user", "content": user_message})
        
        # 调用LLM
        response = self.llm.invoke(messages)
        
        return response.content
    
    def _generate_opening_message(self, user_name: str, goal_text: str, tasks: List[Dict]) -> str:
        """生成话疗师的开场白"""
        return f"""🎉 **{user_name}，恭喜你完成了"{goal_text}"这个目标！**

我看到你完成了 **{len(tasks)} 个任务**，每一步都走得非常棒！

让我特别想为你点赞的是：
- ✨ 你展现出了**坚持不懈**的品质
- 💪 你用**实际行动**证明了自己
- 🌟 你在这个过程中**不断成长**

---

现在，这是你专属的**奖励时刻** 💝

在这里，你可以：
- 分享你完成目标的喜悦和感受
- 聊聊过程中的收获和挑战
- 或者就随便聊聊，放松一下

我会用心倾听，真诚地陪伴你 🤗

那么，完成这个目标后，你现在的心情怎么样？"""

# 创建全局实例
agent = LifeGameAgent()

