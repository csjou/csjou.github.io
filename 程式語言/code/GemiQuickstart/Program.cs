using System;
using System.IO;
using System.Threading.Tasks;
using Google.GenAI;
using Google.GenAI.Types;
class Program
{
    // 請將此處替換為您在 Google AI Studio 取得的 API 金鑰
    private const string ApiKey = "API 金鑰";

    static async Task Main(string[] args)
    {
        Console.WriteLine("=== Google AI Studio C# 基礎教學 ===");
        
        // 1. 初始化 Client
        var client = new Client(apiKey: ApiKey);
        
        // 自 2026 年起，推薦使用速度最快、性價比最高的 gemini-2.5-flash
        string modelName = "gemini-3.6-flash";

        // ==========================================
        // 功能一：最基礎的文字生成（問與答）
        // ==========================================
        Console.WriteLine("\n[1. 基礎文字生成測試...]");
        var response = await client.Models.GenerateContentAsync(
            model: modelName,
            contents: "請用一句話形容 C# 程式語言的優點。"
            // prompt: "請用一句話形容 C# 程式語言的優點。"
        );
        Console.WriteLine($"AI 回應：{response.Text}");


        // ==========================================
        // 功能二：使用系統指令（System Instruction）設定 AI 的角色
        // ==========================================
        Console.WriteLine("\n[2. 角色設定測試...]");
        var pirateResponse = await client.Models.GenerateContentAsync(
            model: modelName,
            contents: "今天天氣如何？",
            // 透過配置參數，強迫 AI 扮演特定角色
            config: new GenerateContentConfig
            {
                SystemInstruction = new Content
                {
                    Parts = new List<Part>
                    {
                        new Part { Text = "你是一個 17 世紀的加勒比海盜，說話必須帶有海盜的口吻和髒話，且結尾要說『哈、哈、哈！』。" }
                    }
                }
            }
        );
        Console.WriteLine($"海盜 AI 回應：{pirateResponse.Text}");


        // ==========================================
        // 功能三：多模態測試（分析圖片）
        // ==========================================
        Console.WriteLine("\n[3. 圖片分析測試...]");
        string imagePath = "test_image.jpg"; // 請確保專案目錄下有這張圖片

        if (System.IO.File.Exists(imagePath))
        {
            // 將圖片讀取為 Byte 陣列
            byte[] imageBytes = await System.IO.File.ReadAllBytesAsync(imagePath);
            
            var imageResponse = await client.Models.GenerateContentAsync(
                model: modelName,
                // 同時傳入文字提示詞與圖片二進位資料
                contents: new List<Content>
                {
                    new Content
                    {
                        Parts = new List<Part>
                        {
                            new Part { Text = "請詳細描述這張圖片裡有什麼？並列出三個主要色彩。" },
                            Part.FromBytes(imageBytes, "image/jpeg")
                        }
                    }
                }
            );
            Console.WriteLine($"圖片分析結果：{imageResponse.Text}");
        }
        else
        {
            Console.WriteLine($"提示：找不到 '{imagePath}'，跳過圖片分析測試。您可以放一張圖片進來試試看！");
        }
    }
}
