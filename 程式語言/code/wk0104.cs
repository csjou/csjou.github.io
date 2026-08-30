// ============================================================
// 學習目標：學會將程式碼分層，讓結構清晰、易維護
// 三層架構：Model（資料）→ DAL（資料存取）→ BLL（業務邏輯）→ UI（介面）
// ============================================================
using System;
using System.Collections.Generic;
using System.Linq; 
namespace Example04_ThreeLayerArchitecture
{
    // ==================== Model 層：定義資料結構 ====================
    namespace Models
    {
        class Book
        {
            public int Id { get; set; }
            public string Title { get; set; }
            public string Author { get; set; }
            public bool IsBorrowed { get; set; }

            public override string ToString()
            {
                string status = IsBorrowed ? "已借出" : "可借閱";
                return $"[{Id}] {Title} - {Author} ({status})";
            }
        }
    }

    // ==================== DAL 層：資料存取（假裝是資料庫）====================
    namespace DataAccess
    {
        using Example04_ThreeLayerArchitecture.Models;

        class BookRepository
        {
            // 模擬資料庫
            private List<Book> _books = new List<Book>
            {
                new Book { Id = 1, Title = "C# 入門", Author = "張三", IsBorrowed = false },
                new Book { Id = 2, Title = "設計模式", Author = "李四", IsBorrowed = true },
                new Book { Id = 3, Title = "演算法導論", Author = "王五", IsBorrowed = false }
            };

            public List<Book> GetAllBooks()
            {
                return _books;
            }

            public Book GetBookById(int id)
            {
                return _books.FirstOrDefault(b => b.Id == id);
            }

            public bool BorrowBook(int id)
            {
                var book = GetBookById(id);
                if (book == null || book.IsBorrowed)
                    return false;
                
                book.IsBorrowed = true;
                return true;
            }

            public bool ReturnBook(int id)
            {
                var book = GetBookById(id);
                if (book == null || !book.IsBorrowed)
                    return false;
                
                book.IsBorrowed = false;
                return true;
            }
        }
    }

    // ==================== BLL 層：業務邏輯（規則與流程）====================
    namespace BusinessLogic
    {
        using Example04_ThreeLayerArchitecture.DataAccess;
        using Example04_ThreeLayerArchitecture.Models;

        class BookService
        {
            // 依賴注入：BLL 依賴 DAL，但由外部傳入
            private BookRepository _repository;

            public BookService(BookRepository repository)
            {
                _repository = repository;
            }

            public List<Book> GetAvailableBooks()
            {
                // 業務邏輯：只顯示可借閱的書
                return _repository.GetAllBooks()
                                  .Where(b => !b.IsBorrowed)
                                  .ToList();
            }

            public string BorrowBook(int bookId, string borrowerName)
            {
                // 業務邏輯：借書前可以檢查會員資格、借閱上限等
                if (string.IsNullOrEmpty(borrowerName))
                    return "借閱人姓名不可空白";

                bool success = _repository.BorrowBook(bookId);
                return success 
                    ? $"{borrowerName} 成功借閱編號 {bookId} 的書籍" 
                    : "借閱失敗（書籍不存在或已被借出）";
            }
        }
    }

    // ==================== UI 層：使用者介面（Console）====================
    namespace Presentation
    {
        using Example04_ThreeLayerArchitecture.BusinessLogic;
        using Example04_ThreeLayerArchitecture.DataAccess;

        class Program
        {
            static void Main(string[] args)
            {
                Console.WriteLine("=== 圖書管理系統 ===\n");

                // 組合各層：建立依賴關係
                var repository = new BookRepository();
                var service = new BookService(repository);

                // 顯示所有書籍
                Console.WriteLine("【所有書籍】");
                foreach (var book in repository.GetAllBooks())
                {
                    Console.WriteLine(book);
                }

                // 顯示可借閱書籍（透過業務邏輯層）
                Console.WriteLine("\n【可借閱書籍】");
                foreach (var book in service.GetAvailableBooks())
                {
                    Console.WriteLine(book);
                }

                // 執行借書
                Console.WriteLine("\n【借書操作】");
                Console.WriteLine(service.BorrowBook(1, "王小明"));
                Console.WriteLine(service.BorrowBook(2, "李小華")); // 已借出，應失敗

                Console.WriteLine("\n按任意鍵結束...");
                Console.ReadKey();
            }
        }
    }
}
