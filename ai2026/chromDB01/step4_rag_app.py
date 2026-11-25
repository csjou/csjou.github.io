import chromadb
from chromadb.utils import embedding_functions
import requests

# 1. 載入 ChromaDB 資料庫與向量模型
client = chromadb.PersistentClient(path="./chroma_db")
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="shibing624/text2vec-base-chinese"
)
collection = client.get_collection(
    name="recipe_knowledge_base", 
    embedding_function=emb_fn
)

def retrieve_context(query, top_k=3):
    """進行向量相似度檢索"""
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    retrieved_docs = results['documents'][0]
    return "\n\n--------------------\n\n".join(retrieved_docs)

def query_ollama(query, context, model_name="qwen2.5:7b"):
    """發送請求給本地 Ollama"""
    prompt = f"""你是一位專業的私房菜烹飪專家與廚藝顧問。請根據以下提供的檢索資料，準確、條理清晰地回答使用者的問題。如果檢索資料中沒有提到解答，請明確說明。

【參考食譜資料】：
{context}

【使用者問題】：
{query}

【廚藝專家解答】："""

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json().get('response', '')
    else:
        return f"Ollama 呼叫失敗，狀態碼：{response.status_code}"

def main():
    print("============================================")
    print("   🍳 離線 AI 食譜專家 RAG 系統 (輸入 q 結束)  ")
    print("============================================")
    
    while True:
        user_query = input("\n請輸入烹飪問題或想查詢的食材（例如：馬鈴薯要怎麼做？或 5分鐘內能完成的菜）：")
        if user_query.strip().lower() == 'q':
            print("感謝使用，系統已關閉！")
            break
        
        print("\n🔍 正在檢索知識庫...")
        context = retrieve_context(user_query, top_k=3)
        
        print("🤖 AI 專家思考中...")
        answer = query_ollama(user_query, context)
        
        print("\n" + "="*40)
        print(answer)
        print("="*40)

if __name__ == "__main__":
    main()