using System.Windows;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Shapes;
using GMap.NET;
using GMap.NET.MapProviders;
using GMap.NET.WindowsPresentation;

namespace wk0101
{
    /// <summary>
    /// MainWindow.xaml 的互動邏輯
    /// </summary>
    public partial class MainWindow : Window
    {
        // 宣告 GMapControl 實例
        private GMapControl mapControl = new GMapControl();

        public MainWindow()
        {
            // 在程式進入點強制加上符合規範的 User-Agent
            // System.Net.WebRequest.DefaultUserAgent = "WpfOsmApp/1.0 (Contact: csjou.hwu@gmail.com)";
            InitializeComponent();
            
            // 視窗初始化後，建置地圖
            InitializeMap();
        }

        private void InitializeMap()
        {
        //mapControl = new GMapControl();

    // 1. 針對 GMap.NET 設定合法的 User-Agent 與 Referer 覆寫預設阻擋
    GMap.NET.MapProviders.GMapProvider.UserAgent = "wk0101/1.0 (092012@mail.hwu.edu.tw)";
    
    // 2. 設定地圖提供者
    mapControl.MapProvider = GMapProviders.OpenStreetMap;
    GMaps.Instance.Mode = AccessMode.ServerAndCache;

    // 後續的地圖屬性設定...
    mapControl.Position = new PointLatLng(25.0330, 121.5654);
    mapControl.MinZoom = 2;
    mapControl.MaxZoom = 18;
    mapControl.Zoom = 14;

    mapControl.DragButton = MouseButton.Left;
    mapControl.MouseWheelZoomType = MouseWheelZoomType.MousePositionAndCenter;

    PointLatLng markerPosition = new PointLatLng(25.0330, 121.5654);
    GMapMarker marker = new GMapMarker(markerPosition)
    {
        Shape = new Ellipse
        {
            Width = 15,
            Height = 15,
            Fill = Brushes.Red,
            Stroke = Brushes.White,
            StrokeThickness = 2,
            ToolTip = "台北 101"
        }
    };

    mapControl.Markers.Add(marker);
    this.Content = mapControl;
}    }
}