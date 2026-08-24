using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

using Mapsui.UI.Wpf;
using Mapsui.Tiling;

namespace wk0104
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            this.Loaded += MainWindow_Loaded;
        }

        private void MainWindow_Loaded(object sender, RoutedEventArgs e)
        {
            try
            {
            // 1. 初始化 Mapsui 控制項
            var mapControl = new MapControl();
            
            // 2. 建立一個全新的地圖實體 (Map 容器)
            mapControl.Map = new Mapsui.Map(); // Map();

            // 3. 建立 OSM 圖層，並「直接在這裡」帶入合法的 User-Agent 來避免 403 阻擋
            var osmLayer = OpenStreetMap.CreateTileLayer("wk0104/1.0 (092012@mail.hwu.edu.tw)");
            
            // 4. 將 OSM 圖層加入地圖的圖層集合中
            mapControl.Map.Layers.Add(osmLayer);

            // 5. 將地圖控制項指定為 WPF 視窗的內容
            this.Content = mapControl;
            }
            catch (System.Exception ex)
           {
            // 建立詳細錯誤訊息
        string errorMessage = $"外層錯誤：{ex.Message}";
        
        // 往內層挖，抓出真正的異常原因
        if (ex.InnerException != null)
        {
            errorMessage += $"\n\n真正的原因 (InnerException)：\n{ex.InnerException.Message}";
        }

        // 顯示在畫面上
        System.Windows.MessageBox.Show(errorMessage, "地圖載入失敗");
            }
        }
        
    }
}