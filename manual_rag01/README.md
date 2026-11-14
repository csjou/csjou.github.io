
my_manual_rag/
├── data/
│   ├── raw_pdf/
│   │   └── repair_manual.pdf        [開發階段] 原始 PDF 檔
│   ├── extracted_images/            [必須] 實體圖檔資料夾（App 需提供圖片預覽/存取）
│   └── captions_metadata.json       [開發階段] 圖片說明中間檔（供人工檢視與修訂）
├── vector_db/                       [必須] 建立好的 ChromaDB 向量資料庫實體目錄
├── 1_extract_and_caption.py         [開發階段] 步驟一腳本：PDF解析與VLM標註
├── 2_build_vectordb.py              [開發階段] 步驟二腳本：讀取中間檔並建立向量庫
└── 3_rag_app.py                     [必須] 步驟三：最終執行的 RAG AI 主程式 App
部署與執行 AI-App (3_rag_app.py) 必需元素
當開發完成並要正式運作 AI-App 時，不需要 重新執行 PDF 解析或 VLM 圖片標註，最小執行環境僅需以下元素：
3_rag_app.py：應用程式主程式。
vector_db/：已將「文字 + 圖片描述」索引化的向量資料庫。
data/extracted_images/：抽出的實體圖檔資料夾（供 App 輸出圖片實體路徑/預覽）。
Ollama 運行環境：後端已啟動 ollama serve 並載入文字語言模型（如 llama3.2 或 qwen2.5）。