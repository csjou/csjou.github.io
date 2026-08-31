# ============================================
# 範例6：Tkinter 視窗應用程式 - 學生成績管理器
# 檔案名：student_gui.py
# 不需要安裝任何套件，Tkinter 是 Python 標準函式庫
# ============================================

import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from typing import List


@dataclass
class Student:
    """學生資料類別（對比 C# 的 Model）"""
    name: str
    student_id: str
    scores: List[float]
    
    @property
    def average(self) -> float:
        return sum(self.scores) / len(self.scores) if self.scores else 0.0
    
    @property
    def highest(self) -> float:
        return max(self.scores) if self.scores else 0.0


class StudentManagerApp:
    """
    主應用程式類別
    對比 C# WPF 的 MainWindow.xaml.cs（Code-Behind）
    """
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🎓 學生成績管理系統 - Tkinter 版")
        self.root.geometry("700x550")
        self.root.configure(bg="#f5f5f5")
        
        # 資料模型（對比 C# 的 ObservableCollection<Student>）
        self.students: List[Student] = []
        
        # 建立 UI（對比 C# WPF 的 InitializeComponent()）
        self._create_styles()
        self._create_widgets()
        self._layout_widgets()
        
        # 預設載入幾筆資料
        self._load_sample_data()
        self._refresh_list()
    
    # ========== 1. 樣式設定 ==========
    def _create_styles(self):
        """設定控制項樣式（對比 C# WPF 的 Style/Resource）"""
        style = ttk.Style()
        style.theme_use("clam")  # 使用現代化主題
        
        # 自訂按鈕樣式
        style.configure("Primary.TButton",
                       font=("Microsoft JhengHei", 11, "bold"),
                       foreground="white",
                       background="#2196F3")
        style.map("Primary.TButton",
                 background=[("active", "#1976D2")])
        
        # 標籤樣式
        style.configure("Header.TLabel",
                       font=("Microsoft JhengHei", 14, "bold"),
                       foreground="#333333")
        
        style.configure("Stats.TLabel",
                       font=("Microsoft JhengHei", 11),
                       foreground="#555555")
    
    # ========== 2. 建立控制項 ==========
    def _create_widgets(self):
        """建立所有 UI 控制項（對比 C# XAML 中的 <Grid>...<Button>...）"""
        
        # --- 標題區 ---
        self.header_label = ttk.Label(
            self.root,
            text="🎓 學生成績管理系統",
            style="Header.TLabel"
        )
        
        # --- 輸入區（對比 C# WPF 的 StackPanel + TextBox）---
        self.input_frame = ttk.LabelFrame(
            self.root,
            text="新增學生",
            padding=10
        )
        
        # 姓名
        self.name_label = ttk.Label(self.input_frame, text="姓名：")
        self.name_var = tk.StringVar()  # 對比 C# 的 Binding 的 Source
        self.name_entry = ttk.Entry(
            self.input_frame,
            textvariable=self.name_var,  # 雙向繫結
            width=15
        )
        
        # 學號
        self.id_label = ttk.Label(self.input_frame, text="學號：")
        self.id_var = tk.StringVar()
        self.id_entry = ttk.Entry(self.input_frame, textvariable=self.id_var, width=15)
        
        # 成績
        self.score_label = ttk.Label(self.input_frame, text="成績：")
        self.score_var = tk.StringVar()
        self.score_entry = ttk.Entry(self.input_frame, textvariable=self.score_var, width=10)
        
        # 新增按鈕（對比 C# WPF 的 Button Click="AddButton_Click"）
        self.add_button = ttk.Button(
            self.input_frame,
            text="➕ 新增學生",
            style="Primary.TButton",
            command=self._on_add_student  # 事件處理函式
        )
        
        # --- 列表區（對比 C# WPF 的 ListView / DataGrid）---
        self.list_frame = ttk.LabelFrame(self.root, text="學生列表", padding=5)
        
        # Treeview 是 Tkinter 的表格/樹狀控制項（對比 C# 的 DataGrid）
        columns = ("name", "id", "scores", "average", "highest")
        self.tree = ttk.Treeview(
            self.list_frame,
            columns=columns,
            show="headings",  # 只顯示表頭，不顯示樹狀節點
            height=10
        )
        
        # 定義欄位（對比 C# DataGrid 的 <DataGridTextColumn Header="..."/>）
        self.tree.heading("name", text="姓名")
        self.tree.heading("id", text="學號")
        self.tree.heading("scores", text="成績")
        self.tree.heading("average", text="平均")
        self.tree.heading("highest", text="最高分")
        
        # 欄位寬度
        self.tree.column("name", width=100, anchor="center")
        self.tree.column("id", width=80, anchor="center")
        self.tree.column("scores", width=150, anchor="center")
        self.tree.column("average", width=80, anchor="center")
        self.tree.column("highest", width=80, anchor="center")
        
        # 捲軸（對比 C# 的 ScrollViewer）
        self.scrollbar = ttk.Scrollbar(
            self.list_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        # --- 統計區（對比 C# WPF 的 StatusBar）---
        self.stats_frame = ttk.LabelFrame(self.root, text="統計資訊", padding=10)
        
        self.total_var = tk.StringVar(value="總人數：0")
        self.total_label = ttk.Label(self.stats_frame, textvariable=self.total_var, style="Stats.TLabel")
        
        self.class_avg_var = tk.StringVar(value="全班平均：0.0")
        self.class_avg_label = ttk.Label(self.stats_frame, textvariable=self.class_avg_var, style="Stats.TLabel")
        
        self.top_student_var = tk.StringVar(value="最高分學生：-")
        self.top_student_label = ttk.Label(self.stats_frame, textvariable=self.top_student_var, style="Stats.TLabel")
        
        # --- 操作按鈕區 ---
        self.button_frame = ttk.Frame(self.root)
        
        self.delete_button = ttk.Button(
            self.button_frame,
            text="🗑️ 刪除選取",
            command=self._on_delete
        )
        self.clear_button = ttk.Button(
            self.button_frame,
            text="🧹 清空全部",
            command=self._on_clear
        )
        self.refresh_button = ttk.Button(
            self.button_frame,
            text="🔄 重新整理",
            command=self._refresh_list
        )
    
    # ========== 3. 版面配置 ==========
    def _layout_widgets(self):
        """佈局管理（對比 C# WPF 的 Grid.Row/Grid.Column）"""
        
        # 標題
        self.header_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="w")
        
        # 輸入區
        self.input_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.name_label.grid(row=0, column=0, padx=5)
        self.name_entry.grid(row=0, column=1, padx=5)
        self.id_label.grid(row=0, column=2, padx=5)
        self.id_entry.grid(row=0, column=3, padx=5)
        self.score_label.grid(row=0, column=4, padx=5)
        self.score_entry.grid(row=0, column=5, padx=5)
        self.add_button.grid(row=0, column=6, padx=10)
        
        # 列表區
        self.list_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # 統計區
        self.stats_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.total_label.grid(row=0, column=0, padx=20)
        self.class_avg_label.grid(row=0, column=1, padx=20)
        self.top_student_label.grid(row=0, column=2, padx=20)
        
        # 操作按鈕
        self.button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        self.delete_button.pack(side="left", padx=5)
        self.clear_button.pack(side="left", padx=5)
        self.refresh_button.pack(side="left", padx=5)
        
        # 設定權重讓列表區可以隨視窗縮放（對比 C# WPF 的 Grid.RowDefinitions）
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_rowconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=1)
    
    # ========== 4. 事件處理 ==========
    def _on_add_student(self):
        """
        新增學生按鈕事件
        對比 C# WPF：private void AddButton_Click(object sender, RoutedEventArgs e)
        """
        name = self.name_var.get().strip()
        student_id = self.id_var.get().strip()
        score_text = self.score_var.get().strip()
        
        # 資料驗證（對比 C# 的 Validation）
        if not name or not student_id:
            messagebox.showwarning("警告", "姓名和學號不能為空！", parent=self.root)
            return
        
        # 解析成績（可輸入多個，用逗號分隔）
        try:
            scores = [float(s.strip()) for s in score_text.split(",") if s.strip()]
            if not scores:
                scores = [0.0]
        except ValueError:
            messagebox.showerror("錯誤", "成績必須是數字，多個成績請用逗號分隔", parent=self.root)
            return
        
        # 檢查學號是否重複
        if any(s.student_id == student_id for s in self.students):
            messagebox.showerror("錯誤", f"學號 {student_id} 已存在！", parent=self.root)
            return
        
        # 建立物件並加入列表
        student = Student(name=name, student_id=student_id, scores=scores)
        self.students.append(student)
        
        # 清空輸入框（對比 C# 的 TextBox.Clear()）
        self.name_var.set("")
        self.id_var.set("")
        self.score_var.set("")
        
        # 重新整理顯示
        self._refresh_list()
        
        messagebox.showinfo("成功", f"已新增學生：{name}", parent=self.root)
    
    def _on_delete(self):
        """刪除選取的學生"""
        selected = self.tree.selection()  # 取得選取的項目
        if not selected:
            messagebox.showwarning("警告", "請先選擇要刪除的學生", parent=self.root)
            return
        
        # 取得選取項目的值
        item = self.tree.item(selected[0])
        student_id = item["values"][1]  # 學號在第2欄
        
        if messagebox.askyesno("確認", f"確定要刪除學號 {student_id} 嗎？", parent=self.root):
            self.students = [s for s in self.students if s.student_id != student_id]
            self._refresh_list()
    
    def _on_clear(self):
        """清空所有資料"""
        if messagebox.askyesno("確認", "確定要清空所有資料嗎？", parent=self.root):
            self.students.clear()
            self._refresh_list()
    
    # ========== 5. 資料更新 ==========
    def _refresh_list(self):
        """
        重新整理列表顯示
        對比 C# WPF 的 ItemsSource = students; 或 NotifyPropertyChanged
        """
        # 清空 Treeview（對比 C# 的 Items.Clear()）
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 填入資料
        for student in self.students:
            scores_str = ", ".join(f"{s:.0f}" for s in student.scores)
            self.tree.insert("", "end", values=(
                student.name,
                student.student_id,
                scores_str,
                f"{student.average:.1f}",
                f"{student.highest:.1f}"
            ))
        
        # 更新統計資訊
        self._update_stats()
    
    def _update_stats(self):
        """更新統計標籤"""
        total = len(self.students)
        self.total_var.set(f"總人數：{total}")
        
        if self.students:
            all_scores = [s.average for s in self.students]
            class_avg = sum(all_scores) / len(all_scores)
            self.class_avg_var.set(f"全班平均：{class_avg:.1f}")
            
            top = max(self.students, key=lambda s: s.average)
            self.top_student_var.set(f"最高分學生：{top.name} ({top.average:.1f})")
        else:
            self.class_avg_var.set("全班平均：0.0")
            self.top_student_var.set("最高分學生：-")
    
    def _load_sample_data(self):
        """載入範例資料"""
        self.students = [
            Student("王小明", "S001", [85, 92, 78]),
            Student("李小華", "S002", [92, 88, 95]),
            Student("張大偉", "S003", [78, 85, 80]),
            Student("陳小美", "S004", [96, 92, 98]),
        ]


# ========== 程式入口 ==========
if __name__ == "__main__":
    # 建立主視窗（對比 C# 的 Window）
    root = tk.Tk()
    
    # 建立應用程式實例
    app = StudentManagerApp(root)
    
    # 啟動主迴圈（對比 C# 的 Application.Run()）
    root.mainloop()