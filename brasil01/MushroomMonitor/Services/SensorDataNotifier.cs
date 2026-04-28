using System;

namespace MushroomMonitor.Services
{
    public class SensorDataNotifier
    {
        /// <summary>
        /// 每當新的感測資料儲存時，觸發此事件。
        /// </summary>
        public event Action? OnDataReceived;

        /// <summary>
        /// 每當收到新的監控圖片時，觸發此事件。
        /// </summary>
        public event Action<string>? OnImageReceived;

        /// <summary>
        /// 存放最新圖片的 Base64 字串。
        /// </summary>
        public string? LatestImageBase64 { get; private set; }

        /// <summary>
        /// 被外部服務 (如 MqttBackgroundService) 呼叫以發出資料通知。
        /// </summary>
        public void Notify()
        {
            OnDataReceived?.Invoke();
        }

        /// <summary>
        /// 被外部服務呼叫以更新圖片並通知 UI。
        /// </summary>
        /// <param name="base64Image">圖片的 Base64 編碼字串</param>
        public void NotifyImage(string base64Image)
        {
            LatestImageBase64 = base64Image;
            OnImageReceived?.Invoke(base64Image);
        }
    }
}
