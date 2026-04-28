# 系統實作計畫

本計畫旨在建構支援多設備擴展的物聯網系統，並針對部署進行容器化 (Docker VM)，將 MQTT、MySQL 與 Blazor Server 封裝成便於遷移的模組，極為適合未來擴充與雲端移植。

## Proposed Changes

### 1. 容器化基礎設施 (Docker Compose)
專案目錄 `brasil01` 下將提供一套自動化部署的 `docker-compose.yml`：
- **mosquitto (Eclipse Mosquitto)**: 負責 MQTT 訊息轉發。對所有區域網路內的 ESP32 開放 Port 1883。
- **mysql (MySQL 8.x)**: 關聯式資料庫，儲存持久化資訊。掛載本地 Volume 以免資料遺失 (Port 3306)。
- **blazor-web (.NET Blazor App)**: 採用 Docker 封裝編譯後的 .NET App，連接內部 Mosquitto 與 MySQL。

### 2. 支援多設備的資料與訊息架構
- **MySQL 資料表設定 (`mushroom_db.EnvironmentLogs`)**：
  - `Id` (主鍵)
  - `NodeId` (VARCHAR 50) - 設備識別碼，例如 `esp32_node_1`
  - `Temperature` (FLOAT)
  - `Humidity` (FLOAT)
  - `Timestamp` (DATETIME)
- **MQTT 主題設計 (利用萬用字元 `+`)**：
  - ESP32 設備發送：`mushroom/node/{NodeId}/temp` 與 `mushroom/node/{NodeId}/humidity`。
  - 後端只需一次性訂閱 `mushroom/node/#` 即可動態處理所有感測器的回報，無限擴充。

### 3. Blazor 網站功能與後端腳本
- **後端 Hosted Service**：整合 `MQTTnet` 與 `EF Core`，長期掛載在 Blazor 服務背景，扮演資料的搬運工 (Broker -> MySQL)。
- **即時看板 (Dashboard)**：首頁使用卡片式 UI 動態展開目前有連線紀錄的所有 Nodes。
- **歷史分析 (History)**：透過圖表組件，分析各個機群的溫濕度變化。
- **ESP32-CAM 影像整合**：網站直接崁入多組鏡頭的串流 IP 提供即時監視。

### 4. IoT 硬體端 (Arduino / C++)
- 規劃一個設定檔專區，讓擴展新設備時，只需將 `#define DEVICE_ID "esp32_node_2"` 變更後燒錄即可。ESP32-CAM 則同樣連接本地 Wi-Fi 啟動串流。

---

## Verification Plan

### Automated Tests
1. 確保一鍵啟動 `docker-compose up -d` 可以成功喚醒 3 個容器且不閃退。

### Manual Verification
1. 使用 MQTT 客戶端模擬 `node_01` 及 `node_02` 同時送出假資料，觀察 MySQL 內是否都有紀錄產生。
2. 實際上線時，連接實體 ESP32 並觀測網站的「即時看板」是否隨時間自動跳動更新溫濕度。
