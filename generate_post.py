import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()
import openai
from openai import OpenAI
from datetime import datetime

# 配置OpenAI API密钥
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_hot_post():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一个资深技术博客作者"},
            {"role": "user", "content": "请生成一篇关于人工智能最新进展的技术文章，要求包含3个主要技术点"}
        ]
    )
    return response.choices[0].message.content

def save_post(content):
    today = datetime.now().strftime("%Y-%m-%d")
    file_path = f"content/posts/{today}-auto-post.md"
    front_matter = f"---\ntitle: 'AI每日热点 - {today}'\ndate: {datetime.now().isoformat()}\ntags: [AI, 技术趋势]\n---\n\n"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(front_matter + content)

if __name__ == "__main__":
    post_content = generate_hot_post()
    save_post(post_content)