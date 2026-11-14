import os
import chromadb
import gradio as gr
import ollama

VECTOR_DB_DIR = "vector_db"
# LLM_MODEL = "llama3.2"  # 建議改用中文支援度高的模型，如 qwen2.5
LLM_MODEL = "qwen2.5:7b"  # 建議改用中文支援度高的模型，如 qwen2.5
chroma_client = chromadb.PersistentClient(path=VECTOR_DB_DIR)
collection = chroma_client.get_collection(name="multi_manual_rag")

def rag_pipeline(user_query):
    if not user_query.strip():
        return "⚠️ 請輸入有效的查詢問題。", [], ""

    # 檢索 Top-3 最相關手冊區塊
    results = collection.query(
        query_texts=[user_query],
        n_results=3
    )

    retrieved_docs = results["documents"][0]
    retrieved_metadatas = results["metadatas"][0]
    
    context = "\n\n====================\n\n".join(retrieved_docs)
    
    # 提取對應的圖檔路徑
    matched_images = []
    for meta in retrieved_metadatas:
        images_str = meta.get("images", "")
        if images_str:
            paths = images_str.split(",")
            for img_path in paths:
                img_path = img_path.strip()
                if os.path.exists(img_path) and img_path not in matched_images:
                    matched_images.append(img_path)

    system_prompt = (
        "你是一位專業的發電機維修與保養專家。"
        "請根據下方提供的參考資料（包含多份技術手冊內文、表格與插圖說明）回答問題。"
        "解答時請列出明確步驟、具體數據或對照表格內容，並註明資料來自哪一份手冊。"
    )
    
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"【參考資料】:\n{context}\n\n【使用者問題】: {user_query}"}
        ]
    )
    
    ai_answer = response["message"]["content"]
    return ai_answer, matched_images, context

# 建立 Gradio Web 介面
with gr.Blocks(title="多手冊發電機 AI 智慧助手", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🛠️ 多冊發電機技術資料 AI 離線檢索系統")
    gr.Markdown("系統已整合柴油引擎發電機基本介紹、安裝施工說明書與發電機規格表。")
    
    with gr.Row():
        with gr.Column(scale=1):
            query_input = gr.Textbox(
                label="請輸入您的問題",
                placeholder="例如：發電機低電壓的可能原因有哪些？或 ELG184E 的效率是多少？",
                lines=4
            )
            with gr.Row():
                submit_btn = gr.Button("🔍 檢索與解答", variant="primary")
                clear_btn = gr.Button("🧹 清除")
                
        with gr.Column(scale=2):
            answer_output = gr.Markdown(label="AI 專家解答", value="*等待查詢中...*")
            
            gr.Markdown("### 📸 關聯手冊插圖預覽")
            gallery_output = gr.Gallery(
                label="對應圖檔",
                show_label=False,
                columns=3,
                height=320,
                object_fit="contain"
            )
            
            with gr.Accordion("🔍 查看檢索到的手冊內文與表格 (RAG Context)", open=False):
                context_output = gr.Markdown()

    submit_btn.click(
        fn=rag_pipeline,
        inputs=[query_input],
        outputs=[answer_output, gallery_output, context_output]
    )
    
    clear_btn.click(
        fn=lambda: ("", "*等待查詢中...*", [], ""),
        inputs=[],
        outputs=[query_input, answer_output, gallery_output, context_output]
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)