#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

// --- Configuration ---
#define DEVICE_ID "esp32_node_1"
const char* ssid = "wifi_ssid"; // "YOUR_WIFI_SSID";
const char* password = "wifi_pass"; // "YOUR_WIFI_PASSWORD";
const char* mqtt_server = "mqtt_ip"; // Updated to external broker

//#define DHTPIN 4
#define DHTPIN 22
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;

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
  Serial.println("\nWiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(DEVICE_ID)) {
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
  dht.begin();
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > 5000) { // Read every 5 seconds
    lastMsg = now;
    float h = dht.readHumidity();
    float t = dht.readTemperature();

    if (isnan(h) || isnan(t)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }

    String payload = "{\"temperature\": " + String(t) + ", \"humidity\": " + String(h) + "}";
    String topic = String("mushroom/node/") + String(DEVICE_ID) + String("/data");
    
    Serial.print("Publish message to ");
    Serial.print(topic);
    Serial.print(": ");
    Serial.println(payload);
    
    client.publish(topic.c_str(), payload.c_str());
  }
}
