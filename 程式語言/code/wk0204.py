# ============================================
# 範例4：Console應用程式 - 學生成績管理系統
# ============================================

import json
import os

# 資料檔案路徑
DATA_FILE = "students_data.json"

class StudentManager:
    """學生管理系統（Console 版本）"""
    
    def __init__(self):
        self.students = []
        self._load_data()
    
    def _load_data(self):
        """從 JSON 檔案載入資料"""
        # 對比 C# 的 if (File.Exists(...))
        if os.path.exists(DATA_FILE):
            try:
                # with 語句自動管理資源（對比 C# 的 using）
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.students = json.load(f)
                print(f"✅ 已載入 {len(self.students)} 位學生資料")
            except json.JSONDecodeError:
                print("❌ 資料檔案損壞，建立新資料")
                self.students = []
        else:
            print("📁 找不到資料檔案，建立新的資料庫")
    
    def _save_data(self):
        """儲存資料到 JSON 檔案"""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            # ensure_ascii=False 才能正確儲存中文
            json.dump(self.students, f, ensure_ascii=False, indent=2)
        print("💾 資料已儲存")
    
    def add_student(self):
        """新增學生"""
        print("\n--- 新增學生 ---")
        try:
            name = input("姓名：").strip()
            if not name:
                print("❌ 姓名不能為空")
                return
            
            # 對比 C# 的 int.TryParse
            try:
                age = int(input("年齡："))
            except ValueError:
                print("❌ 年齡必須是數字")
                return
            
            student_id = input("學號：").strip()
            
            # 檢查學號是否重複
            if any(s["id"] == student_id for s in self.students):
                print("❌ 學號已存在")
                return
            
            student = {
                "name": name,
                "age": age,
                "id": student_id,
                "scores": []
            }
            self.students.append(student)
            self._save_data()
            print(f"✅ 已新增學生：{name}")
            
        except Exception as e:
            print(f"❌ 發生錯誤：{e}")
    
    def add_score(self):
        """新增成績"""
        print("\n--- 新增成績 ---")
        student_id = input("學號：").strip()
        
        # 尋找學生（對比 C# 的 FirstOrDefault）
        student = next((s for s in self.students if s["id"] == student_id), None)
        
        if not student:
            print("❌ 找不到該學生")
            return
        
        try:
            score = float(input("成績 (0-100)："))
            if not 0 <= score <= 100:
                print("❌ 成績必須在 0-100 之間")
                return
            
            subject = input("科目：").strip()
            
            student["scores"].append({
                "subject": subject,
                "score": score
            })
            self._save_data()
            print(f"✅ 已新增 {subject} 成績：{score}")
            
        except ValueError:
            print("❌ 成績必須是數字")
    
    def show_all(self):
        """顯示所有學生"""
        print("\n" + "=" * 50)
        print("📋 學生列表")
        print("=" * 50)
        
        if not self.students:
            print("尚無資料")
            return
        
        for s in self.students:
            scores = s["scores"]
            avg = sum(sc["score"] for sc in scores) / len(scores) if scores else 0
            
            print(f"\n🎓 {s['name']} ({s['id']})")
            print(f"   年齡：{s['age']} 歲")
            if scores:
                print(f"   成績：{', '.join(f'{sc['subject']}:{sc['score']}' for sc in scores)}")
                print(f"   平均：{avg:.1f}")
            else:
                print("   尚無成績")
    
    def search(self):
        """搜尋學生"""
        keyword = input("\n搜尋關鍵字（姓名或學號）：").strip().lower()
        
        results = [
            s for s in self.students 
            if keyword in s["name"].lower() or keyword in s["id"].lower()
        ]
        
        if results:
            print(f"\n找到 {len(results)} 筆結果：")
            for s in results:
                print(f"  - {s['name']} ({s['id']})")
        else:
            print("找不到符合的學生")
    
    def run(self):
        """主程式迴圈"""
        while True:
            print("\n" + "=" * 30)
            print("📚 學生成績管理系統")
            print("=" * 30)
            print("1. 新增學生")
            print("2. 新增成績")
            print("3. 顯示所有學生")
            print("4. 搜尋學生")
            print("5. 離開")
            
            choice = input("\n請選擇 (1-5)：").strip()
            
            # 對比 C# 的 switch-case（Python 3.10+ 可用 match-case）
            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.add_score()
            elif choice == "3":
                self.show_all()
            elif choice == "4":
                self.search()
            elif choice == "5":
                print("👋 再見！")
                break
            else:
                print("❌ 無效選項")


# 程式入口（對比 C# 的 static void Main）
if __name__ == "__main__":
    app = StudentManager()
    app.run()