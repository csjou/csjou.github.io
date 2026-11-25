## 建構離線食譜 RAG（檢索增強生成）
### 專家系統主要包含四大模組：
#### 文字解析與結構化分段 (Chunking)、Web/GUI 人工檢核介面、向量化與 ChromaDB 數據庫匯入，以及Ollama 本地大語言模型整合。

建議統一採用 Python 技術棧（結合 Gradio UI、ChromaDB、Sentence-Transformers 與 Ollama），系統建構流暢且易於離線部署。

環境套件準備
執行前請先開啟終端機安裝必要套件：
pip install chromadb gradio sentence-transformers requests

同時請至 Ollama 官網 下載並安裝 Ollama，執行以下指令下載適合中文且適合食譜問答的模型（例如 Qwen 2.5）：

#### 步驟 1：文字讀取與結構化 Chunking 程式 (step1_chunking.py)
由於食譜資料本身具備明確的4個欄位結構（【食譜】:、【用料】:、【備菜步驟】:、【做菜步驟】:），最佳的 Chunking 策略是以「完整單一食譜」作為基本 Chunk 單元，確保食材與步驟不會被中途截斷。

#### 步驟 2：人工檢核與修改 GUI 介面 (step2_review_ui.py)
使用 Gradio 打造網頁版檢核介面，可逐筆檢視、編輯 460 筆切分好的食譜，並存檔為 recipes_reviewed.json。

#### 步驟 3：Embedding 向量化與 ChromaDB 匯入 (step3_chroma_import.py)
使用專為中文優化的 Embedding 模型（如 shibing624/text2vec-base-chinese 或 BAAI/bge-small-zh-v1.5）將審核後的食譜向量化存入本地 ChromaDB。

#### 步驟 4：Ollama + ChromaDB 互動式離線 RAG 專家系統 (step4_rag_app.py)
結合前述向量庫檢索與本地 Ollama API，提供終端機互動介面（亦可擴充為 Web UI）。

### 系統操作流程說明
分段：執行 python step1_chunking.py，系統讀取 menu.txt 並生成 recipes_chunked.json。

檢核：執行 python step2_review_ui.py，開啟瀏覽器造訪 [http://127.0.0.1:7860](http://127.0.0.1:7860) 進行逐筆檢查與編修，修改完成後點擊「儲存變更」，生成 recipes_reviewed.json。

建庫：執行 python step3_chroma_import.py，模型自動將 JSON 文字轉為向量並寫入 ./chroma_db。

問答：確定 Ollama 已啟動，執行 python step4_rag_app.py 即可開始進行離線 AI 食譜問答與建議。

