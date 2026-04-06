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
graph TD;
    %% 定義風格
    classDef hardware fill:#f9f,stroke:#333,stroke-width:2px;
    classDef network fill:#bbf,stroke:#333,stroke-width:2px;
    classDef docker fill:#dfd,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5;
    classDef app fill:#fff4dd,stroke:#d4a017,stroke-width:2px;

    subgraph Sensing_Layer ["感知層 (Edge Layer - ESP32)"]
        direction TB
        S1[DHT11 / SHT31<br/>溫濕度感測]
        S2[MH-Z19B<br/>CO2 監測]
        CAM[ESP32-CAM<br/>影像擷取]
        MCU[ESP32 主控端<br/>Arduino C++ / RTOS]
        
        S1 & S2 --> MCU
    end

    subgraph Network_Layer ["網絡傳輸層 (Network Layer)"]
        MQTT_P[MQTT 協議<br/>JSON 格式推播]
        HTTP_S[HTTP Stream<br/>低幀率影像串流]
    end

    subgraph Docker_VM ["服務層 (Docker Container - Windows 11 Host)"]
        direction TB
        Broker[Mosquitto<br/>MQTT Broker]
        DB[(MySQL 8.0<br/>歷史資料庫)]
        Worker[Worker Service<br/>數據解析與持久化]
        
        Broker <--> Worker
        Worker --> DB
    end

    subgraph Application_Layer ["應用展示層 (UI Layer)"]
        Dash[Blazor Server<br/>即時監控儀表板]
        Chart[MudBlazor<br/>數據視覺化圖表]
        Video[Live View<br/>串流監控視窗]
        
        Dash --- Chart
        Dash --- Video
    end

    %% 建立連線
    MCU -->|Publish| MQTT_P
    MQTT_P --> Broker
    CAM -->|Stream| HTTP_S
    HTTP_S --> Video
    DB <-->|Query| Dash

    %% 套用風格
    class MCU,S1,S2,CAM hardware;
    class MQTT_P,HTTP_S network;
    class Broker,DB,Worker docker;
    class Dash,Chart,Video app;
