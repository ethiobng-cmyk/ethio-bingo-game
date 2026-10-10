from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# የኢትዮ ቢንጎ (Ethio Bingo) ሙሉ አደረጃጀት - እንደ አራዳ ቢንጎ ስርአት
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ኢትዮ ቢንጎ - Ethio Bingo</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --primary: #f59e0b;
            --primary-hover: #d97706;
            --text-color: #ffffff;
            --text-secondary: #94a3b8;
            --success: #10b981;
            --danger: #ef4444;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        header {
            background-color: var(--card-bg);
            padding: 15px;
            text-align: center;
            border-bottom: 1px solid #334155;
        }
        h1 {
            margin: 0;
            font-size: 22px;
            color: var(--primary);
        }
        .user-balance {
            font-size: 14px;
            color: var(--text-secondary);
            margin-top: 5px;
        }
        .container {
            flex: 1;
            padding: 15px;
            max-width: 480px;
            margin: 0 auto;
            width: 100%;
            box-sizing: border-box;
        }
        /* Navigation Tabs / Menu */
        .menu-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }
        .menu-btn {
            background-color: var(--card-bg);
            border: 1px solid #334155;
            color: var(--text-color);
            padding: 12px 8px;
            border-radius: 10px;
            font-size: 13px;
            font-weight: bold;
            cursor: pointer;
            text-align: center;
            transition: 0.2s;
        }
        .menu-btn.active, .menu-btn:hover {
            background-color: var(--primary);
            color: #000;
            border-color: var(--primary);
        }
        /* Sections */
        .section {
            display: none;
        }
        .section.active {
            display: block;
        }
        /* Bingo Card */
        .bingo-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 6px;
            margin: 15px 0;
        }
        .cell {
            background-color: var(--card-bg);
            border: 1px solid #334155;
            aspect-ratio: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            user-select: none;
            transition: 0.2s;
        }
        .cell.selected {
            background-color: var(--primary);
            color: #000;
        }
        .cell.free {
            background-color: var(--success);
            color: #fff;
            font-size: 12px;
        }
        .btn-main {
            background-color: var(--primary);
            color: #000;
            border: none;
            width: 100%;
            padding: 14px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 10px;
        }
        .btn-main:hover {
            background-color: var(--primary-hover);
        }
        /* Forms & Cards */
        .card {
            background-color: var(--card-bg);
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 15px;
            border: 1px solid #334155;
        }
        input, select {
            width: 100%;
            padding: 12px;
            margin: 8px 0 15px 0;
            background-color: #0f172a;
            border: 1px solid #334155;
            border-radius: 8px;
            color: #fff;
            box-sizing: border-box;
        }
    </style>
</head>
<body>

    <header>
        <h1>ኢትዮ ቢንጎ ቦት (Ethio Bingo)</h1>
        <div class="user-balance">ሒሳብ: <span id="balance">0.00</span> ብር</div>
    </header>

    <div class="container">
        <!-- Main Navigation Menu -->
        <div class="menu-grid">
            <button class="menu-btn active" onclick="switchTab('play')">🎮 ጨዋታ</button>
            <button class="menu-btn" onclick="switchTab('deposit')">💳 ሂሳብ ማስገባት</button>
            <button class="menu-btn" onclick="switchTab('withdraw')">💸 ማውጣት</button>
            <button class="menu-btn" onclick="switchTab('invite')">👥 ጓደኛ ግብዣ</button>
            <button class="menu-btn" onclick="switchTab('contact')">📞 እገዛ/ድጋፍ</button>
        </div>

        <!-- 1. Play Section -->
        <div id="play" class="section active">
            <div style="text-align: center; margin-bottom: 10px;">
                <span>ክፍል: <b>መደበኛ ቢንጎ (10 ብር)</b></span>
            </div>
            <div class="bingo-grid" id="bingoCard">
                <!-- Generated via JS -->
            </div>
            <button class="btn-main" onclick="callBingo()">ሉንጎ! (BINGO)</button>
        </div>

        <!-- 2. Deposit Section -->
        <div id="deposit" class="section">
            <div class="card">
                <h3>💳 የክፍያ አማራጮች (Deposit)</h3>
                <p style="font-size: 13px; color: var(--text-secondary);">እባክዎ ከታች ባሉት አካውንቶች ገንዘብ ካስተላለፉ በኋላ የትራንዛክሽን ቁጥር (Transaction ID) ያስገቡ።</p>
                <hr style="border-color: #334155;">
                <p><b>ንግድ ባንክ (CBE):</b> 1000682528641<br>ስም: አንየፈው አሙፄ</p>
                <p><b>ቴሌብር (Telebirr):</b> 0911122100<br>ስም: አንየፈው አሙፄ</p>
            </div>
            <div class="card">
                <label>የተላለፈው መጠን (ብር):</label>
                <input type="number" id="depAmount" placeholder="ለምሳሌ 50">
                <label>የባንክ/ቴሌብር ሪፈረንስ/ትራንዛክሽን ቁጥር:</label>
                <input type="text" id="depRef" placeholder="TRX12345678">
                <button class="btn-main" onclick="submitDeposit()">ክፍያ አረጋግጥ</button>
            </div>
        </div>

        <!-- 3. Withdraw Section -->
        <div id="withdraw" class="section">
            <div class="card">
                <h3>💸 ገንዘብ ማውጣት (Withdraw)</h3>
                <label>የባንክ ወይም ቴሌብር አካውንት ዓይነት:</label>
                <select id="wMethod">
                    <option value="cbe">ንግድ ባንክ (CBE)</option>
                    <option value="telebirr">ቴሌብር (Telebirr)</option>
                </select>
                <label>የአካውንት ቁጥር:</label>
                <input type="text" id="wAccount" placeholder="አካውንት ቁጥርዎ">
                <label>የሚወጣው መጠን (ብር):</label>
                <input type="number" id="wAmount" placeholder="ዝቅተኛ 100 ብር">
                <button class="btn-main" onclick="submitWithdraw()">ጥያቄ ላክ</button>
            </div>
        </div>

        <!-- 4. Invite Friend Section -->
        <div id="invite" class="section">
            <div class="card" style="text-align: center;">
                <h3>👥 ጓደኛ ይጋብዙ (Invite Friends)</h3>
                <p style="color: var(--text-secondary); font-size: 14px;">ሊንኮን ለጓደኛዎ በማጋራት ቦቱ ላይ እንዲቀላቀሉ ያድርጉ እና ቦነስ ያግኙ!</p>
                <input type="text" value="https://t.me/bravo_ethio_bingo_bot?start=ref123" readonly style="text-align: center;">
                <button class="btn-main" onclick="alert('ሊንኩ ተኮርጇል!')">ሊንክ ኮፒ አድርግ</button>
            </div>
        </div>

        <!-- 5. Contact Us Section -->
        <div id="contact" class="section">
            <div class="card" style="text-align: center;">
                <h3>📞 እገዛ እና ድጋፍ (Contact Us)</h3>
                <p style="color: var(--text-secondary); font-size: 14px;">ማንኛውም ጥያቄ ወይም አስተያየት ካለዎት ከታች ባለው አድራሻ ያግኙን።</p>
                <p>የቴሌግራም ቻት: <a href="https://t.me/support" style="color: var(--primary);" target="_blank">@EthioBingoSupport</a></p>
                <p>ስልክ ቁጥር: +251 911 122 100</p>
            </div>
        </div>
    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();

        // Tab Switching Logic
        function switchTab(tabId) {
            document.querySelectorAll('.section').forEach(sec => sec.classList.remove('active'));
            document.querySelectorAll('.menu-btn').forEach(btn => btn.classList.remove('active'));
            
            document.getElementById(tabId).classList.add('active');
            event.currentTarget.classList.add('active');
        }

        // Generate Bingo Card Grid
        const bingoCard = document.getElementById('bingoCard');
        const numbers = [4, 18, 25, 38, 50, 11, 22, 31, 44, 58, 7, 19, 'FREE', 40, 60, 2, 16, 29, 33, 52, 14, 27, 35, 41, 55];
        
        numbers.forEach((num, index) => {
            const cell = document.createElement('div');
            cell.className = num === 'FREE' ? 'cell free' : 'cell';
            cell.innerText = num;
            if(num !== 'FREE') {
                cell.onclick = () => cell.classList.toggle('selected');
            }
            bingoCard.appendChild(cell);
        });

        function callBingo() {
            alert('ሉንጎ (BINGO) ጥያቄዎ ተልኳል! እየተጣራ ነው።');
        }

        function submitDeposit() {
            alert('የክፍያ ጥያቄዎ ደርሷል! በአጭር ጊዜ ውስጥ ይረጋገጣል።');
        }

        function submitWithdraw() {
            alert('የገንዘብ ማውጣት ጥያቄዎ ተመዝግቧል!');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

