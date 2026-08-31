# ============================================
# 範例2：Class vs Object - 學生與課程系統
# ============================================

class Person:
    """基礎類別（對比 C# 的 Base Class）"""
    
    # 類別變數（對比 C# 的 static 欄位）
    total_people = 0
    
    def __init__(self, name, age):
        """
        建構子（對比 C# 的 Constructor）
        注意：第一個參數一定是 self，代表物件本身
        """
        self.name = name            # 實例屬性
        self._age = age             # _前綴表示「建議私有」（慣例）
        Person.total_people += 1   # 存取類別變數
    
    def introduce(self):
        """方法（對比 C# 的 public method）"""
        return f"我是{self.name}，{self._age}歲"
    
    # @property 裝飾器（對比 C# 的 Property）
    @property
    def age(self):
        """Getter"""
        return self._age
    
    @age.setter
    def age(self, value):
        """Setter（可加入驗證邏輯）"""
        if value < 0:
            raise ValueError("年齡不能為負數")
        self._age = value


class Student(Person):  # 繼承語法：class 子類別(父類別)
    """學生類別，繼承自 Person"""
    
    def __init__(self, name, age, student_id):
        # 呼叫父類別建構子（對比 C# 的 base()）
        super().__init__(name, age)
        self.student_id = student_id
        self._scores = []           # 私有屬性（慣例）
    
    def add_score(self, score):
        """新增成績"""
        if 0 <= score <= 100:
            self._scores.append(score)
        else:
            raise ValueError("成績必須在0-100之間")
    
    def get_average(self):
        """計算平均（對比 C# 的 method）"""
        if not self._scores:
            return 0
        return sum(self._scores) / len(self._scores)
    
    # 覆寫（Override）父類別方法
    def introduce(self):
        base = super().introduce()
        return f"{base}，學號：{self.student_id}，平均成績：{self.get_average():.1f}"
    
    # 類別方法（對比 C# 的 static method）
    @classmethod
    def create_from_dict(cls, data):
        """工廠方法：從字典建立學生物件"""
        return cls(data["name"], data["age"], data["id"])


# ===== 使用範例 =====

# 建立物件（不需要 new 關鍵字！）
student1 = Student("王小明", 20, "S001")
student2 = Student("李小華", 19, "S002")

# 使用屬性（像存取欄位一樣簡潔，對比 C# 的 Property）
student1.age = 21           # 呼叫 setter
print(f"年齡：{student1.age}")  # 呼叫 getter

# 新增成績
student1.add_score(85)
student1.add_score(92)
student1.add_score(78)

# 呼叫方法
print(student1.introduce())

# 使用類別方法建立物件
data = {"name": "張大偉", "age": 22, "id": "S003"}
student3 = Student.create_from_dict(data)
print(student3.introduce())

# 類別變數
print(f"總人數：{Person.total_people}")
