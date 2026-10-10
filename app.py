import os
from flask import Flask, render_template_string, request, jsonify
import telebot
from telebot import types

# Flask App Initialization
app = Flask(__name__)

# Direct Bot Token configuration to avoid Railway secrets build issues
BOT_TOKEN = "8915919521:AAGA_nI0C-vYpr5AwSYyk4GKYxqF-O3OLT0"
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# In-Memory Database for Users
users_db = {}

# HTML Template for Mini-App (Arada Bingo Style)
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ethio Bingo Game</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --accent-color: #f59e0b;
            --text-color: #f8fafc;
            --btn-green: #10b981;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 15px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .header h1 {
            color: var(--accent-color);
            margin: 0;
            font-size: 26px;
        }
        .header p {
            font-size: 14px;
            color: #94a3b8;
            margin-top: 5px;
        }
        .bingo-board {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 8px;
            width: 100%;
            max-width: 360px;
            background: var(--card-bg);
            padding: 12px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        }
        .cell {
            aspect-ratio: 1;
            background: #334155;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 18px;
            border-radius: 8px;
            cursor: pointer;
            user-select: none;
            transition: all 0.2s;
        }
        .cell.selected {
            background: var(--accent-color);
            color: #000;
        }
        .cell.free {
            background: var(--btn-green);
            color: white;
        }
        .action-btn {
            width: 100%;
            max-width: 360px;
            margin-top: 20px;
            padding: 14px;
            background: var(--accent-color);
            color: #000;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
        }
        .info-card {
            width: 100%;
            max-width: 360px;
            background: var(--card-bg);
            margin-top: 20px;
            padding: 15px;
            border-radius: 12px;
            font-size: 14px;
            box-sizing: border-box;
        }
        .info-card h3 {
            margin-top: 0;
            color: var(--accent-color);
        }
    </style>
</head>
<body>

    <div class="header">
        <h1>Ethio Bingo Game</h1>
        <p id="user-greeting">እንኳን ወደ ኢትዮ ቢንጎ በደህና መጡ!</p>
    </div>

    <div class="bingo-board" id="board">
        <!-- Bingo Grid Cells -->
    </div>

    <button class="action-btn" onclick="claimBingo()">ቢንጎ! (BINGO)</button>

    <div class="info-card">
        <h3>💳 የክፍያ አማራጮች</h3>
        <p><b>ንግድ ባንክ (CBE):</b> 1000682528641<br>ስም: አንያቸው አመጀ</p>
        <p><b>ቴሌብር (Telebirr):</b> 0944123180<br>ስም: አንያቸው አመጀ</p>
    </div>

    <script>
        const tg = window.Telegram.WebApp;
        tg.expand();

        if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
            document.getElementById('user-greeting').innerText = "ሰላም " + tg.initDataUnsafe.user.first_name + " 👋! መልካም እድል!";
        }

        const board = document.getElementById('board');
        const numbers = [
            4, 18, 25, 38, 50,
            11, 22, 31, 44, 58,
            7, 19, 'FREE', 40, 60,
            2, 16, 29, 33, 52,
            14, 27, 35, 41, 55
        ];

        numbers.forEach((num) => {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            if (num === 'FREE') {
                cell.classList.add('free');
            }
            cell.innerText = num;
            cell.onclick = () => {
                cell.classList.toggle('selected');
            };
            board.appendChild(cell);
        });

        function claimBingo() {
            tg.showAlert("🎉 ቢንጎ ተብሏል! ውጤቱ እየተረጋገጠ ነው...");
        }
    </script>
</body>
</html>
"""

# Web Routes
@app.route("/")
def index():
    return render_template_string(HTML_LAYOUT)

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        if bot:
            bot.process_new_updates([update])
        return "OK", 200
    return "Forbidden", 403

# Telegram Bot Logic (Arada Bingo Flow)
if bot:
    @bot.message_handler(commands=['start'])
    def start_cmd(message):
        chat_id = message.chat.id
        if chat_id not in users_db:
            msg = bot.send_message(
                chat_id, 
                "👋 <b>እንኳን ወደ Ethio Bingo Game በደህና መጡ!</b>\n\nለመጫወት እባክዎን መጀመሪያ <b>ሙሉ ስምዎን</b> አስገቡ፦"
            )
            bot.register_next_step_handler(msg, process_name)
        else:
            show_main_menu(chat_id)

    def process_name(message):
        chat_id = message.chat.id
        name = message.text
        users_db[chat_id] = {"name": name}
        
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        btn_phone = types.KeyboardButton("📱 ስልክ ቁጥር አጋራ", request_contact=True)
        markup.add(btn_phone)
        
        msg = bot.send_message(
            chat_id, 
            f"እናመሰግናለን <b>{name}</b>!\nቀጥለው እባክዎን ከታች ያለውን በተን በመጫን የቴሌግራም ስልክ ቁጥርዎን ያጋሩ፦", 
            reply_markup=markup
        )
        bot.register_next_step_handler(msg, process_phone)

    def process_phone(message):
        chat_id = message.chat.id
        if message.contact:
            users_db[chat_id]["phone"] = message.contact.phone_number
        else:
            users_db[chat_id]["phone"] = message.text

        bot.send_message(
            chat_id, 
            "✅ <b>ምዝገባዎ በተሳካ ሁኔታ ተጠናቋል!</b>", 
            reply_markup=types.ReplyKeyboardRemove()
        )
        show_main_menu(chat_id)

    def show_main_menu(chat_id):
        user_name = users_db.get(chat_id, {}).get("name", "ተጫዋች")
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        web_app_url = "https://ethio-bingo-game-production-e562.up.railway.app"
        
        btn_play = types.InlineKeyboardButton("🎮 ጨዋታ ጀምር (Play)", web_app_url=types.WebAppInfo(url=web_app_url))
        btn_rules = types.InlineKeyboardButton("📜 የጨዋታው ህጎች", callback_data="rules")
        btn_deposit = types.InlineKeyboardButton("💳 ገንዘብ ማስገቢያ", callback_data="deposit")
        btn_account = types.InlineKeyboardButton("👤 የእኔ አካውንት", callback_data="account")
        
        markup.add(btn_play)
        markup.add(btn_deposit, btn_rules)
        markup.add(btn_account)
        
        text = f"ሰላም <b>{user_name}</b> 👋\nእንኳን ወደ <b>Ethio Bingo Game</b> በደህና መጡ!\n\nከታች ባሉት አማራጮች ጨዋታውን መጀመር ወይም ሂሳብዎን መሙላት ይችላሉ፦"
        bot.send_message(chat_id, text, reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        if call.data == "rules":
            rules_text = (
                "📜 <b>የ Ethio Bingo ጨዋታ ደንቦችና መመሪያዎች፦</b>\n\n"
                "1. ጨዋታው ከመጀመሩ በፊት በቂ ባላንስ/ካርድ ሊኖርዎት ይገባል።\n"
                "2. በሲስተሙ የሚወጡትን ቁጥሮች በካርድዎ ላይ ይከታተሉ።\n"
                "3. መስመር ያሞላ በመጀመሪያ 'BINGO' የሚለውን በመጫን አሸናፊ ይሆናል።\n"
                "4. ማንኛውም የማጭበርበር ሙከራ አካውንት እንዲታገድ ያደርጋል።"
            )
            bot.send_message(call.message.chat.id, rules_text)
        elif call.data == "deposit":
            deposit_text = (
                "💳 <b>የክፍያ መረጃ (Deposit)፦</b>\n\n"
                "<b>ንግድ ባንክ (CBE):</b>\n<code>1000682528641</code>\nስም: አንያቸው አመጀ\n\n"
                "<b>ቴሌብር (Telebirr):</b>\n<code>0944123180</code>\nስም: አንያቸው አመጀ\n\n"
                "📌 ገንዘብ ገቢ ካደረጉ በኋላ የደረሰኝ ስክሪንሾት (Screenshot) እዚህ ይላኩልን።"
            )
            bot.send_message(call.message.chat.id, deposit_text)
        elif call.data == "account":
            user_info = users_db.get(call.message.chat.id, {})
            account_text = (
                f"👤 <b>የእኔ ፕሮፋይል፦</b>\n\n"
                f"<b>ስም:</b> {user_info.get('name', 'N/A')}\n"
                f"<b>ስልክ:</b> {user_info.get('phone', 'N/A')}\n"
                f"<b>ያለዎት ባላንስ:</b> 0.00 ETB"
            )
            bot.send_message(call.message.chat.id, account_text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

