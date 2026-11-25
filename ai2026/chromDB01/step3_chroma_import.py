import json
import chromadb
from chromadb.utils import embedding_functions

def import_to_chromadb(json_file="recipes_reviewed.json", db_path="./chroma_db"):
    # 讀取人工審核後的食譜 JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        recipes = json.load(f)

    # 建立持久化 ChromaDB 客戶端
    client = chromadb.PersistentClient(path=db_path)

    # 使用適合中文語意理解的向量模型
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="shibing624/text2vec-base-chinese"
    )

    # 建立或取得 Collection
    collection = client.get_or_create_collection(
        name="recipe_knowledge_base",
        embedding_function=emb_fn,
        metadata={"hnsw:space": "cosine"}
    )

    ids = [r['id'] for r in recipes]
    documents = [r['content'] for r in recipes]
    metadatas = [{"title": r['title']} for r in recipes]

    # 批次寫入資料庫
    batch_size = 50
    for i in range(0, len(recipes), batch_size):
        collection.add(
            ids=ids[i:i+batch_size],
            documents=documents[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size]
        )

    print(f"成功將 {len(recipes)} 筆食譜向量化寫入 ChromaDB（資料庫路徑：{db_path}）！")

if __name__ == "__main__":
    import_to_chromadb()