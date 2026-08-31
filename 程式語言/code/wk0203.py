# ============================================
# 範例3：Lambda 與函數式程式設計
# ============================================

students = [
    {"name": "王小明", "score": 85, "subject": "數學"},
    {"name": "李小華", "score": 92, "subject": "數學"},
    {"name": "張大偉", "score": 78, "subject": "英文"},
    {"name": "陳小美", "score": 96, "subject": "數學"},
    {"name": "劉小強", "score": 65, "subject": "英文"},
]

# ========== 1. Lambda 函式 ==========
# 語法：lambda 參數: 回傳值（對比 C# 的 x => x * 2）

# 簡單的 lambda
double = lambda x: x * 2
print(f"double(5) = {double(5)}")

# 多參數 lambda
add = lambda x, y: x + y
print(f"add(3, 4) = {add(3, 4)}")

# ========== 2. map() - 對每個元素做轉換 ==========
# C# 對比：students.Select(s => s["score"] * 1.1)

scores = [85, 92, 78, 96, 65]

# 傳統寫法
new_scores = []
for s in scores:
    new_scores.append(s * 1.1)

# 使用 map + lambda（函數式寫法）
new_scores_map = list(map(lambda s: s * 1.1, scores))
print(f"加分後：{new_scores_map}")

# ========== 3. filter() - 過濾元素 ==========
# C# 對比：students.Where(s => s["score"] >= 80)

# 過濾及格的分數
passing_scores = list(filter(lambda s: s >= 60, scores))
print(f"及格分數：{passing_scores}")

# ========== 4. sorted() - 排序 ==========
# C# 對比：students.OrderByDescending(s => s["score"])

# 按成績排序（降冪）
sorted_students = sorted(students, key=lambda s: s["score"], reverse=True)
print("成績排序：")
for s in sorted_students:
    print(f"  {s['name']}: {s['score']}")

# ========== 5. List Comprehension（Python 殺手級特性） ==========
# 這是 Python 最強大的語法糖，可以取代大部分 map/filter

# [運算式 for 變數 in 可迭代物件 if 條件]

# 等同 map：所有成績加 10%
bonus_scores = [s * 1.1 for s in scores]
print(f"\n加分後(List Comp)：{bonus_scores}")

# 等同 filter：只取及格的
passing = [s for s in scores if s >= 60]
print(f"及格(List Comp)：{passing}")

# 綜合：及格的分數加 10%，並取整數
bonus_passing = [int(s * 1.1) for s in scores if s >= 60]
print(f"及格且加分：{bonus_passing}")

# 字典推導式（Dictionary Comprehension）
student_dict = {s["name"]: s["score"] for s in students}
print(f"\n姓名對照分數：{student_dict}")

# 複雜範例：數學科且成績>80的學生姓名
math_excellent = [
    s["name"] 
    for s in students 
    if s["subject"] == "數學" and s["score"] > 80
]
print(f"數學優秀學生：{math_excellent}")

# ========== 6. 函式作為參數（第一級公民） ==========
def apply_operation(numbers, operation):
    """接收函式作為參數（對比 C# 的 Func<>）"""
    return [operation(n) for n in numbers]

result = apply_operation(scores, lambda x: x ** 2)
print(f"\n分數平方：{result}")
