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


