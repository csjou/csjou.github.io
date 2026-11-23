以下彙整先前排查與測試的結論，依**測試模組**、**下載安裝的模型與設定參數**，以及**對應測試的功能與成果**條列說明：

### 1. ComfyUI 核心與外掛相容性模組

* **測試模組**：
* Windows 可攜版 ComfyUI（`0.45.0`，搭配 `python_embeded` Python `3.13.14`、PyTorch `2.14.1+cu130`、RTX 3050 Ti Laptop GPU `4GB VRAM`）。
* `Comfyui-SadTalker` 自訂節點（含 `SadTalker`、`ShowVideo`、`ShowText`、`ShowAudio`、`LoadRefVideo`）。


* **下載安裝的模型與參數**：
* 啟動參數：`--windows-standalone-build --lowvram`。
* 套件調整：安裝 `audioop-lts` 補齊 `audioop`；移除卡死於 `get_version()` 的 `basicsr==1.3.3.3` 與相依衝突的 `gfpgan==1.3.8`，並於 `face_enhancer.py` 加入 `try...except ImportError` 讓 `GFPGANer` 缺席時不中斷載入。
* 節點與工作流：將下游輸出從接收 `VIDEO` 物件的 `SaveVideo` 改為接收 `STRING` 路徑的 `ShowVideo`，對齊 `SadTalker` 輸出的 `('video_path', 'show_video_path')`（`STRING, STRING`）。


* **對應測試的功能與成果**：
* 成功解決 `ModuleNotFoundError: audioop`、`ImportError: GFPGANer`、`basicsr` 建置失敗與 `Return type mismatch: received_type(STRING) mismatch input_type(VIDEO)`。
* 重啟後 `Comfyui-SadTalker` 節點正常註冊並可透過工作流 JSON 與 `/prompt` API 提交執行。



### 2. 人像對齊與 3DMM 前處理模組

* **測試模組**：
* `SadTalker\src\face3d\util\preprocess.py`（`align_img`、`resize_n_crop_img`）與 `SadTalker\src\utils\preprocess.py`（`generate`）。


* **下載安裝的模型與參數**：
* 執行時自動下載至 `gfpgan\weights\` 的人臉偵測與對齊權重：`alignment_WFLW_4HG.pth`、`detection_Resnet50_Final.pth`（其餘 SadTalker `256` 權重與輸入 `portrait.png`、`speech.mp3`）。
* 前處理參數：`faceModelResolution = "256"`、`preprocess = "crop"`、`gfpganAsFaceEnhancer = False`、`batchSizeInGeneration = 1`。
* 程式碼相容修正：將 `face3d/util/preprocess.py`（`left`、`up` 計算行）與 `utils/preprocess.py`（`trans_params` 拆分行）中對非 0 維 NumPy 陣列直接呼叫 `float(...)` 的寫法，改為 `float(np.asarray(...).reshape(-1)[0])` 以相容 NumPy 2.x。


* **對應測試的功能與成果**：
* 成功完成 `landmark Det`（人臉關鍵點偵測）與進入 `3DMM Extraction`，排除 NumPy 2.x `TypeError: only 0-dimensional arrays can be converted to Python scalars` 阻斷。



### 3. 影片生成與輸出驗證模組

* **測試模組**：
* `SadTalkerNode.generate` -> `Pb.test` -> `ShowVideo` / 輸出目錄（`.mp4`）。


* **下載安裝的模型與參數**：
* 沿用前一步已通過前處理的 `256` 解析度、關閉 `GFPGAN` 人臉增強、`batchSizeInGeneration = 1` 與 `--lowvram` 設定。


* **對應測試的功能與成果**：
* 工作流完整執行完畢並產出 `.mp4` 影片檔案，可透過輸出路徑查驗檔案大小與完整性，並在播放器中確認對嘴同步、裁切邊界與音軌播放效果。