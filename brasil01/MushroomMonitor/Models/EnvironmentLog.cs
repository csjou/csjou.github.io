using System;

namespace MushroomMonitor.Models
{
    public class EnvironmentLog
    {
        public int Id { get; set; }
        public string NodeId { get; set; } = string.Empty;
        public float Temperature { get; set; }
        public float Humidity { get; set; }
        public DateTime Timestamp { get; set; }
    }
}
