using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace wk0105
{
    using Mapsui;
    using Mapsui.Utilities;
    /// <summary>
    /// MainWindow.xaml 的互動邏輯
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            var map = new Mapsui.Map();

            // 最新版推薦寫法：手動創建並指定 App 專屬的 User-Agent 名稱（避開 OSM 封鎖）
            var osmLayer = OpenStreetMap.CreateTileLayer("wk0105/1.0");

            // 如果上述方法還是找不到 OpenStreetMap 類別，請改用以下替代寫法：
            // var osmLayer = new TileLayer(KnownTileSources.Create(KnownTileSource.OpenStreetMap, "MyWpfMapApp/1.0"));

            map.Layers.Add(osmLayer);
            MyMapControl.Map = map;
        }
    }
}
