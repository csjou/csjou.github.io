#include "esp_camera.h"
#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "wifi_ssid";
<<<<<<< HEAD
const char* password = "wifipassword";
=======
const char* password = "wifi_pass";
>>>>>>> 154f2af283c27093ee9b2e4ce5fd9aa119be98bc
const char* mqtt_server = "mqtt_ip"; // 您的 MQTT Broker 位址
const char* mqtt_topic = "mushroom/node/cam01/image";

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;
// 設定傳送間隔 (毫秒)。目前設定為 10 分鐘 (10 * 60 * 1000)
// 為了測試，您可以先改短一點，例如 30000 (30秒)
unsigned long interval = 600000; 

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32CAM_Client")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  
  // ESP32-CAM 針腳配置 (AI Thinker)
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = 5; config.pin_d1 = 18; config.pin_d2 = 19; config.pin_d3 = 21;
  config.pin_d4 = 36; config.pin_d5 = 39; config.pin_d6 = 34; config.pin_d7 = 35;
  config.pin_xclk = 0; config.pin_pclk = 22; config.pin_vsync = 25;
  config.pin_href = 23; config.pin_sscb_sda = 26; config.pin_sscb_scl = 27;
  config.pin_pwdn = 32; config.pin_reset = -1;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  
  // 如果有 PSRAM，解析度設為 VGA (640x480)，品質調好一點
  if(psramFound()){
    config.frame_size = FRAMESIZE_VGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  setup_wifi();
  client.setServer(mqtt_server, 1883);
  
  // 重要：增加 MQTT 封包緩衝區大小以容納圖片
  // 640x480 JPEG 約 20KB-50KB，這裡設為 64KB
  client.setBufferSize(64000);
}

void capture_and_publish() {
  camera_fb_t * fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }

  Serial.printf("Captured image, size: %u bytes\n", fb->len);

  if (client.publish(mqtt_topic, fb->buf, fb->len)) {
    Serial.println("Image published successfully");
  } else {
    Serial.println("Image publish failed (check buffer size or connection)");
  }

  esp_camera_fb_return(fb);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > interval) {
    lastMsg = now;
    capture_and_publish();
  }
}
