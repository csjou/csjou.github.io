using System.Text.Json;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Configuration;
using MQTTnet;
using MQTTnet.Client;
using MushroomMonitor.Data;
using MushroomMonitor.Models;
using Microsoft.EntityFrameworkCore;

namespace MushroomMonitor.Services
{
    public class MqttBackgroundService : BackgroundService
    {
        private readonly ILogger<MqttBackgroundService> _logger;
        private readonly IDbContextFactory<AppDbContext> _dbFactory;
        private readonly IConfiguration _configuration;
        private readonly SensorDataNotifier _notifier;
        private IMqttClient? _mqttClient;

        public MqttBackgroundService(ILogger<MqttBackgroundService> logger, IDbContextFactory<AppDbContext> dbFactory, IConfiguration configuration, SensorDataNotifier notifier)
        {
            _logger = logger;
            _dbFactory = dbFactory;
            _configuration = configuration;
            _notifier = notifier;
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            var factory = new MqttFactory();
            _mqttClient = factory.CreateMqttClient();

            var brokerAddress = _configuration["MqttSettings:BrokerAddress"] ?? "localhost";

            var options = new MqttClientOptionsBuilder()
                .WithTcpServer(brokerAddress, 1883)
                .WithCleanSession()
                .Build();

            _mqttClient.ApplicationMessageReceivedAsync += async e =>
            {
                var topic = e.ApplicationMessage.Topic;
                var segments = topic.Split('/');
                
                // 檢查是否符合我們的 Topic 結構: mushroom/node/{nodeId}/{type}
                if (segments.Length >= 4 && segments[0] == "mushroom" && segments[1] == "node")
                {
                    var nodeId = segments[2];
                    var type = segments[3];

                    if (type == "data")
                    {
                        var payload = e.ApplicationMessage.ConvertPayloadToString();
                        try 
                        {
                            var data = JsonSerializer.Deserialize<Dictionary<string, float>>(payload, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
                            if (data != null && data.ContainsKey("temperature") && data.ContainsKey("humidity"))
                            {
                                using var db = await _dbFactory.CreateDbContextAsync();

                                var log = new EnvironmentLog
                                {
                                    NodeId = nodeId,
                                    Temperature = data["temperature"],
                                    Humidity = data["humidity"],
                                    Timestamp = DateTime.Now
                                };

                                db.EnvironmentLogs.Add(log);
                                await db.SaveChangesAsync();
                                _notifier.Notify();
                                _logger.LogInformation($"Saved data for {nodeId}: Temp={data["temperature"]}, Hum={data["humidity"]}");
                            }
                        } 
                        catch(Exception ex) 
                        {
                            _logger.LogError($"Error parsing MQTT JSON payload: {ex.Message}. Content: {payload}");
                        }
                    }
                    else if (type == "image")
                    {
                        try
                        {
                            var payloadBytes = e.ApplicationMessage.PayloadSegment.ToArray();
                            if (payloadBytes.Length > 0)
                            {
                                var base64 = Convert.ToBase64String(payloadBytes);
                                _notifier.NotifyImage(base64);
                                _logger.LogInformation($"Received image for {nodeId}, size: {payloadBytes.Length} bytes");
                            }
                        }
                        catch (Exception ex)
                        {
                            _logger.LogError($"Error processing MQTT image payload: {ex.Message}");
                        }
                    }
                }
            };

            while (!stoppingToken.IsCancellationRequested)
            {
                try
                {
                    if (!_mqttClient.IsConnected)
                    {
                        await _mqttClient.ConnectAsync(options, stoppingToken);
                        await _mqttClient.SubscribeAsync("mushroom/node/#", MQTTnet.Protocol.MqttQualityOfServiceLevel.AtLeastOnce, stoppingToken);
                        _logger.LogInformation("Connected to MQTT Broker and subscribed to mushroom/node/#");
                    }
                }
                catch (Exception ex)
                {
                    _logger.LogWarning($"MQTT Connection failed: {ex.Message}");
                }
                
                await Task.Delay(5000, stoppingToken);
            }
        }
    }
}
