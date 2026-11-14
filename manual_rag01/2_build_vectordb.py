import json
import os
import chromadb

JSON_INPUT = "data/captions_metadata.json"
VECTOR_DB_DIR = "vector_db"

chroma_client = chromadb.PersistentClient(path=VECTOR_DB_DIR)
# 若資料庫已存在則重新取得
collection = chroma_client.get_or_create_collection(name="multi_manual_rag")

with open(JSON_INPUT, "r", encoding="utf-8") as f:
    parsed_pages = json.load(f)

for idx, item in enumerate(parsed_pages):
    source_doc = item["source_doc"]
    page_num = item["page_number"]
    content = item["content"]
    
    img_descriptions = []
    image_paths_list = []
    
    for img in item["images"]:
        final_caption = img["manual_caption"].strip() if img["manual_caption"].strip() else img["auto_caption"]
        img_descriptions.append(
            f"\n[手冊插圖: {img['image_path']}]\n插圖詳細說明：{final_caption}"
        )
        image_paths_list.append(img["image_path"])

    # 組合該 Block 文本 (來源 + 文字 + 結構化表格 + 圖片說明)
    full_chunk_text = (
        f"【來源檔案】: {source_doc}\n"
        f"【頁數】: 第 {page_num} 頁\n"
        f"{content}\n" +
        "\n".join(img_descriptions)
    )
    
    collection.add(
        documents=[full_chunk_text],
        metadatas=[{
            "source_doc": source_doc,
            "page": page_num,
            "images": ",".join(image_paths_list)
        }],
        ids=[f"doc_{idx}_p{page_num}"]
    )

print(f"✅ 向量庫建立完成！實體檔案儲存於: {VECTOR_DB_DIR}")