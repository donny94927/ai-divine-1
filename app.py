import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)  # 允許前端網頁跨網域呼叫這個 API

# 1. 完整 22 張大阿爾克那牌組資料
tarot_deck = [
    "0. 愚者 (The Fool) - 代表冒險、盲目、新的起點與無限可能",
    "1. 魔術師 (The Magician) - 代表具備資源、展現創造力、主動性",
    "2. 女祭司 (The High Priestess) - 象徵沉靜、理性、聽從內心的直覺與智慧",
    "3. 女皇 (The Empress) - 代表豐收、母愛、富足與溫暖的能量",
    "4. 皇帝 (The Emperor) - 代表權力、控制、紀律、嚴肅與穩定力",
    "5. 教皇 (The Hierophant) - 代表傳統、體制、貴人相助、引導與學習",
    "6. 戀人 (The Lovers) - 代表面臨重要的選擇、和諧的關係、吸引力",
    "7. 戰車 (The Chariot) - 代表意志力、勝利、克服困難、衝勁與前進",
    "8. 力量 (Strength) - 代表以柔克剛、勇氣、耐心與內心的強大",
    "9. 隱士 (The Hermit) - 代表內省、孤獨、尋找真理、低調與沉澱",
    "10. 命運之輪 (Wheel of Fortune) - 代表轉機、命運的安排、順應變化與機會",
    "11. 正義 (Justice) - 代表公平、法律、理性思考、因果關係與決定",
    "12. 倒吊人 (The Hanged Man) - 代表換個角度思考、犧牲、等待與考驗",
    "13. 死神 (Death) - 代表舊事物的終結、徹底的結束與迎接全新的轉變",
    "14. 節制 (Temperance) - 代表溝通、淨化、協調、平衡與細水長流",
    "15. 惡魔 (The Devil) - 代表慾望、束縛、誘惑、物質享受與沉迷",
    "16. 高塔 (The Tower) - 代表突如其來的衝擊、幻滅、破壞與意外的覺醒",
    "17. 星星 (The Star) - 代表希望、祝福、正能量、療癒與願景達成",
    "18. 月亮 (The Moon) - 代表不安、迷茫、恐懼、隱藏的秘密與潛意識",
    "19. 太陽 (The Sun) - 代表光明、成功、活力、喜悅與充滿自信的未來",
    "20. 審判 (Judgment) - 代表重生的機會、重大決定、覺醒與因果回報",
    "21. 世界 (The World) - 代表完美終點、圓滿、達成目標、一個階段的順利結束"
]

# 2. 定義允許的合法關鍵字清單（你可以自己隨時增減）
ALLOWED_KEYWORDS = ["運勢", "愛情", "學業", "工作", "財運", "占卜"]

@app.route('/api/divine', methods=['POST'])
def divine():
    data = request.json
    user_question = data.get('question', '').strip()  # 移除文字前後多餘空白
    
    # 【改動一：欄位驗證】檢查使用者的提問有沒有包含我們指定的關鍵字
    has_keyword = any(keyword.lower() in user_question.lower() for keyword in ALLOWED_KEYWORDS)
    
    # 如果使用者亂輸入（不包含關鍵字），直接阻擋並回傳引導訊息
    if not has_keyword:
        return jsonify({
            "card": "🔮 宇宙訊號混亂",
            "analysis": "🧙 大師開導：『占卜需要誠心。請在問題中加入以下關鍵字，大師才能為你指點迷津：\n【愛情、學業、工作、運勢、財運、占卜】』"
        })
    
    # 【通過驗證】隨機抽一張牌
    drawn_card = random.choice(tarot_deck)
    
    # 建立給 AI 的提示詞（Prompt）
    prompt = f"你是一位精通塔羅牌的神祕學大師。信徒問題：{user_question}。他抽到的牌：{drawn_card}。請用溫柔、神祕的語氣為他解牌，並給予具體建議。"
    
    try:
        # 【改動二：硬編碼鎖定 API Key】直接餵入你的金鑰，解決環境變數讀不到的問題
        client = genai.Client(api_key="")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        ai_analysis = response.text
    except Exception as e:
        ai_analysis = f"（大師暫時斷線了，因為：{str(e)}。但這張牌代表好兆頭！）"

    return jsonify({
        "card": drawn_card,
        "analysis": ai_analysis
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)