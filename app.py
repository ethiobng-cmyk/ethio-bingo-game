from flask import Flask, render_template_string, request, jsonify
import random

app = Flask(__name__)

# Complete "Arada Bingo" Style System with Correct Name & Accounts
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ኢትዮ ቢንጎ ቦት - Ethio Bingo</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        :root {
            --bg-color: #0b0f19;
            --card-bg: #161e31;
            --primary: #f59e0b;
            --primary-hover: #d97706;
            --text-color: #ffffff;
            --text-secondary: #94a3b8;
            --success: #10b981;
            --danger: #ef4444;
            --b-color: #3b82f6;
            --i-color: #8b5cf6;
            --n-color: #ec4899;
            --g-color: #06b6d4;
            --o-color: #10b981;
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
            padding: 12px 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #1e293b;
        }
        h1 {
            margin: 0;
            font-size: 18px;
            color: var(--primary);
        }
        .user-balance {
            font-size: 13px;
            background: #0f172a;
            padding: 6px 12px;
            border-radius: 20px;
            border: 1px solid #334155;
            color: var(--success);
            font-weight: bold;
        }
        .container {
            flex: 1;
            padding: 12px;
            max-width: 480px;
            margin: 0 auto;
            width: 100%;
            box-sizing: border-box;
        }
        /* Registration Overlay */
        #regScreen {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 80vh;
            text-align: center;
        }
        /* Navigation / Menu Bar */
        .menu-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 6px;
            margin-bottom: 15px;
        }
        .menu-btn {
            background-color: var(--card-bg);
            border: 1px solid #334155;
            color: var(--text-secondary);
            padding: 8px 4px;
            border-radius: 8px;
            font-size: 11px;
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
        /* Room Selection */
        .room-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-bottom: 15px;
        }
        .room-card {
            background: var(--card-bg);
            border: 2px solid #334155;
            border-radius: 10px;
            padding: 12px;
            text-align: center;
            cursor: pointer;
            transition: 0.2s;
        }
        .room-card.selected {
            border-color: var(--primary);
            background: #1e293b;
        }
        .room-card h3 {
            margin: 0 0 5px 0;
            font-size: 15px;
            color: var(--primary);
        }
        .room-card p {
            margin: 0;
            font-size: 12px;
            color: var(--text-secondary);
        }
        /* Live Called Number Board */
        .live-board {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 12px;
            text-align: center;
            margin-bottom: 15px;
            border: 1px solid #334155;
        }
        .called-number-display {
            font-size: 36px;
            font-weight: bold;
            color: var(--primary);
            margin: 5px 0;
        }
        .timer-text {
            font-size: 12px;
            color: var(--text-secondary);
        }
        /* Bingo Card Grid (B-I-N-G-O) */
        .bingo-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 5px;
            margin-bottom: 15px;
        }
        .bingo-header-cell {
            background: #0f172a;
            color: #fff;
            text-align: center;
            padding: 8px 0;
            font-weight: bold;
            font-size: 16px;
            border-radius: 6px;
        }
        .bingo-cell {
            background-color: var(--card-bg);
            border: 1px solid #334155;
            aspect-ratio: 1;
            text-align: center;
            vertical-align: middle;
            font-size: 15px;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
            user-select: none;
            transition: 0.2s;
            color: #fff;
        }
        .bingo-cell.marked {
            background-color: var(--primary) !important;
            color: #000 !important;
            border-color: var(--primary);
        }
        .bingo-cell.free-cell {
            background-color: var(--success) !important;
            color: #fff !important;
            font-size: 11px;
        }
        .btn-main {
            background-color: var(--primary);
            color: #000;
            border: none;
            width: 100%;
            padding: 12px;
            border-radius: 10px;
            font-size: 15px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 5px;
            transition: 0.2s;
        }
        .btn-main:hover {
            background-color: var(--primary-hover);
        }
        /* General Cards & Forms */
        .card {
            background-color: var(--card-bg);
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 15px;
            border: 1px solid #334155;
        }
        input, select {
            width: 100%;
            padding: 10px;
            margin: 6px 0 12px 0;
            background-color: #0f172a;
            border: 1px solid #334155;
            border-radius: 8px;
            color: #fff;
            box-sizing: border-box;
            font-size: 14px;
        }
    </style>
</head>
<body>

    <!-- REGISTRATION SCREEN (Shown on Start) -->
    <div id="regScreen" class="container">
        <div class="card" style="width: 100%;">
            <h2 style="color: var(--primary); margin-top: 0;">🎯 እንኳን ወደ ኢትዮ ቢንጎ በደህና መጡ</h2>
            <p style="font-size: 13px; color: var(--text-secondary);">ለመጀመር እባክዎ ስምዎን እና ስልክ ቁጥርዎን ያስገቡ።</p>
            <label style="text-align: left; display: block; font-size: 13px;">ሙሉ ስምዎ:</label>
            <input type="text" id="regName" placeholder="ስምዎን ያስገቡ">
            <label style="text-align: left; display: block; font-size: 13px;">ስልክ ቁጥር:</label>
            <input type="text" id="regPhone" placeholder="09xxxxxxxx">
            <button class="btn-main" onclick="completeRegistration()">ይመዝገቡ (Register)</button>
        </div>
    </div>

    <!-- MAIN APP SCREEN (Hidden until registered) -->
    <div id="mainApp" style="display: none; flex-direction: column; min-height: 100vh;">
        <header>
            <h1>ኢትዮ ቢንጎ ቦት</h1>
            <div class="user-balance">ሒሳብ: <span id="userBalance">100.00</span> ብር</div>
        </header>

        <div class="container">
            <!-- Navigation Menu -->
            <div class="menu-grid">
                <button class="menu-btn active" onclick="switchTab('play')">🎮 ጨዋታ</button>
                <button class="menu-btn" onclick="switchTab('deposit')">💳 ዲፖዚት</button>
                <button class="menu-btn" onclick="switchTab('withdraw')">💸 ማውጣት</button>
                <button class="menu-btn" onclick="switchTab('invite')">👥 ጓደኛ</button>
                <button class="menu-btn" onclick="switchTab('contact')">📞 ድጋፍ</button>
            </div>

            <!-- 1. PLAY SECTION -->
            <div id="play" class="section active">
                <div style="font-size: 13px; color: var(--text-secondary); margin-bottom: 8px; text-align: center;">የጨዋታ ክፍል ይምረጡ:</div>
                <div class="room-grid">
                    <div class="room-card selected" onclick="selectRoom(10, this)">
                        <h3>ባለ 10 ብር</h3>
                        <p>ሽልማት: 220 ብር</p>
                    </div>
                    <div class="room-card" onclick="selectRoom(20, this)">
                        <h3>ባለ 20 ብር</h3>
                        <p>ሽልማት: 450 ብር</p>
                    </div>
                    <div class="room-card" onclick="selectRoom(50, this)">
                        <h3>ባለ 50 ብር</h3>
                        <p>ሽልማት: 1,150 ብር</p>
                    </div>
                </div>

                <!-- Live Calling Box -->
                <div class="live-board">
                    <div class="timer-text">ቀጣይ ቁጥር በ <span id="countdown">3</span> ሰከንድ ውስጥ...</div>
                    <div class="called-number-display" id="currentCalledNum">B-7</div>
                    <div style="font-size: 12px; color: var(--success);" id="gameStatus">ዙር #1204 በሂደት ላይ...</div>
                </div>

                <!-- B-I-N-G-O Grid Card -->
                <table class="bingo-table">
                    <tr>
                        <td class="bingo-header-cell" style="color:var(--b-color)">B</td>
                        <td class="bingo-header-cell" style="color:var(--i-color)">I</td>
                        <td class="bingo-header-cell" style="color:var(--n-color)">N</td>
                        <td class="bingo-header-cell" style="color:var(--g-color)">G</td>
                        <td class="bingo-header-cell" style="color:var(--o-color)">O</td>
                    </tr>
                    <tbody id="bingoCardBody">
                        <!-- Dynamically populated -->
                    </tbody>
                </table>

                <button class="btn-main" onclick="checkBingoWin()" style="background-color: var(--success); color: white;">🎉 ሉንጎ! (BINGO)</button>
            </div>

            <!-- 2. DEPOSIT SECTION (With Correct Name & Accounts) -->
            <div id="deposit" class="section">
                <div class="card">
                    <h3>💳 የሂሳብ ማሞቂያ (Deposit)</h3>
                    <p style="font-size: 12px; color: var(--text-secondary);">ገንዘብ ከዚህ በታች ባሉት ትክክለኛ አካውንቶች ካስተላለፉ በኋላ ሪፈረንስ ቁጥር ያስገቡ።</p>
                    <hr style="border-color: #334155;">
                    <p style="font-size: 13px;"><b>ንግድ ባንክ (CBE):</b> 1000682528641<br><b>ስም:</b> እንያቸው አመርጋ</p>
                    <p style="font-size: 13px;"><b>ቴሌብር (Telebirr):</b> 0944123180<br><b>ስም:</b> እንያቸው አመርጋ</p>
                </div>
                <div class="card">
                    <label>የተላለፈው መጠን (ብር):</label>
                    <input type="number" id="depAmount" placeholder="ለምሳሌ 50">
                    <label>የትራንዛክሽን ቁጥር (Reference ID):</label>
                    <input type="text" id="depRef" placeholder="TRX12345678">
                    <button class="btn-main" onclick="submitDeposit()">ክፍያ አረጋግጥ</button>
                </div>
            </div>

            <!-- 3. WITHDRAW SECTION -->
            <div id="withdraw" class="section">
                <div class="card">
                    <h3>💸 ገንዘብ ማውጣት (Withdraw)</h3>
                    <label>የሂሳብ ዓይነት:</label>
                    <select id="wMethod">
                        <option value="cbe">ንግድ ባንክ (CBE)</option>
                        <option value="telebirr">ቴሌብር (Telebirr)</option>
                    </select>
                    <label>አካውንት ቁጥር:</label>
                    <input type="text" id="wAccount" placeholder="አካውንት ቁጥርዎ">
                    <label>የሚወጣው መጠን (ብር):</label>
                    <input type="number" id="wAmount" placeholder="ዝቅተኛ 50 ብር">
                    <button class="btn-main" onclick="submitWithdraw()">የማውጣት ጥያቄ ላክ</button>
                </div>
            </div>

            <!-- 4. INVITE SECTION -->
            <div id="invite" class="section">
                <div class="card" style="text-align: center;">
                    <h3>👥 ጓደኛ ይጋብዙ</h3>
                    <p style="color: var(--text-secondary); font-size: 13px;">ሊንኮን ለጓደኛዎ በመላክ ቦነስ ያግኙ!</p>
                    <input type="text" value="https://t.me/bravo_ethio_bingo_bot?start=ref123" readonly style="text-align: center;">
                    <button class="btn-main" onclick="alert('የጋበዣ ሊንክ ተኮርጇል!')">ሊንክ ኮፒ አድርግ</button>
                </div>
            </div>

            <!-- 5. CONTACT SECTION -->
            <div id="contact" class="section">
                <div class="card" style="text-align: center;">
                    <h3>📞 እገዛ እና ድጋፍ</h3>
                    <p style="color: var(--text-secondary); font-size: 13px;">ማንኛውም ጥያቄ ካለዎት ያግኙን።</p>
                    <p style="font-size: 14px;">ቴሌግራም: <a href="https://t.me/support" style="color: var(--primary);">@EthioBingoSupport</a></p>
                    <p style="font-size: 14px;">ስልክ: +251 944 123 180</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();

        let currentBalance = 100.00;
        let selectedRoomPrice = 10;

        function completeRegistration() {
            let name = document.getElementById('regName').value;
            let phone = document.getElementById('regPhone').value;
            if(!name || !phone) {
                alert('እባክዎ ስምዎን እና ስልክ ቁጥርዎን ያስገቡ!');
                return;
            }
            document.getElementById('regScreen').style.display = 'none';
            document.getElementById('mainApp').style.display = 'flex';
            generateCard();
            alert(`እንኳን ደስ አለዎት ${name}! ምዝገባው ተጠናቋል።`);
        }

        function switchTab(tabId) {
            document.querySelectorAll('.section').forEach(sec => sec.classList.remove('active'));
            document.querySelectorAll('.menu-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.currentTarget.classList.add('active');
        }

        function selectRoom(price, element) {
            document.querySelectorAll('.room-card').forEach(c => c.classList.remove('selected'));
            element.classList.add('selected');
            selectedRoomPrice = price;
            if(currentBalance < price) {
                alert('ሒሳብዎ አያሳይም! እባክዎ ዲፖዚት ያድርጉ።');
            } else {
                currentBalance -= price;
                document.getElementById('userBalance').innerText = currentBalance.toFixed(2);
                alert(`የባለ ${price} ብር ክፍል ተቀላቅለዋል! ጨዋታው ተጀምሯል።`);
                generateCard();
            }
        }

        let playerCard = [];
        function generateCard() {
            const tbody = document.getElementById('bingoCardBody');
            tbody.innerHTML = '';
            playerCard = [];

            let cols = [
                getRandomNums(1, 15, 5),
                getRandomNums(16, 30, 5),
                getRandomNums(31, 45, 5),
                getRandomNums(46, 60, 5),
                getRandomNums(61, 75, 5)
            ];

            for (let r = 0; r < 5; r++) {
                let row = document.createElement('tr');
                let rowData = [];
                for (let c = 0; c < 5; c++) {
                    let td = document.createElement('td');
                    td.className = 'bingo-cell';
                    
                    if (r === 2 && c === 2) {
                        td.innerText = 'FREE';
                        td.classList.add('free-cell');
                        rowData.push('FREE');
                    } else {
                        let val = cols[c][r];
                        td.innerText = val;
                        td.onclick = function() {
                            this.classList.toggle('marked');
                        };
                        rowData.push(val);
                    }
                    row.appendChild(td);
                }
                tbody.appendChild(row);
                playerCard.push(rowData);
            }
        }

        function getRandomNums(min, max, count) {
            let arr = [];
            while(arr.length < count) {
                let r = Math.floor(Math.random() * (max - min + 1)) + min;
                if(arr.indexOf(r) === -1) arr.push(r);
            }
            return arr.sort((a,b) => a - b);
        }

        let calledNumbersList = [];
        let letters = ['B', 'I', 'N', 'G', 'O'];
        let timerCount = 3;

        setInterval(() => {
            timerCount--;
            document.getElementById('countdown').innerText = timerCount;
            if (timerCount <= 0) {
                timerCount = 3;
                let letter = letters[Math.floor(Math.random() * letters.length)];
                let num = Math.floor(Math.random() * 15) + 1;
                if(letter === 'I') num += 15;
                if(letter === 'N') num += 30;
                if(letter === 'G') num += 45;
                if(letter === 'O') num += 60;
                
                let callStr = `${letter}-${num}`;
                document.getElementById('currentCalledNum').innerText = callStr;
                calledNumbersList.push(num);
            }
        }, 1000);

        function checkBingoWin() {
            let markedCells = document.querySelectorAll('.bingo-cell.marked');
            if (markedCells.length >= 4) {
                let winAmount = selectedRoomPrice * 22;
                currentBalance += winAmount;
                document.getElementById('userBalance').innerText = currentBalance.toFixed(2);
                alert(`🎉 እንኳን ደስ አለዎት! ሉንጎ (BINGO) ሆኗል! ${winAmount} ብር ወደ አካውንትዎ ገብቷል!`);
            } else {
                alert('አሁንም ተጨማሪ ቁጥሮች መታየት አለባቸው ወይም አልተሟላም!');
            }
        }

        function submitDeposit() {
            alert('የክፍያ ጥያቄዎ ተመዝግቧል! በሰከንዶች ውስጥ ይረጋገጣል።');
        }

        function submitWithdraw() {
            alert('የገንዘብ ማውጣት ጥያቄዎ ተልኳል!');
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
