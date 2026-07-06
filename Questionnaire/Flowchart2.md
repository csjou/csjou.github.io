```mermaid
flowchart TD
    %% 定義節點與形狀 (文字全部加上雙引號與 <br> 換行以避免解析錯誤)
    Start(["開始：載入問卷資料庫"])
    Init["建立空的 summary_results 列表"]
    
    %% 雙層迴圈結構
    LoopDV{"外層迴圈：<br>取出 1 個依變項 (管教方式)<br>(共5組)"}
    LoopIV{"內層迴圈：<br>取出 1 個自變項 (類別變項)<br>(共8組)"}
    
    %% 核心分析邏輯
    Levene["Step 1: 進行 Levene's 變異數同質性檢定"]
    CondVar{"符合同質性假設？<br>(p >= 0.05)"}
    
    StandardANOVA["Step 2A: 執行標準 ANOVA"]
    WelchANOVA["Step 2B: 執行 Welch's ANOVA"]
    
    CondSig1{"ANOVA F值<br>是否顯著？ (p < 0.05)"}
    CondSig2{"Welch 統計量<br>是否顯著？ (p < 0.05)"}
    
    PostHoc1["Step 3A: 事後比較<br>(Scheffé / Tukey)"]
    PostHoc2["Step 3B: 事後比較<br>(Games-Howell)"]
    
    NoDiff1["標示：無顯著差異"]
    NoDiff2["標示：無顯著差異"]
    
    Record["Step 4: 將單次檢定結果(包含所用方法與p值)<br>記錄到 summary_results 列表中"]
    
    %% 結束機制
    NextIV(("準備下一個自變項"))
    NextDV(("準備下一個依變項"))
    Output(["結束：匯出包含 40 筆分析結果的總表"])

    %% 建立連接線與流程邏輯
    Start --> Init
    Init --> LoopDV
    
    LoopDV -- "還有尚未分析的依變項" --> LoopIV
    LoopDV -- "已完成5組依變項" --> Output
    
    LoopIV -- "還有尚未配對的自變項" --> Levene
    LoopIV -- "已完成8組自變項" --> NextDV
    NextDV --> LoopDV
    
    Levene --> CondVar
    
    CondVar -- "是 (符合)" --> StandardANOVA
    CondVar -- "否 (違反)" --> WelchANOVA
    
    StandardANOVA --> CondSig1
    WelchANOVA --> CondSig2
    
    CondSig1 -- "是" --> PostHoc1
    CondSig1 -- "否" --> NoDiff1
    
    CondSig2 -- "是" --> PostHoc2
    CondSig2 -- "否" --> NoDiff2
    
    PostHoc1 --> Record
    NoDiff1 --> Record
    PostHoc2 --> Record
    NoDiff2 --> Record
    
    Record --> NextIV
    NextIV --> LoopIV
    
    %% 自定義樣式 (美化圖表)
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:2px;
    classDef loop fill:#e1d5e7,stroke:#9673a6,stroke-width:2px;
    classDef decision fill:#fff2cc,stroke:#d6b656,stroke-width:2px;
    classDef endpoint fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
    
    class LoopDV,LoopIV loop;
    class CondVar,CondSig1,CondSig2 decision;
    class Start,Output endpoint;
