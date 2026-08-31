# ============================================
# 範例5：Web應用程式 - 學生API服務 (Flask)
# 檔案名：app.py
# ============================================

from flask import Flask, jsonify, request, render_template_string
import json

app = Flask(__name__)  # 建立 Flask 應用（對比 C# 的 WebApplication.CreateBuilder）
# ========== 中文 ==========
app.json.ensure_ascii = False  # JSON 不使用 ASCII 編碼（對比 C# 的 JsonSerializerOptions）
# 模擬資料庫
students_db = [
    {"id": "S001", "name": "王小明", "age": 20, "scores": [85, 92, 78]},
    {"id": "S002", "name": "李小華", "age": 19, "scores": [92, 88, 95]},
    {"id": "S003", "name": "張大偉", "age": 21, "scores": [78, 85, 80]},
]

# ========== API 路由 ==========

@app.route("/")  # 根路徑（對比 C# 的 [Route]）
def home():
    """首頁 - 回傳簡單HTML"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>學生API系統</title>
        <style>
            body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #333; }
            .endpoint { background: #f0f0f0; padding: 10px; margin: 10px 0; border-radius: 5px; }
            code { background: #e0e0e0; padding: 2px 5px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>🎓 學生API系統</h1>
        <p>這是一個用 Python Flask 建立的簡易 API 服務</p>
        
        <h2>可用端點：</h2>
        <div class="endpoint">
            <strong>GET</strong> <code>/api/students</code> - 取得所有學生
        </div>
        <div class="endpoint">
            <strong>GET</strong> <code>/api/students/&lt;id&gt;</code> - 取得特定學生
        </div>
        <div class="endpoint">
            <strong>POST</strong> <code>/api/students</code> - 新增學生
        </div>
        <div class="endpoint">
            <strong>GET</strong> <code>/api/students/top/&lt;n&gt;</code> - 取得前N名
        </div>
    </body>
    </html>
    """
    return html


@app.route("/api/students", methods=["GET"])  # 對比 C# 的 [HttpGet]
def get_all_students():
    """取得所有學生（對比 C# 的 IActionResult）"""
    return jsonify({
        "count": len(students_db),
        "students": students_db
    })


@app.route("/api/students/<student_id>", methods=["GET"])
def get_student(student_id):
    """取得特定學生（對比 C# 的路由參數）"""
    # 使用 List Comprehension + next 尋找
    student = next((s for s in students_db if s["id"] == student_id), None)
    
    if student:
        # 計算平均
        avg = sum(student["scores"]) / len(student["scores"]) if student["scores"] else 0
        result = {**student, "average": round(avg, 1)}  # 解包字典並新增欄位
        return jsonify(result)
    else:
        return jsonify({"error": "找不到學生"}), 404  # HTTP 404


@app.route("/api/students", methods=["POST"])
def create_student():
    """新增學生（對比 C# 的 [HttpPost]）"""
    # 取得 JSON 請求內容（對比 C# 的 [FromBody]）
    data = request.get_json()
    
    # 簡單驗證
    if not data or "name" not in data or "id" not in data:
        return jsonify({"error": "缺少必要欄位"}), 400
    
    # 檢查是否已存在
    if any(s["id"] == data["id"] for s in students_db):
        return jsonify({"error": "學號已存在"}), 409
    
    new_student = {
        "id": data["id"],
        "name": data["name"],
        "age": data.get("age", 18),
        "scores": data.get("scores", [])
    }
    students_db.append(new_student)
    
    return jsonify(new_student), 201  # HTTP 201 Created


@app.route("/api/students/top/<int:n>", methods=["GET"])
def get_top_students(n):
    """取得前N名學生（使用 Lambda 排序）"""
    # 計算平均並排序（對比 C# 的 OrderByDescending）
    ranked = sorted(
        students_db,
        key=lambda s: sum(s["scores"]) / len(s["scores"]) if s["scores"] else 0,
        reverse=True
    )[:n]
    
    return jsonify({
        "top": n,
        "students": ranked
    })


# 錯誤處理（對比 C# 的 Middleware）
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "找不到頁面"}), 404


# 啟動伺服器（對比 C# 的 app.Run()）
if __name__ == "__main__":
    print("🚀 啟動伺服器於 http://localhost:5000")
    app.run(debug=True, port=5000)