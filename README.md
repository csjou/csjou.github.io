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
    %% 全域風格設定：灰階、淺色、高對比
    classDef hardware fill:#ffffff,stroke:#000000,stroke-width:2px;
    classDef network fill:#ffffff,stroke:#000000,stroke-width:1.5px,stroke-dasharray: 5 5;
    classDef docker fill:#f2f2f2,stroke:#000000,stroke-width:2px;
    classDef app fill:#ffffff,stroke:#000000,stroke-width:2px;

    %% 左側：感知與傳輸 (Sensing & Network)
    subgraph Sensing_Network ["感知與傳輸層 (Edge & Network)"]
        direction TB
        S1[DHT11/SHT31<br/>環境感測]
        CAM[ESP32-CAM<br/>影像擷取]
        MCU[ESP32 主控模組<br/>Arduino C++]
        MQTT_P[MQTT 傳輸層<br/>JSON Push]
        HTTP_S[影像串流層<br/>HTTP Stream]
        
        S1 & CAM --> MCU
        MCU --> MQTT_P
        MCU --> HTTP_S
    end

    %% 右側分層：服務在右側上方，應用在右側下方
    subgraph Server_App_Group ["後端與應用端 (Host: ASUS GV301Q)"]
        direction TB
        
        %% 右上：服務層
        subgraph Docker_VM ["服務層 (Docker Containers)"]
            direction LR
            Broker[Mosquitto<br/>Broker]
            Worker[Worker<br/>Service]
            DB[(MySQL 8.0<br/>Database)]
            
            Broker --> Worker --> DB
        end

        %% 右下：應用層
        subgraph UI_Layer ["應用展示層 (Web Interface)"]
            direction LR
            Dash[Blazor Server<br/>Dashboard]
            Chart[數據趨勢圖]
            Video[影像監視窗]
            
            Dash --- Chart
            Dash --- Video
        end
    end

    %% 跨區連線
    MQTT_P ----> Broker
    HTTP_S ----> Video
    DB -.->|Data Fetch| Dash

    %% 套用風格
    class MCU,S1,CAM hardware;
    class MQTT_P,HTTP_S network;
    class Broker,DB,Worker docker;
    class Dash,Chart,Video app;
