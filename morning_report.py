import os
import requests
from openai import OpenAI

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
WEWORK_WEBHOOK = os.environ["WEWORK_WEBHOOK"]

client = OpenAI(api_key=OPENAI_API_KEY)

prompt = """
你是一个服务于信息流广告剪辑师的AI晨报助手。

请生成今天的中文晨报，内容必须实用、简洁、可行动。

晨报结构：

# 今日信息流广告AI晨报

## 1. AI要闻
筛选最近24-48小时内，和以下方向有关的AI新闻：
AI视频、AI图片、AI剪辑、AI配音、数字人、AI Agent、广告创意工具、自动化工作流。

每条格式：
- 【标题】
  发生了什么：
  对广告剪辑师的影响：
  建议动作：

## 2. 平台政策
重点关注：
抖音/巨量引擎、快手磁力引擎、小红书聚光、微信广告、视频号、TikTok、Meta Ads。

每条格式：
- 【平台】
  政策/规则变化：
  对素材剪辑或投放的影响：
  建议注意：

## 3. GitHub热门项目
关注：
AI视频、图片生成、自动剪辑、字幕、配音、数字人、广告素材分析、自动化工作流。

每条格式：
- 【项目名】
  项目用途：
  适合广告剪辑师怎么用：

## 今日建议
用一句话告诉我，今天最值得关注或尝试的一件事。

要求：
- 不要写空话
- 不要堆砌新闻
- 优先选择和信息流广告剪辑工作相关的内容
- 每部分3-5条
- 输出适合企业微信 markdown 的格式
"""

response = client.responses.create(
    model="gpt-4.1-mini",
    tools=[{"type": "web_search_preview"}],
    input=prompt
)

report = response.output_text

payload = {
    "msgtype": "markdown",
    "markdown": {
        "content": report
    }
}

r = requests.post(WEWORK_WEBHOOK, json=payload, timeout=30)
r.raise_for_status()

print("晨报已发送")
