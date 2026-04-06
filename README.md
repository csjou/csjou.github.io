# csjou.github.io
## Distance 
Ref: https://www.itread01.com/content/1503464527.html \
根據兩點間經緯度坐標（double值），計算兩點間距離 \
lon1 lat1 第一點的經度,緯度 \
lon2 lat3 第二點的經度,緯度 \
public static double GetDistance(double lat1,double lon1, double lat2,double lon2) \
{ \
double radLat1 = rad(lat1); \
double radLat2 = rad(lat2); \
double a = radLat1 - radLat2; \
double b = rad(lon1) - rad(lon2); \
double s = 2 * Math.asin(Math.sqrt(Math.pow(Math.sin(a/2),2)+Math.cos(radLat1)*Math.cos(radLat2)*Math.pow(Math.sin(b/2),2))); \
s = s * EARTH_RADIUS; \
s = Math.round(s * 10000) / 10000; \
return s; \
} 

```mermaid
graph LR
    %% 全域風格設定：以灰階、淺色為主，確保黑白列印清晰
    classDef hardware fill:#ffffff,stroke:#000000,stroke-width:2px;
    classDef network fill:#f2f2f2,stroke:#000000,stroke-width:1px,stroke-dasharray: 5 5;
    classDef docker fill:#f9f9f9,stroke:#000000,stroke-width:2px;
    classDef app fill:#ffffff,stroke:#000000,stroke-width:2px;

    %% 左側：感知與傳輸 (Sensing & Network)
    subgraph Left_Side ["數據源與傳輸 (Edge & Network)"]
        direction TB
        S1[DHT11/SHT31<br/>環境感測器]
        CAM[ESP32-CAM<br/>影像擷取]
        MCU[ESP32 主控模組<br/>Arduino C++]
        
        S1 --> MCU
        CAM --> MCU
        
        MCU -->|MQTT/JSON| MQTT_P[MQTT 傳輸層]
        MCU -->|HTTP Stream| HTTP_S[影像串流層]
    end

    %% 右側：雲端服務與展示 (Server & UI)
    subgraph Right_Side ["後端處理與應用 (Docker & UI)"]
        direction TB
        subgraph Docker_VM ["Docker 容器環境 (ASUS Laptop)"]
            Broker[Mosquitto<br/>MQTT Broker]
            Worker[Worker Service<br/>數據解析]
            DB[(MySQL 8.0<br/>歷史資料庫)]
            
            Broker --- Worker
            Worker --- DB
        end

        subgraph UI_Layer ["應用展示層"]
            Dash[Blazor Server<br/>監控儀表板]
            Chart[數據趨勢圖表]
            Video[即時影像視窗]
            
            Dash --- Chart
            Dash --- Video
        end
    end

    %% 左右橫向連接
    MQTT_P ----> Broker
    HTTP_S ----> Video
    DB -.->|Data Query| Dash

    %% 套用灰階風格
    class MCU,S1,CAM hardware;
    class MQTT_P,HTTP_S network;
    class Broker,DB,Worker docker;
    class Dash,Chart,Video app;
