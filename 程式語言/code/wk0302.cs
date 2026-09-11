// C# - Class
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
// C# - Object Initializer
Func<int, int> square = x => x * x;
var numbers = new List<int> { 1, 2, 3 };
var squared = numbers.Select(n => n * n).ToList();
var student = new Student("Alice", 85);
var anonymousStudent = new { Name = "Bob", Score = 70 };
Console.WriteLine($"Student: {student.Name}, Score: {student.Score}"); 
Console.WriteLine($"Anonymous Student: {anonymousStudent.Name}, Score: {anonymousStudent.Score}");
Console.WriteLine($"Squared: {string.Join(", ", squared)}");   
// C# - Lambda


public class Student {
    public string Name { get; set; }
    public int Score { get; set; }
    
    public Student(string name, int score) {
        Name = name;
        Score = score;
    }
    
    public bool IsPassed() => Score >= 60;  // Lambda expression
}

