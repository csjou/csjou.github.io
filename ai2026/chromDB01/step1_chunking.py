# conda create -n recipe_rag python=3.10 -y
# conda activate recipe_rag
# pip install chromadb gradio sentence-transformers requests
# ollama pull qwen2.5:7b 下載前先安裝 ollama Download ollamaSetup.exe 執行自動到位置
import re
import json

def parse_and_chunk_menu(file_path="menu.txt", output_json="recipes_chunked.json"):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 使用正則表達式依據【食譜】:進行切分
    raw_recipes = re.split(r'(?=\n?【食譜】:)', content)
    chunks = []

    for idx, raw in enumerate(raw_recipes):
        raw_text = raw.strip()
        if not raw_text or '【食譜】:' not in raw_text:
            continue
        
        # 提取食譜名稱
        title_match = re.search(r'【食譜】:\s*(.*?)(?=\s*\||\n|【用料】:)', raw_text)
        title = title_match.group(1).strip() if title_match else f"未命名食譜_{idx+1}"

        chunks.append({
            "id": f"recipe_{idx+1:04d}",
            "title": title,
            "content": raw_text
        })

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"解析完成！共處理 {len(chunks)} 筆食譜 Chunk，已儲存至 {output_json}。")

if __name__ == "__main__":
    parse_and_chunk_menu()