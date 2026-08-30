// ============================================================
// 學習目標：Lambda 是「匿名函式的簡寫」，讓程式更簡潔
// ============================================================
using System;
using System.Collections.Generic;
using System.Linq;
namespace Example03_LambdaAndLinq
{
    class Product
    {
        public string Name { get; set; }
        public decimal Price { get; set; }
        public string Category { get; set; }
    }

    class Program
    {
        static void Main(string[] args)
        {
            // 建立商品清單
            List<Product> products = new List<Product>
            {
                new Product { Name = "蘋果", Price = 30, Category = "水果" },
                new Product { Name = "香蕉", Price = 20, Category = "水果" },
                new Product { Name = "高麗菜", Price = 25, Category = "蔬菜" },
                new Product { Name = "牛肉", Price = 200, Category = "肉類" },
                new Product { Name = "豬肉", Price = 150, Category = "肉類" }
            };

            Console.WriteLine("=== 所有商品 ===");
            foreach (var p in products)
            {
                Console.WriteLine($"{p.Name} - ${p.Price} ({p.Category})");
            }

            // ========================================
            // Lambda 基礎語法：(參數) => 表達式
            // ========================================

            // 1. 傳統委派寫法（比較囉嗦）
            // delegate bool CheckPrice(Product p);
            // CheckPrice isExpensive = delegate(Product p) { return p.Price > 100; };

            // 2. Lambda 寫法（簡潔！）
            // 語法：(輸入參數) => { 程式碼 }
            var expensiveProducts = products.Where(p => p.Price > 100);

            Console.WriteLine("\n=== 價格超過 100 的商品（Lambda）===");
            foreach (var p in expensiveProducts)
            {
                Console.WriteLine($"{p.Name}: ${p.Price}");
            }

            // ========================================
            // LINQ + Lambda 常見操作
            // ========================================

            // 篩選（Where）
            var fruits = products.Where(p => p.Category == "水果");
            Console.WriteLine("\n=== 水果類 ===");
            fruits.ToList().ForEach(p => Console.WriteLine(p.Name));

            // 排序（OrderBy / OrderByDescending）
            var sorted = products.OrderBy(p => p.Price);
            Console.WriteLine("\n=== 依價格排序（低到高）===");
            sorted.ToList().ForEach(p => Console.WriteLine($"{p.Name}: ${p.Price}"));

            // 選擇（Select）— 只取需要的欄位
            var names = products.Select(p => p.Name);
            Console.WriteLine("\n=== 所有商品名稱 ===");
            Console.WriteLine(string.Join(", ", names));

            // 聚合（Aggregate）
            decimal total = products.Sum(p => p.Price);
            decimal avg = products.Average(p => p.Price);
            Console.WriteLine($"\n總價：${total}，平均：${avg:F2}");

            // ========================================
            // Func<T> 與 Action<T> 委派型別
            // ========================================
            
            // Func<輸入, 輸入, ..., 輸出>：有回傳值的委派
            Func<int, int, int> add = (a, b) => a + b;
            Console.WriteLine($"\nFunc 測試：5 + 3 = {add(5, 3)}");

            // Action<輸入, ...>：無回傳值的委派
            Action<string> greet = name => Console.WriteLine($"你好，{name}！");
            greet("C# 學生");

            Console.ReadKey();
        }
    }
}
