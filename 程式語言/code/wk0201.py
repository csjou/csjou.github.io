# ============================================
# 範例1：Python基礎架構 - 學生資料管理
# ============================================

# 1. 變數與動態型別（不需要宣告型別！）
student_name = "王小明"      # str
student_age = 20            # int
student_score = 85.5        # float
is_passed = True            # bool

# 2. 輸出（對比 C# 的 Console.WriteLine）
print(f"學生：{student_name}，年齡：{student_age}，成績：{student_score}")

# 3. 條件判斷（注意：縮排決定程式區塊！沒有大括號）
if student_score >= 90:
    grade = "A"
    print("優秀！")
elif student_score >= 80:   # 對比 C# 的 else if
    grade = "B"
    print("良好")
else:
    grade = "C"
    print("加油")

# 4. 迴圈（對比 C# 的 foreach）
scores = [85, 92, 78, 96, 88]

# for 迴圈直接迭代（不需要索引）
total = 0
for score in scores:
    total += score
    print(f"目前分數：{score}")

average = total / len(scores)
print(f"平均：{average:.2f}")  # 格式化輸出

# 5. 函式定義（對比 C# 的 method，不需要回傳型別宣告）
def calculate_grade(score):
    """根據分數回傳等第（這是 DocString，類似C#的XML註解）"""
    if score >= 90:
        return "A"          # 不需要寫 return type
    elif score >= 80:
        return "B"
    else:
        return "C"

# 6. 呼叫函式
for s in scores:
    print(f"分數 {s} -> 等第 {calculate_grade(s)}")

# 7. 字典（Dictionary）- 對比 C# 的 Dictionary<string, object>
student = {
    "name": "王小明",
    "age": 20,
    "scores": scores,
    "grade": calculate_grade(average)
}

print(f"\n學生完整資料：{student}")
print(f"姓名：{student['name']}")  # 用中括號取值
