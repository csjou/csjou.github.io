// 範例 1：Hello C# — Namespace / Class / Main

// ============================================================
// 學習目標：理解 C# 程式的基本骨架
// ============================================================

// Namespace（命名空間）：用來組織和分類程式碼，避免名稱衝突
using System; // 引入 System 命名空間，提供基本功能，如輸入輸出
namespace Example01_BasicStructure
{
    // Class（類別）：程式的基本單位，裡面可以包含資料和方法
    class Program
    {
        // Main 方法：程式的進入點，執行時會從這裡開始
        static void Main(string[] args)
        {
            Console.WriteLine("=== 歡迎來到 C# 世界 ===");
            
            // 變數宣告：型別 變數名 = 值;
            string name = "小明";
            int age = 20;
            double score = 87.5;
            bool isStudent = true;

            // 字串插值（String Interpolation）：用 $ 符號
            Console.WriteLine($"姓名：{name}，年齡：{age}，成績：{score}");
            Console.WriteLine($"是否為學生：{isStudent}");

            // 條件判斷
            if (score >= 60)
            {
                Console.WriteLine("及格！");
            }
            else
            {
                Console.WriteLine("不及格...");
            }

            // 迴圈
            Console.WriteLine("倒數：");
            for (int i = 3; i >= 1; i--)
            {
                Console.Write($"{i}... ");
            }
            Console.WriteLine("發射！");

            Console.WriteLine("\n按任意鍵結束...");
            Console.ReadKey();
        }
    }
}
