# 系統開發流程圖與架構規劃 (System Architecture & Workflow)

本節詳細說明「全自動化跨模態影音生成管線」的開發規劃。系統採用模組化 (Modularized) 設計，並以 Python 作為核心控制腳本，串接各大開源 AI 模型與 API，實現從「純文字短篇小說」至「動態短劇影片」的端到端 (End-to-End) 產出。

## 1. 系統開發流程圖 (System Workflow Diagram)

本系統管線主要拆解為四大階段，支援角色特徵一致性控制與自動化快取管理。以下為系統整體運作之流程圖：

```mermaid
flowchart TD
    %% 定義節點樣式
    classDef stage fill:#f9f9f9,stroke:#333,stroke-width:2px;
    classDef core fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef output fill:#e8f5e9,stroke:#388e3c,stroke-width:2px;

    subgraph 階段一：文本轉譯與劇本解構
        A[短篇小說文本] -->|LLM API / Gemini| B(結構化分鏡腳本 JSON)
    end

    subgraph 階段二：角色一致性與靜態圖像生成
        B --> C{PromptBuilder<br/>提示詞管理程式}
        C -->|特徵極簡化 + Seed 鎖定| C1[合成完整提示詞]
        C1 -->|檢查 GenCache| C2{快取是否命中?}
        C2 -->|Yes| D1(讀取既有場景圖)
        C2 -->|No| D2(StableDiffusionXLPipeline<br/>Animagine-XL-3.1)
        D2 -->|產出並寫入快取| D[靜態漫畫分鏡圖]
        D1 --> D
    end

    subgraph 階段三：視覺動態化與多模態語音
        B -->|擷取對白| E3(TTS 語音生成<br/>edge-tts / pyttsx3)
        D -->|場景氛圍| E1(AnimateDiffPipeline<br/>微動效影片生成 8fps)
        D -->|角色對嘴| E2(InsightFace + SadTalker<br/>臉部定位與動態驅動)
        E3 -.->|驅動音訊| E2
    end

    subgraph 階段四：影音疊加與終端合成
        E1 --> F(MoviePy / OpenCV<br/>畫面貼合與 Alpha 羽化融合)
        E2 --> F
        E3 --> F
        F --> G[終端動態短劇影片 MP4]
    end

    %% 套用樣式
    class A,G output;
    class B,D,E1,E2,E3 core;
