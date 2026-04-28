# 建置階段 (Build Stage)
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src

# 先複製專案檔並還原依賴項 (利用 Docker 快取)
COPY ["MushroomMonitor.csproj", "./"]
RUN dotnet restore "MushroomMonitor.csproj"

# 複製其餘原始碼並進行建置
COPY . .
RUN dotnet build "MushroomMonitor.csproj" -c Release -o /app/build

# 發佈階段 (Publish Stage)
FROM build AS publish
RUN dotnet publish "MushroomMonitor.csproj" -c Release -o /app/publish /p:UseAppHost=false

# 執行階段 (Final Runtime Stage)
FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS final
WORKDIR /app
COPY --from=publish /app/publish .

# 設定環境變數監聽常用埠位
ENV ASPNETCORE_URLS=http://+:8080
EXPOSE 8080

ENTRYPOINT ["dotnet", "MushroomMonitor.dll"]
