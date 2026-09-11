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

namespace wk0202
{
    using Mapsui.Tiling;
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            InitializeMap();
        }

        private void InitializeMap()
        {
            // 1. Create a map object
            var map = new Mapsui.Map();

            // 2. Add the OpenStreetMap tile layer
            map.Layers.Add(OpenStreetMap.CreateTileLayer());

            // 3. Assign the map configuration to the control
            MyMapControl.Map = map;
        }
    }
}