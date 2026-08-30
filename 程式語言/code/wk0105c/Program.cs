// ============================================================
// Web 版本：提供 HTTP API，供網頁/手機 App 呼叫
// 需要建立 ASP.NET Core Web API 專案
// ============================================================

// 📁 Program.cs
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// 模擬資料庫
var books = new List<Book>
{
    new Book { Id = 1, Title = "C# 入門", IsBorrowed = false },
    new Book { Id = 2, Title = "設計模式", IsBorrowed = true },
    new Book { Id = 3, Title = "演算法導論", IsBorrowed = false }
};

// API 端點：GET /books → 回傳所有書籍
app.MapGet("/books", () => books);

// API 端點：GET /books/{id} → 回傳特定書籍
app.MapGet("/books/{id}", (int id) => 
{
    var book = books.FirstOrDefault(b => b.Id == id);
    return book is null ? Results.NotFound() : Results.Ok(book);
});

// API 端點：POST /books/{id}/borrow → 借書
app.MapPost("/books/{id}/borrow", (int id) =>
{
    var book = books.FirstOrDefault(b => b.Id == id);
    if (book is null) return Results.NotFound("書籍不存在");
    if (book.IsBorrowed) return Results.BadRequest("已被借出");
    
    book.IsBorrowed = true;
    return Results.Ok(new { message = "借書成功", book });
});

app.Run();

public class Book
{
    public int Id { get; set; }
    public string Title { get; set; }
    public bool IsBorrowed { get; set; }
}

// 測試方式：
// 1. 執行後開啟瀏覽器
// 2. 訪問 https://localhost:5001/books 查看 JSON 資料
// 3. 用 Postman 呼叫 POST /books/1/borrow 來借書
/*
# 1. 設定 API 網址
$url = "http://localhost:5140/books/1/borrow"

# 2. 設定 Headers（指定資料格式為 JSON）
$headers = @{
    "Content-Type" = "application/json"
}

# 3. 設定 Body 資料（若不需參數可改為 "{}"）
$body = @{
    "userId" = "user_12345"
} | ConvertTo-Json

# 4. 發送 POST 請求並取得完整回應
$response = Invoke-WebRequest -Uri $url -Method Post -Headers $headers -Body $body

# 5. 顯示執行結果
Write-Host "狀態碼: " $response.StatusCode
Write-Host "回應內容: " $response.Content

*/
