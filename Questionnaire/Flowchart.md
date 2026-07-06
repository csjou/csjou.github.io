```mermaid
flowchart TD
    %% 定義節點與形狀
    Start([分析目標：檢驗三組以上類別變項在「家長管教方式」之差異])
    Step1[步驟一：進行變異數同質性檢定]
    
    Cond{是否符合\n同質性假設？}
    
    ANOVA[進行標準 ANOVA 檢定]
    Robust[使用 Robust 檢定進行校正]
    
    F_Test{檢視 F 值\n是否顯著？}
    R_Test{檢視 Brown-Forsythe\n和 Welch 是否顯著？}
    
    Scheffe[使用薛費法 Scheffé \n 進行事後比較]
    GH[使用 Games-Howell 法 \n 進行事後比較]
    
    End_NoDiff([結束：無顯著差異])
    End_Diff([終點：瞭解各組之間的差異情形])

    %% 建立連接線與流程邏輯
    Start --> Step1
    Step1 --> Cond
    
    Cond -- "情況 A：符合" --> ANOVA
    Cond -- "情況 B：違反" --> Robust
    
    ANOVA --> F_Test
    Robust --> R_Test
    
    F_Test -- "達顯著水準" --> Scheffe
    F_Test -- "未達顯著" --> End_NoDiff
    
    R_Test -- "達顯著水準" --> GH
    R_Test -- "未達顯著" --> End_NoDiff
    
    Scheffe --> End_Diff
    GH --> End_Diff
    
    %% 自定義樣式 (可選，讓圖表更美觀)
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:2px;
    classDef decision fill:#fff2cc,stroke:#d6b656,stroke-width:2px;
    classDef endpoint fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
    
    class Cond,F_Test,R_Test decision;
    class Start,End_NoDiff,End_Diff endpoint;
