import os
import frontmatter
from openai import OpenAI
import time
import random

# === 配置 ===
API_KEY = os.getenv("ZHIPU_API_KEY") 

if not API_KEY:
    raise ValueError("请设置环境变量 ZHIPU_API_KEY")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

MODEL_NAME = "glm-4-flash"

def translate_text(text, target_lang="English", is_short_text=False):  
    # 针对正文的 Prompt
    system_prompt_long = f"""
    You are a professional technical translator specialized in SRE, Kubernetes, and Cloud Native.
    Translate the Markdown content from Chinese to {target_lang}.
    Rules:
    1. Keep all Markdown formatting exactly as is.
    2. Do NOT translate code blocks, commands, or technical terms that should remain in English.
    3. Only output the translated content.
    """

    # 针对标题/分类的 Prompt (更严格)
    system_prompt_short = f"""
    Translate the following text to {target_lang} concisely.
    Rules:
    1. DIRECT TRANSLATION ONLY. Do not interpret, extend, or explain.
    2. Do not add words that are not in the source text.
    3. Remove any trailing punctuation like periods.
    """
    
    prompt = system_prompt_short if is_short_text else system_prompt_long
    
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.1,
                top_p=0.7,
                max_tokens=4095
            )
            return response.choices[0].message.content.strip() # 去除首尾空格
            
        except Exception as e:
            print(f"⚠️ 翻译出错: {e}")
            time.sleep(2)
            continue
    return None

def process_file(file_path):
    dir_name = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    
    if base_name.endswith(".en.md"): return 
    
    # 确定目标文件名
    if base_name == "index.md" or base_name == "index.zh-cn.md":
        target_file = os.path.join(dir_name, "index.en.md")
    else:
        name_part = base_name.replace(".zh-cn.md", "").replace(".md", "")
        target_file = os.path.join(dir_name, f"{name_part}.en.md")

    if os.path.exists(target_file):
        print(f"⏭️  跳过: {target_file}")
        return
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        # 1. 翻译 Title (开启短文本模式，防止延伸)
        if post.metadata.get('title'):
            res = translate_text(post.metadata['title'], is_short_text=True)
            if res: post.metadata['title'] = res
            
        if post.metadata.get('description'):
            res = translate_text(post.metadata['description'], is_short_text=True)
            if res: post.metadata['description'] = res

        if post.metadata.get('categories'):
            new_cats = []
            for cat in post.metadata['categories']:
                trans_cat = translate_text(cat, is_short_text=True)
                if trans_cat:
                    new_cats.append(trans_cat)
                else:
                    new_cats.append(cat)
            post.metadata['categories'] = new_cats
            print(f"   └─ Categories: {new_cats}")

        if post.metadata.get('tags'):
            new_tags = []
            for tag in post.metadata['tags']:
                trans_tag = translate_text(tag, is_short_text=True)
                if trans_tag:
                    new_tags.append(trans_tag)
                else:
                    new_tags.append(tag)
            post.metadata['tags'] = new_tags
        
        translated_content = translate_text(post.content)
        if translated_content:
            post.content = translated_content
        
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))
        
        print(f"✅ 完成: {target_file}")
        
    except Exception as e:
        print(f"❌ 失败 {file_path}: {e}")
    
    time.sleep(1)

def main():
    # 自动寻找 content 目录
    possible_paths = ["content", "../content", "./blog-hugo/content"]
    content_dir = None
    for p in possible_paths:
        if os.path.exists(p):
            content_dir = p
            break
            
    if not content_dir:
        print("❌ 找不到 content 目录")
        return

    print(f"🚀 开始全量重译...")
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if (file.endswith(".md") and not file.endswith(".en.md")):
                if file == "_index.md": continue
                full_path = os.path.join(root, file)
                process_file(full_path)

if __name__ == "__main__":
    main()