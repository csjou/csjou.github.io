# csjou.github.io
## Distance 
Ref: https://www.itread01.com/content/1503464527.html \
根據兩點間經緯度坐標（double值），計算兩點間距離 \
lon1 lat1 第一點的經度,緯度 \
lon2 lat3 第二點的經度,緯度 \
public static double GetDistance(double lat1,double lon1, double lat2,double lon2) \
{ \
double radLat1 = rad(lat1); \
double radLat2 = rad(lat2); \
double a = radLat1 - radLat2; \
double b = rad(lon1) - rad(lon2); \
double s = 2 * Math.asin(Math.sqrt(Math.pow(Math.sin(a/2),2)+Math.cos(radLat1)*Math.cos(radLat2)*Math.pow(Math.sin(b/2),2))); \
s = s * EARTH_RADIUS; \
s = Math.round(s * 10000) / 10000; \
return s; \
} 
