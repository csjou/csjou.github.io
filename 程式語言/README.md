# Mimi k3
## wk01 C#
## 3 個核心方向，我來幫你補成 5 個循序漸進的範例，讓學生從「完全看不懂」到「能寫出結構化程式」：
### wk0101
教學重點：
 • namespace 像「資料夾」，class 像「文件」
 • static void Main() 是唯一的程式入口
 • C# 是強型別語言，每個變數都要宣告型別
#### csc wk0101.cs
#### .\wk0101.exe     Powershell
### wk0102
教學重點：
 • class Student 是藍圖，new Student(...) 是蓋房子
 • public 是存取修飾詞，控制誰能看到這個成員
 • 建構子讓物件「一出生就有初始值」
### wk0103
教學重點：
 • Lambda：p => p.Price > 100 讀作「對於每個 p，回傳 p.Price 是否大於 100」
 • Where、Select、OrderBy 是 LINQ 方法，搭配 Lambda 威力強大
 • Func<> 是有回傳值的函式變數，Action<> 是沒有回傳值的
### wk0104
三層架構 — 圖書管理系統
教學重點：
 • Model：純資料，沒有邏輯
 • DAL：負責「怎麼存取資料」（這裡用記憶體模擬，實務上會接資料庫）
 • BLL：負責「業務規則是什麼」（借書條件、權限檢查）
 • UI：負責「怎麼呈現給使用者」
 • 各層用 namespace 分開，職責分明
 ### wk0105
 dotnet new console -o wk01015a 
 dotnet new wpf -o wk01015b
 dotnet new web -o wk01015c
 範例 5：Console vs WPF vs Web — 同一套邏輯，三種面孔
 這個範例展示「同樣的圖書邏輯，在不同平台上的寫法差異」。

# wk02 python
🐍 Python 入門教學規劃：5個實例對照C#思維
針對有C#基礎或完全初學的學生，以下規劃 5個由淺入深的實例，每個範例都會標註與C#的對比，幫助學生快速建立Python的思維模式。
📋 整體架構總覽

## wk0201
教學重點
1. 縮排是語法的一部分：錯誤縮排會直接導致 IndentationError
2. 動態型別：變數型別在執行時決定，可用 type() 查看
3. f-string 格式化：f"文字{變數}" 比 C# 的 $"文字{變數}" 更簡潔
### wk0201.py
python wk0201.py

## wk0202
教學重點
1. self 是什麼？：相當於 C# 的 this，但必須顯式寫在第一個參數
2. __init__ 是建構子：雙底線表示 Python 的「魔法方法」
3. @property 裝飾器：優雅的 Getter/Setter，使用時像存取欄位
4. 沒有真正的 private：用 _前綴 表示「建議不要直接存取」
### wk0202.py
python wk0202.py

## wk0203
範例 3：Lambda 與函數式程式設計 ⚡
🎯 學習目標
理解 Python 的 lambda 語法，以及強大的 List Comprehension，這是 Python 最引以為傲的特性之一。
教學重點
1. List Comprehension 是必學：[x for x in list if condition] 比 map+filter 更 Pythonic
2. Lambda 限制：只能寫單行運算式，複雜邏輯請用 def
3. 函式是第一級公民：可以傳入、回傳、賦值，類似 C# 的 Func<> 和 Action<>
### wk0203.py

## wk0204
範例 4：Console 應用程式 🖥️
🎯 學習目標
整合前面所學，建立一個具備 檔案讀寫、JSON 處理、錯誤處理 的實用 Console 程式。
🔑 與 C# 的關鍵對比
教學重點
1. with open()：自動管理檔案資源，對比 C# 的 using 語句
2. json 模組：內建支援，不需要額外安裝（對比 C# 的 System.Text.Json）
3. next() + Generator：next((x for x in list if condition), None) 是常見的「找第一個或回傳 None」模式
4. if __name__ == "__main__"：Python 的程式入口慣例
### wk0204.py

## wk0205
範例 5：Web 應用程式 🌐
🎯 學習目標
使用 Flask 框架快速建立 Web API，理解 Python 在 Web 開發的簡潔威力。
🔑 與 C# 的關鍵對比
 教學重點
1. 裝飾器路由：@app.route() 是 Flask 的核心，對比 C# 的 Attribute Routing
2. request.get_json()：自動解析 JSON 請求體
3. jsonify()：自動將 Python 字典轉為 JSON 回應
4. 內建開發伺服器：debug=True 會自動重載程式碼，開發體驗極佳

### wk0205.py
🧪 測試 API 的方式
啟動後，可以用瀏覽器或 curl 測試：
￼
# 1. 查看所有學生
curl http://localhost:5000/api/students
# 2. 查看特定學生
curl http://localhost:5000/api/students/S001
# 3. 新增學生
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{"id":"S004","name":"陳小文","age":20,"scores":[88,90,85]}'
# 4. 查看前2名
curl http://localhost:5000/api/students/top/2

#### 中文顯示
在 app = Flask(__name__) 後面加上 app.json.ensure_ascii = False 即可！

## 給 C# 背景學生的特別提醒
1. 忘記大括號和分號：Python 用縮排表達結構，一開始會很不習慣，但寫久了會覺得清爽
2. 型別是建議不是規則：Python 是鴨子型別，重視「能不能做」而非「是什麼型別」
3. 少即是多：Python 的哲學是「一種明顯的做法」，通常最直覺的寫法就是最佳實踐
4. 善用互動式環境：鼓勵學生使用 Python 互動式直譯器（或 Jupyter Notebook）即時測試程式碼
這五個範例從語法基礎一路貫穿到 Web 開發，能讓學生在 10-15 小時 內建立紮實的 Python 基礎，並理解 Python 與 C# 在設計哲學上的根本差異！

## wk0206
範例 6：Tkinter vs WPF — 視窗應用程式對照
延續前面「學生成績管理」的主題，這個範例展示如何用 Python 的 Tkinter（內建 GUI 函式庫）建立視窗應用程式，並與 C# WPF 進行概念對照。

### wk0206.py
這個範例讓學生理解：Python 的 GUI 開發雖然沒有 WPF 的 XAML 那麼強大的宣告式設計，但憑藉「純程式碼 + 輕量級」的優勢，非常適合快速原型開發和內部工具製作！
