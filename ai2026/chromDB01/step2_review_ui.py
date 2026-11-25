import gradio as gr
import json
import os

INPUT_FILE = "recipes_chunked.json"
OUTPUT_FILE = "recipes_reviewed.json"

# 初始化資料
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        recipes_data = json.load(f)
else:
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        recipes_data = json.load(f)

def get_recipe_by_index(idx):
    idx = int(idx)
    if 0 <= idx < len(recipes_data):
        item = recipes_data[idx]
        return item['id'], item['title'], item['content'], f"目前第 {idx + 1} / {len(recipes_data)} 筆"
    return "", "", "", "索引超出範圍！"

def save_current_recipe(idx, updated_content):
    idx = int(idx)
    if 0 <= idx < len(recipes_data):
        recipes_data[idx]['content'] = updated_content.strip()
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(recipes_data, f, ensure_ascii=False, indent=2)
        return f"第 {idx + 1} 筆（{recipes_data[idx]['title']}）已成功儲存至 {OUTPUT_FILE}！"
    return "儲存失敗，索引錯誤。"

def nav_recipe(current_idx, step):
    new_idx = max(0, min(len(recipes_data) - 1, int(current_idx) + step))
    r_id, title, content, status = get_recipe_by_index(new_idx)
    return new_idx, r_id, title, content, status

with gr.Blocks(title="食譜 RAG 檢核系統") as demo:
    gr.Markdown("# 食譜 Chunk 人工檢核與修改介面")
    
    with gr.Row():
        idx_input = gr.Number(value=0, label="食譜索引號 (從 0 開始)", precision=0)
        status_box = gr.Textbox(label="當前狀態", interactive=False)

    recipe_id_box = gr.Textbox(label="食譜 ID", interactive=False)
    title_box = gr.Textbox(label="食譜名稱", interactive=False)
    content_box = gr.TextArea(label="食譜 Chunk 完整內容 (包含【用料】/【備菜】/【做菜】可直接修改)", lines=12)

    with gr.Row():
        prev_btn = gr.Button("◀ 上一筆")
        next_btn = gr.Button("下一筆 ▶")
        save_btn = gr.Button("儲存變更", variant="primary")

    msg_box = gr.Textbox(label="系統訊息", interactive=False)

    # 事件綁定
    idx_input.change(get_recipe_by_index, inputs=[idx_input], outputs=[recipe_id_box, title_box, content_box, status_box])
    prev_btn.click(nav_recipe, inputs=[idx_input, gr.State(-1)], outputs=[idx_input, recipe_id_box, title_box, content_box, status_box])
    next_btn.click(nav_recipe, inputs=[idx_input, gr.State(1)], outputs=[idx_input, recipe_id_box, title_box, content_box, status_box])
    save_btn.click(save_current_recipe, inputs=[idx_input, content_box], outputs=[msg_box])

if __name__ == "__main__":
    #demo.launch(server_name="127.0.0.1", port=7860)
    demo.launch(server_name="127.0.0.1", server_port=7860)