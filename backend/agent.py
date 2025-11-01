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

class GameResponse(BaseModel):
    story: str = Field(description="根据用户目标生成的游戏化故事背景")
    tasks: List[TaskItem] = Field(description="拆解后的任务列表，3-8个任务")
    stats: Dict[str, int] = Field(description="初始数值系统，如：{'等级': 1, '经验值': 0, '金币': 0, '成就点': 0}")

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

3. **设计数值系统**：创建一个简单的数值系统来追踪进度，包含 3-5 个数值类型，如：
   - 等级（初始为 1）
   - 经验值（初始为 0）
   - 金币、成就点、技能点等（根据目标类型自定义）
   - 所有初始值都设为 0（等级除外）

返回格式示例：
{{
  "story": "在像素王国中，你是被选中的勇者...",
  "tasks": [
    {{
      "title": "【任务一】具体的任务标题",
      "description": "详细的任务描述，说明具体要做什么",
      "estimated_time": "30分钟"
    }},
    {{
      "title": "【任务二】具体的任务标题",
      "description": "详细的任务描述",
      "estimated_time": "1小时"
    }}
  ],
  "stats": {{
    "等级": 1,
    "经验值": 0,
    "金币": 0,
    "成就点": 0
  }}
}}

{format_instructions}

⚠️ 重要提示：
1. 每个任务必须包含 title、description 和 estimated_time 三个字段
2. 必须包含顶层的 stats 字段
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
    
    def calculate_rewards(self, task_title: str, current_stats: Dict[str, int]) -> Dict[str, int]:
        """计算任务完成后的奖励"""
        rewards = {}
        
        # 基础奖励
        if "经验值" in current_stats:
            rewards["经验值"] = 20
        
        if "金币" in current_stats:
            rewards["金币"] = 10
            
        if "成就点" in current_stats:
            rewards["成就点"] = 5
        
        # 等级提升判断
        if "等级" in current_stats and "经验值" in current_stats:
            new_exp = current_stats["经验值"] + rewards.get("经验值", 0)
            current_level = current_stats["等级"]
            exp_needed = current_level * 100  # 每级需要 level * 100 经验
            
            if new_exp >= exp_needed:
                rewards["等级"] = 1
                rewards["经验值"] = new_exp - exp_needed  # 重置经验值（溢出的保留）
        
        return rewards

# 创建全局实例
agent = LifeGameAgent()

