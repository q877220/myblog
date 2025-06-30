import os
import subprocess
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

def commit_post(file_path):
    try:
        subprocess.run(["git", "add", file_path], check=True)
        subprocess.run(["git", "commit", "-m", f"自动发布文章: {file_path}"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git提交失败: {e}")
        return False

def push_post():
    try:
        # 推送到GitHub
        subprocess.run(["git", "push", "origin", "master:gh-pages"], check=True)
        
        # 部署到Vercel
        vercel_result = subprocess.run(["vercel", "--prod"], 
                                     capture_output=True, 
                                     text=True)
        if vercel_result.returncode == 0:
            print("Vercel部署成功!")
            print(vercel_result.stdout)
        else:
            print("Vercel部署失败:")
            print(vercel_result.stderr)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git推送失败: {e}")
        return False

def save_post(content):
    today = datetime.now().strftime("%Y-%m-%d")
    file_path = f"content/posts/{today}-auto-post.md"
    front_matter = f"---\ntitle: 'AI每日热点 - {today}'\ndate: {datetime.now().isoformat()}\ntags: [AI, 技术趋势]\n---\n\n"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(front_matter + content)
    return file_path

if __name__ == "__main__":
    try:
        post_content = generate_hot_post()
        post_path = save_post(post_content)
        if commit_post(post_path):
            if push_post():
                print("文章已自动发布并部署成功！")
            else:
                print("文章已提交但推送失败，请手动推送")
        else:
            print("文章保存成功但提交失败")
    except Exception as e:
        print(f"自动发布失败: {e}")