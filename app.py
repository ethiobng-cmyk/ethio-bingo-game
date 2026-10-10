import os
from flask import Flask, render_template_string, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

app = Flask(__name__)

# የድርጅቱ የባንክ እና የቴሌብር መረጃዎች
BANK_DETAILS = """
🏦 **የኢትዮ ቢንጎ የክፍያ አማራጮች (Deposit Account)**

ከዚህ በታች ባሉት ሂሳቦች ገንዘብ ገቢ ማድረግ ይችላሉ፦

1️⃣ **ንግድ ባንክ (CBE)**
• Account: `1000682528641`
• Name: Enyachew Amerga (እንያቸው አመርጋ)

2️⃣ **ቴሌብር (Telebirr)**
• Phone: `0944123180`
• Name: Enyachew Amerga (እንያቸው አመርጋ)

⚠️ **ማሳሰቢያ፦** ገንዘብ ገቢ ካደረጉ በኋላ የደረሰኙን ትራንዛክሽን አይዲ (Transaction ID) ወይም ስክሪንሹት ለሳፖርት ይላኩ!
"""

# የቴሌግራም ሚኒ-አፕ (Web App) UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ethio Bingo Game</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body { font-family: Arial, sans-serif; background-color: #0f172a; color: #ffffff; text-align: center; padding: 15px; margin: 0; }
        h1 { color: #f59e0b; margin-bottom: 5px; }
        .sub-title { color: #94a3b8; font-size: 14px; margin-bottom: 20px; }
        .card { display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; max-width: 320px; margin: 0 auto; background: #1e293b; padding: 12px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        .cell { background: #334155; padding: 14px 0; font-size: 16px; font-weight: bold; border-radius: 6px; cursor: pointer; user-select: none; }
        .cell.marked { background: #22c55e; color: white; }
        .btn-bingo { background: #eab308; color: #000; font-weight: bold; border: none; padding: 14px 28px; font-size: 18px; border-radius: 8px; cursor: pointer; margin-top: 20px; width: 100%; max-width: 320px; }
    </style>
</head>
<body>
    <h1>Ethio Bingo Game</h1>
    <div class="sub-title">እንኳን ወደ ኢትዮ ቢንጎ በደህና መጡ!</div>
    
    <div class="card" id="bingoCard"></div>

    <button class="btn-bingo" onclick="callBingo()">ቢንጎ! (BINGO)</button>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();

        const cardDiv = document.getElementById('bingoCard');
        let numbers = [4, 18, 25, 38, 50, 11, 22, 31, 44, 58, 7, 19, "FREE", 40, 60, 2, 16, 29, 33, 52, 14, 27, 35, 41, 55];

        numbers.forEach((num) => {
            let cell = document.createElement('div');
            cell.className = 'cell';
            cell.innerText = num;
            if(num === "FREE") cell.classList.add('marked');
            cell.onclick = function() {
                if(num !== "FREE") cell.classList.toggle('marked');
            };
            cardDiv.appendChild(cell);
        });

        function callBingo() {
            tg.showAlert("ቢንጎ ብለዋል! አሸናፊነትዎ በቦቱ በኩል እየተረጋገጠ ነው...");
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    return jsonify({"status": "running", "bot": "Ethio Bingo Game"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
