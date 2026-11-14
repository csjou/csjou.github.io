# pip install "PyMuPDF>=1.23.0"
# python -m pip install ollama
# pip install tabulate
import fitz  # PyMuPDF (需要 PyMuPDF >= 1.23.0 支援 find_tables)
import os
import json
import ollama

RAW_PDF_DIR = "data/raw_pdf"
IMAGE_DIR = "data/extracted_images"
JSON_OUTPUT = "data/captions_metadata.json"

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(os.path.dirname(JSON_OUTPUT), exist_ok=True)

all_parsed_data = []

pdf_files = [f for f in os.listdir(RAW_PDF_DIR) if f.endswith('.pdf')]

for pdf_file in pdf_files:
    pdf_path = os.path.join(RAW_PDF_DIR, pdf_file)
    doc_prefix = os.path.splitext(pdf_file)[0]
    print(f"\n📄 正在解析手冊: {pdf_file} ...")
    
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # 1. 表格特別處理：提取表格並轉為 Markdown 格式
        tables = page.find_tables()
        table_markdowns = []
        if tables.tables:
            for tab in tables.tables:
                df = tab.to_pandas()
                table_md = df.to_markdown(index=False)
                table_markdowns.append(f"\n【頁面表格內容】:\n{table_md}\n")
        
        page_text = page.get_text("text")
        full_page_content = page_text + "\n".join(table_markdowns)
        
        # 2. 圖片處理與 Ollama VLM 語意標註
        image_list = page.get_images(full=True)
        image_metadata = []
        
        for img_index, img_info in enumerate(image_list):
            xref = img_info[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # 加入檔名前綴避免檔名衝突
            img_filename = f"{doc_prefix}_p{page_num+1}_img{img_index+1}.{image_ext}"
            img_filepath = os.path.join(IMAGE_DIR, img_filename)
            
            with open(img_filepath, "wb") as f:
                f.write(image_bytes)
                
            print(f"  └─ [第 {page_num+1} 頁] 分析插圖: {img_filename}...")
            
            # 呼叫 VLM 描述圖片
            try:
                vlm_res = ollama.chat(
                    model="qwen2-vl",
                    messages=[{
                        "role": "user",
                        "content": "請詳細說明這張手冊插圖中的：零件名稱、標號、動作指示與注意事項。",
                        "images": [img_filepath]
                    }]
                )
                auto_caption = vlm_res["message"]["content"]
            except Exception as e:
                auto_caption = f"圖片解析失敗: {str(e)}"
            
            image_metadata.append({
                "image_path": img_filepath,
                "filename": img_filename,
                "auto_caption": auto_caption,
                "manual_caption": ""  # 預留人工校對欄位
            })

        all_parsed_data.append({
            "source_doc": pdf_file,
            "page_number": page_num + 1,
            "content": full_page_content,
            "images": image_metadata
        })

# 導出 JSON 中間檔
with open(JSON_OUTPUT, "w", encoding="utf-8") as f:
    json.dump(all_parsed_data, f, ensure_ascii=False, indent=2)

print(f"\n✅ 3 份手冊解析完成！中間檔已儲存至: {JSON_OUTPUT}")