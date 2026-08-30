// ============================================================
// Console 版本：最簡單，純文字互動
// ============================================================

namespace Example05A_ConsoleUI
{
    class Program
    {
        static void Main(string[] args)
        {
            var books = new List<(int Id, string Title, bool IsBorrowed)>
            {
                (1, "C# 入門", false),
                (2, "設計模式", true),
                (3, "演算法導論", false)
            };

            while (true)
            {
                Console.Clear();
                Console.WriteLine("=== Console 圖書系統 ===");
                Console.WriteLine("1. 查看書籍");
                Console.WriteLine("2. 借書");
                Console.WriteLine("3. 離開");
                Console.Write("請選擇：");

                string choice = Console.ReadLine();

                if (choice == "1")
                {
                    Console.WriteLine("\n書籍清單：");
                    foreach (var b in books)
                    {
                        string status = b.IsBorrowed ? "[已借出]" : "[可借閱]";
                        Console.WriteLine($"{b.Id}. {b.Title} {status}");
                    }
                }
                else if (choice == "2")
                {
                    Console.Write("輸入書籍編號：");
                    if (int.TryParse(Console.ReadLine(), out int id))
                    {
                        var book = books.FirstOrDefault(b => b.Id == id);
                        if (book.Id == 0) Console.WriteLine("書籍不存在");
                        else if (book.IsBorrowed) Console.WriteLine("已被借出");
                        else
                        {
                            // 更新狀態
                            int idx = books.FindIndex(b => b.Id == id);
                            books[idx] = (id, book.Title, true);
                            Console.WriteLine("借書成功！");
                        }
                    }
                }
                else if (choice == "3") break;

                Console.WriteLine("\n按 Enter 繼續...");
                Console.ReadLine();
            }
        }
    }
}
