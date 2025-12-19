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

# False: 智能模式（只翻译新文章或被修改过的文章）
# True:  暴力模式（无视时间，全部重译）
FORCE_UPDATE = False 

def translate_text(text, target_lang="English", is_short_text=False):  
    system_prompt_long = f"""
    You are a professional technical translator specialized in SRE, Kubernetes, and Cloud Native.
    Translate the Markdown content from Chinese to {target_lang}.
    Rules:
    1. Keep all Markdown formatting exactly as is.
    2. Do NOT translate code blocks, commands, or technical terms that should remain in English.
    3. Only output the translated content.
    """

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
            return response.choices[0].message.content.strip() 
            
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

    # 🔥 修改点：智能增量更新逻辑
    if os.path.exists(target_file):
        if FORCE_UPDATE:
            print(f"🔨 强制重译模式: {base_name}")
        else:
            # 获取最后修改时间
            source_mtime = os.path.getmtime(file_path)
            target_mtime = os.path.getmtime(target_file)
            
            # 如果中文源文件的时间 早于 英文目标文件，说明英文已经是新的了
            if source_mtime < target_mtime:
                print(f"⏭️  跳过 (无更新): {base_name}")
                return
            else:
                print(f"📝 检测到原文更新，正在重译: {base_name} ...")
    else:
        print(f"🆕 发现新文章，正在翻译: {base_name} ...")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        # 1. 翻译 Title
        if post.metadata.get('title'):
            res = translate_text(post.metadata['title'], is_short_text=True)
            if res: post.metadata['title'] = res
            
        # 2. 翻译 Description
        if post.metadata.get('description'):
            res = translate_text(post.metadata['description'], is_short_text=True)
            if res: post.metadata['description'] = res

        # 3. 翻译 Categories
        if post.metadata.get('categories'):
            new_cats = []
            for cat in post.metadata['categories']:
                trans_cat = translate_text(cat, is_short_text=True)
                new_cats.append(trans_cat if trans_cat else cat)
            post.metadata['categories'] = new_cats

        # 4. 翻译 Tags
        if post.metadata.get('tags'):
            new_tags = []
            for tag in post.metadata['tags']:
                trans_tag = translate_text(tag, is_short_text=True)
                new_tags.append(trans_tag if trans_tag else tag)
            post.metadata['tags'] = new_tags
        
        # 5. 翻译正文
        translated_content = translate_text(post.content)
        if translated_content:
            post.content = translated_content
        
        # 保存文件
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(frontmatter.dumps(post))
        
        print(f"✅ 完成: {target_file}")
        
    except Exception as e:
        print(f"❌ 失败 {file_path}: {e}")
    
    # 稍微休息一下，避免并发过高（虽然 GLM-4-Flash 很快）
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

    mode_str = "强制覆盖" if FORCE_UPDATE else "智能增量"
    print(f"🚀 开始任务 (模式: {mode_str})...")
    
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if (file.endswith(".md") and not file.endswith(".en.md")):
                if file == "_index.md": continue
                full_path = os.path.join(root, file)
                process_file(full_path)

if __name__ == "__main__":
    main()