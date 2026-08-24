OpenStreetMap 應用功能清單
在熟悉基礎的地圖載入後，您可以逐步擴充以下進階功能：

## 基礎圖資操作：動態載入 OSM 瓦片 (Tiles)、滑鼠拖曳平移、滾輪縮放、設定最大/最小縮放層級。

## 動態標記 (Markers) 系統：在地圖上標記特定經緯度位置 (如：IoT 感測器節點、特定建築物)，並支援自訂 WPF 控制項 (如按鈕、圖片、幾何圖形) 作為標記外觀。

## 多邊形與幾何繪製 (Polygons & Routes)：根據一系列的 GPS 座標點，在地圖上繪製行車軌跡、校園導覽路線或劃定特定區域邊界 (Geofencing)。

## 互動式圖層提示 (ToolTips & Popups)：當滑鼠懸停或點擊特定標記時，彈出包含即時數據 (例如：溫濕度監測值) 的資訊視窗。

## 離線圖資快取 (Offline Caching)：將瀏覽過的圖資快取到本機 SQLite 資料庫中，讓系統在無網路環境下也能正常顯示已載入過的地圖區域。

## 座標轉換系統：結合點擊事件 (Mouse Click)，將螢幕的像素座標 (X, Y) 即時反向轉換為真實世界的經緯度 (Lat, Lng)，適合用於手動標記地點。

## wk0101 Error 403 Access block

## wk0103/wk0105 dotnet framework 4.7.2
add package Mapsui.Wpf-Net472

## wk0103 dotnet core 10.0 wpf
版本要注意!
<ItemGroup>
    <PackageReference Include="HarfBuzzSharp.NativeAssets.Win32" Version="8.3.1.3" />
    <PackageReference Include="Mapsui.Wpf" Version="5.1.0" />
    <PackageReference Include="SkiaSharp" Version="3.119.2" />
    <PackageReference Include="SkiaSharp.NativeAssets.Win32" Version="3.119.2" />
    <PackageReference Include="SkiaSharp.Views.WPF" Version="3.119.2" />
</ItemGroup>