// ============================================================
// 學習目標：理解「類別是藍圖，物件是實體」
// ============================================================
using System;
namespace Example02_ClassAndObject
{
    // 定義一個「學生」類別（藍圖）
    class Student
    {
        // 屬性（Property）：封裝欄位，控制讀寫權限
        public string Name { get; set; }
        public int Age { get; set; }
        
        // 自動屬性 + 唯讀
        public string StudentId { get; }

        // 建構子（Constructor）：建立物件時自動執行
        public Student(string name, int age, string studentId)
        {
            Name = name;
            Age = age;
            StudentId = studentId;
        }

        // 方法（Method）：物件能做的事
        public void Introduce()
        {
            Console.WriteLine($"大家好，我是{Name}，{Age}歲，學號{StudentId}。");
        }

        public bool IsAdult()
        {
            return Age >= 18;
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            // 用 new 建立「物件實例」（根據藍圖蓋出的實體房子）
            Student student1 = new Student("王小明", 20, "S001");
            Student student2 = new Student("李小華", 17, "S002");

            // 使用物件
            student1.Introduce();
            student2.Introduce();

            Console.WriteLine($"\n{student1.Name} 是否成年？{student1.IsAdult()}");
            Console.WriteLine($"{student2.Name} 是否成年？{student2.IsAdult()}");

            // 靜態成員 vs 實例成員的對比
            Console.WriteLine($"\n目前建立了學生物件，但 C# 中靜態屬於「類別本身」");
            Console.WriteLine("例如：Console.WriteLine() — WriteLine 是靜態方法，不需要 new Console()");

            Console.ReadKey();
        }
    }
}
