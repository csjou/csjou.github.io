// C#
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

int age = 25;
string name = "Alice";
var scores = new List<int> { 90, 85, 88 };
scores.Add(95);

const double PI = 3.14159;
// PI = 3.14;  // ❌ 編譯錯誤
Console.WriteLine($"Name: {name}, Age: {age}");
Console.WriteLine($"PI: {PI}");