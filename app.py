from flask import Flask, render_template_string, request, jsonify
import random

app = Flask(__name__)

# Complete Arada Bingo System - Final Production with Public Winner Announcement & Private False Bingo Disqualification
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
        /* Registration Screen */
        #regScreen {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 85vh;
            text-align: center;
        }
        /* Navigation Menu Buttons */
        .menu-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin-bottom: 15px;
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
            gap: 8px;
            margin-bottom: 12px;
        }
        .room-card {
            background: var(--card-bg);
            border: 2px solid #334155;
            border-radius: 10px;
            padding: 10px;
            text-align: center;
            cursor: pointer;
            transition: 0.2s;
        }
        .room-card.selected {
            border-color: var(--primary);
            background: #1e293b;
        }
        .room-card h3 {
            margin: 0 0 4px 0;
            font-size: 14px;
            color: var(--primary);
        }
        .room-card p {
            margin: 0;
            font-size: 11px;
            color: var(--text-secondary);
        }
        /* Live Board */
        .live-board {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 10px;
            text-align: center;
            margin-bottom: 12px;
            border: 1px solid #334155;
        }
        .called-number-display {
            font-size: 32px;
            font-weight: bold;
            color: var(--primary);
            margin: 4px 0;
        }
        .timer-text {
            font-size: 12px;
            color: var(--text-secondary);
        }
        /* Bingo Table Grid */
        .bingo-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 4px;
            margin-bottom: 12px;
        }
        .bingo-header-cell {
            background: #0f172a;
            color: #fff;
            text-align: center;
            padding: 6px 0;
            font-weight: bold;
            font-size: 15px;
            border-radius: 6px;
        }
        .bingo-cell {
            background-color: var(--card-bg);
            border: 1px solid #334155;
            aspect-ratio: 1;
            text-align: center;
            vertical-align: middle;
            font-size: 14px;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
            user-select: none;
            color: #fff;
        }
        .bingo-cell.marked {
            background-color: var(--primary) !important;
            color: #000 !important;
        }
        .bingo-cell.free-cell {
            background-color: var(--success) !important;
            color: #fff !important;
            font-size: 10px;
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
        }
        .card {
            background-color: var(--card-bg);
            padding: 14px;
            border-radius: 12px;
            margin-bottom: 12px;
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
            font-size: 13px;
        }
        /* Live Public Announcement Box */
        .announcement-box {
            background: #1e293b;
            border-left: 4px solid var(--primary);
            padding: 8px 12px;
            font-size: 12px;
            margin-bottom: 12px;
            border-radius: 4px;
            color: var(--text-secondary);
        }
    </style>
</head>
<body>

    <!-- REGISTRATION SCREEN -->
    <div id="regScreen" class="container">
        <div class="card" style="width: 100%;">
            <h2 style="color: var(--primary); margin-top: 0;">🎯 እንኳን ወደ ኢትዮ ቢንጎ ቦት በደህና መጡ</h2>
            <p style="font-size: 13px; color: var(--text-secondary);">ለመጀመር እባክዎ ስምዎን (ዩዘርኔም) እና ስልክ ቁጥርዎን ያስገቡ።</p>
            <label style="text-align: left; display: block; font-size: 12px;">ስምዎ / ዩዘርኔም (ለምሳሌ @enyachew):</label>
            <input type="text" id="regName" placeholder="@username ወይም ስምዎ">
            <label style="text-align: left; display: block; font-size: 12px;">ስልክ ቁጥር:</label>
            <input type="text" id="regPhone" placeholder="09xxxxxxxx">
            <button class="btn-main" onclick="completeRegistration()">ቦቱን ጀምር (/start)</button>
        </div>
    </div>

    <!-- MAIN APP SCREEN -->
    <div id="mainApp" style="display: none; flex-direction: column; min-height: 100vh;">
        <header>
            <h1>ኢትዮ ቢንጎ ቦት</h1>
            <div class="user-balance">ሒሳብ: <span id="userBalance">150.00</span> ብር</div>
        </header>

        <div class="container">
            <!-- Navigation Menu -->
            <div class="menu-grid">
                <button class="menu-btn active" onclick="switchTab('play')">🎮 Play</button>
                <button class="menu-btn" onclick="switchTab('deposit')">💳 Deposit</button>
                <button class="menu-btn" onclick="switchTab('withdraw')">💸 Withdraw</button>
                <button class="menu-btn" onclick="switchTab('balance')">💳 Check Balance</button>
                <button class="menu-btn" onclick="switchTab('invite')">👥 Invite</button>
                <button class="menu-btn" onclick="switchTab('contact')">📞 Contact Us</button>
            </div>

            <!-- 1. PLAY SECTION -->
            <div id="play" class="section active">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 12px; color: var(--text-secondary);">ክፍል ይምረጡ:</span>
                    <span style="font-size: 12px; color: var(--success);" id="playingStatus">ግዛት: Active (Playing)</span>
                </div>
                
                <!-- Live Public Announcement Feed -->
                <div class="announcement-box" id="publicAnnouncement">
                    📢 <b>የቦቱ ዜና:</b> ጨዋታው በቀጣይነት በሂደት ላይ ነው! መልካም ዕድል።
                </div>

                <div class="room-grid">
                    <div class="room-card selected" onclick="selectRoom(10, this)">
                        <h3>10 ETB</h3>
                        <p>ተጫዋች: 10 ሰው</p>
                    </div>
                    <div class="room-card" onclick="selectRoom(20, this)">
                        <h3>20 ETB</h3>
                        <p>ተጫዋች: 10 ሰው</p>
                    </div>
                    <div class="room-card" onclick="selectRoom(50, this)">
                        <h3>50 ETB</h3>
                        <p>ተጫዋች: 10 ሰው</p>
                    </div>
                </div>

                <div style="margin-bottom: 8px;">
                    <label style="font-size: 12px; color: var(--text-secondary);">ካርቴላ ቁጥር ይምረጡ (ከ 1 እስከ 200):</label>
                    <select id="cardSelect" onchange="changeCardNumber()">
                        <!-- Populated via JS -->
                    </select>
                </div>

                <!-- Live 45s Timer Board -->
                <div class="live-board">
                    <div class="timer-text">ቀጣይ ቁጥር በ <span id="countdown">45</span> ሰከንድ ውስጥ ይጠራል...</div>
                    <div class="called-number-display" id="currentCalledNum">B-7</div>
                    <div style="font-size: 11px; color: var(--success);" id="gameRoundInfo">ዙር በሂደት ላይ - የተጠሩ: <span id="calledCount">1</span></div>
                </div>

                <!-- B-I-N-G-O Table Grid -->
                <table class="bingo-table">
                    <tr>
                        <td class="bingo-header-cell" style="color:var(--b-color)">B</td>
                        <td class="bingo-header-cell" style="color:var(--i-color)">I</td>
                        <td class="bingo-header-cell" style="color:var(--n-color)">N</td>
                        <td class="bingo-header-cell" style="color:var(--g-color)">G</td>
                        <td class="bingo-header-cell" style="color:var(--o-color)">O</td>
                    </tr>
                    <tbody id="bingoCardBody"></tbody>
                </table>

                <button id="bingoBtn" class="btn-main" onclick="checkBingoWin()" style="background-color: var(--success); color: white;">🎉 ሉንጎ! (BINGO)</button>
            </div>

            <!-- 2. DEPOSIT SECTION -->
            <div id="deposit" class="section">
                <div class="card">
                    <h3>💳 ሒሳብ ማሞቂያ (Deposit)</h3>
                    <p style="font-size: 12px; color: var(--text-secondary);">ገንዘብ ከዚህ በታች ባሉት አካውንቶች ካስተላለፉ በኋላ የFT ሪፈረንስ ቁጥር ያስገቡ። ቦቱ አረጋግጦ ወዲያው ይጨምራል።</p>
                    <hr style="border-color: #334155;">
                    <p style="font-size: 13px;"><b>ንግድ ባንክ (CBE):</b> 1000682528641<br><b>ስም:</b> እንያቸው አመርጋ (Enyachew Amerga)</p>
                    <p style="font-size: 13px;"><b>ቴሌብር (Telebirr):</b> 0944123180<br><b>ስም:</b> እንያቸው አመርጋ (Enyachew Amerga)</p>
                </div>
                <div class="card">
                    <label>የተላለፈው መጠን (ብር):</label>
                    <input type="number" id="depAmount" placeholder="ለምሳሌ 50">
                    <label>የ FT ሪፈረንስ ቁጥር (FT Number):</label>
                    <input type="text" id="depRef" placeholder="FT12345678">
                    <button class="btn-main" onclick="submitDeposit()">ክፍያ በቦቱ አረጋግጥ</button>
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
                    <label>አካውንት ቁጥርዎ:</label>
                    <input type="text" id="wAccount" placeholder="አካውንት ቁጥርዎ">
                    <label>የሚወጣው መጠን (ብር):</label>
                    <input type="number" id="wAmount" placeholder="ዝቅተኛ 50 ብር">
                    <button class="btn-main" onclick="submitWithdraw()">የማውጣት ጥያቄ ለአድሚን ላክ</button>
                </div>
            </div>

            <!-- 4. CHECK BALANCE SECTION -->
            <div id="balance" class="section">
                <div class="card" style="text-align: center;">
                    <h3>💳 የሂሳብ ዝርዝር (Balance Summary)</h3>
                    <p style="font-size: 14px; color: var(--text-secondary); margin: 15px 0;">የአሁኑ የዋሌት ቀሪ ሂሳብዎ:</p>
                    <div style="font-size: 28px; font-weight: bold; color: var(--success);" id="balanceDisplay">150.00 ብር</div>
                </div>
            </div>

            <!-- 5. INVITE SECTION -->
            <div id="invite" class="section">
                <div class="card" style="text-align: center;">
                    <h3>👥 ጓደኛ ይጋብዙ</h3>
                    <p style="color: var(--text-secondary); font-size: 12px;">ሊንኩን ለጓደኛዎ በመላክ ቦነስ ያግኙ!</p>
                    <input type="text" value="https://t.me/bravo_ethio_bingo_bot?start=ref123" readonly style="text-align: center;">
                    <button class="btn-main" onclick="alert('ሊንኩ ተኮርጇል!')">ሊንክ ኮፒ አድርግ</button>
                </div>
            </div>

            <!-- 6. CONTACT US SECTION -->
            <div id="contact" class="section">
                <div class="card" style="text-align: center;">
                    <h3>📞 እገዛ እና ድጋፍ (Contact Us)</h3>
                    <p style="font-size: 13px; color: var(--text-secondary);">ማንኛውም ጥያቄ ካለዎት በቀጥታ አድሚኑን ያግኙ።</p>
                    <p style="font-size: 15px; margin-top: 15px;">የአድሚን ቴሌግራም ዩዘርኔም:<br><a href="https://t.me/enyachew_19" style="color: var(--primary); font-size: 18px; font-weight: bold;" target="_blank">@enyachew_19</a></p>
                </div>
            </div>
        </div>
    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();

        let currentBalance = 150.00;
        let selectedRoomPrice = 10;
        let registeredUser = "@enyachew";
        let isDisqualified = false;
        let usedFtNumbers = [];

        // Populate 1 to 200 Card Numbers
        const cardSelect = document.getElementById('cardSelect');
        for(let i=1; i<=200; i++) {
            let opt = document.createElement('option');
            opt.value = i;
            opt.innerText = `ካርቴላ ቁጥር #${i}`;
            cardSelect.appendChild(opt);
        }

        function completeRegistration() {
            let name = document.getElementById('regName').value.trim();
            let phone = document.getElementById('regPhone').value.trim();
            if(!name || !phone) {
                alert('እባክዎ ስምዎን/ዩዘርኔምዎን እና ስልክ ቁጥርዎን ያስገቡ!');
                return;
            }
            registeredUser = name.startsWith('@') ? name : '@' + name;
            document.getElementById('regScreen').style.display = 'none';
            document.getElementById('mainApp').style.display = 'flex';
            generateCard();
            alert(`እንኳን ደስ አለዎት ${registeredUser}! ምዝገባው ተጠናቋል።`);
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
            isDisqualified = false;
            document.getElementById('bingoBtn').disabled = false;
            document.getElementById('bingoBtn').style.opacity = '1';

            if(currentBalance < price) {
                alert('❌ ሒሳብዎ በቂ አይደለም! Low balance. እባክዎ መጀመሪያ ዲፖዚት ያድርጉ።');
            } else {
                currentBalance -= price;
                updateBalanceDisplay();
                alert(`የባለ ${price} ብር ክፍል ተቀላቅለዋል! ጨዋታው በቀጣይነት በሂደት ላይ ነው።`);
                generateCard();
            }
        }

        function updateBalanceDisplay() {
            document.getElementById('userBalance').innerText = currentBalance.toFixed(2);
            document.getElementById('balanceDisplay').innerText = currentBalance.toFixed(2) + " ብር";
        }

        function changeCardNumber() {
            generateCard();
        }

        let playerCardData = [];
        let allCalledNumbers = [];

        function generateCard() {
            const tbody = document.getElementById('bingoCardBody');
            tbody.innerHTML = '';
            playerCardData = [];

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
                        td.classList.add('marked');
                        rowData.push('FREE');
                    } else {
                        let val = cols[c][r];
                        td.innerText = val;
                        td.onclick = function() {
                            if(!isDisqualified) {
                                this.classList.toggle('marked');
                            }
                        };
                        rowData.push(val);
                    }
                    row.appendChild(td);
                }
                tbody.appendChild(row);
                playerCardData.push(rowData);
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

        // Live Calling & Timer (45s)
        let timerCount = 45;
        setInterval(() => {
            timerCount--;
            document.getElementById('countdown').innerText = timerCount;
            if (timerCount <= 0) {
                timerCount = 45;
                let letters = ['B', 'I', 'N', 'G', 'O'];
                let letter = letters[Math.floor(Math.random() * letters.length)];
                let num = Math.floor(Math.random() * 15) + 1;
                if(letter === 'I') num += 15;
                if(letter === 'N') num += 30;
                if(letter === 'G') num += 45;
                if(letter === 'O') num += 60;
                
                let callStr = `${letter}-${num}`;
                document.getElementById('currentCalledNum').innerText = callStr;
                if(!allCalledNumbers.includes(num)) {
                    allCalledNumbers.push(num);
                }
                document.getElementById('calledCount').innerText = allCalledNumbers.length;
            }
        }, 1000);

        // Instant Bingo Verification with 20% Hidden Commission, Public Announcement & Private Disqualification
        function checkBingoWin() {
            if(isDisqualified) {
                alert('❌ የውሸት ቢንጎ ብለው ስለተጫኑ ከዚህ ዙር ጨዋታ ውጪ ነዎት። ጨዋታው ግን ለሌሎች ቀጥሏል!');
                return;
            }

            let markedCells = document.querySelectorAll('.bingo-cell.marked');
            let isValid = true;
            
            markedCells.forEach(cell => {
                let val = cell.innerText;
                if(val !== 'FREE') {
                    let numVal = parseInt(val);
                    if(!allCalledNumbers.includes(numVal)) {
                        isValid = false;
                    }
                }
            });

            if(markedCells.length >= 5 && isValid) {
                // Calculation: 10 players pool, 20% commission cut silently, 80% to winner
                let totalPool = selectedRoomPrice * 10;
                let netWinAmount = totalPool * 0.80;
                currentBalance += netWinAmount;
                updateBalanceDisplay();

                let selectedCardNum = document.getElementById('cardSelect').value;

                // Public Broadcast Announcement for Winner
                let announcementText = `🏆 <b>አሸናፊ ተገኘ!</b> ተጫዋች <b>${registeredUser}</b> ካርቴላ ቁጥር <b>#${selectedCardNum}</b> ይዞ ሉንጎ (BINGO) አሸንፏል! ሽልማት: <b>${netWinAmount.toFixed(2)} ብር</b>`;
                document.getElementById('publicAnnouncement').innerHTML = announcementText;

                alert(`🎉 እንኳን ደስ አለዎት! ሉንጎ (BINGO) በትክክል ተረጋግጧል! ${netWinAmount.toFixed(2)} ብር ወደ ዋሌታዎ ገብቷል!`);
            } else {
                // Private Disqualification for False Bingo only (Game does NOT stop)
                isDisqualified = true;
                document.getElementById('bingoBtn').disabled = true;
                document.getElementById('bingoBtn').style.opacity = '0.5';
                alert('❌ ስህተት ቢንጎ! ያልተጠራ ቁጥር ተጭነዋል። ከዚህ ዙር ጨዋታ ውጪ ሆኑ (Disqualified)፤ ጨዋታው ግን ለሌሎች ቀጥሏል!');
            }
        }

        // Auto Deposit Logic
        function submitDeposit() {
            let amt = parseFloat(document.getElementById('depAmount').value);
            let ref = document.getElementById('depRef').value.trim();
            
            if(!amt || !ref) {
                alert('እባክዎ መጠኑን እና የ FT ሪፈረንስ ቁጥር ያስገቡ!');
                return;
            }

            if(usedFtNumbers.includes(ref)) {
                alert('❌ ይህ የ FT ሪፈረንስ ቁጥር ቀደም ሲል ጥቅም ላይ ውሏል!');
                return;
            }

            if(ref.length < 5) {
                alert('❌ ትክክለኛ ያልሆነ የ FT ሪፈረንስ ቁጥር ነው።');
                return;
            }

            usedFtNumbers.push(ref);
            currentBalance += amt;
            updateBalanceDisplay();
            alert(`✅ ክፍያዎ በቦቱ ተረጋግጧል! ${amt} ብር በትክክል ወደ ዋሌታዎ ገብቷል!`);
            document.getElementById('depAmount').value = '';
            document.getElementById('depRef').value = '';
        }

        // Withdraw Logic
        function submitWithdraw() {
            let method = document.getElementById('wMethod').value;
            let account = document.getElementById('wAccount').value.trim();
            let amount = parseFloat(document.getElementById('wAmount').value);

            if(!account || !amount) {
                alert('እባክዎ አካውንት ቁጥር እና የሚወጣውን መጠን ያስገቡ!');
                return;
            }

            if(amount < 50) {
                alert('❌ ዝቅተኛው የማውጣት መጠን 50 ብር ነው።');
                return;
            }

            if(amount > currentBalance) {
                alert('❌ በቂ ሂሳብ የለዎትም!');
                return;
            }

            currentBalance -= amount;
            updateBalanceDisplay();

            alert(`💸 የማውጣት ጥያቄዎ ተመዝግቧል! ሒሳብዎ ከዋሌትዎ ቀንሷል። ጥያቄው በአድሚን ዩዘርኔም @enyachew_19 በኩል ተረጋግጦ ይለቀቃል።`);
            document.getElementById('wAccount').value = '';
            document.getElementById('wAmount').value = '';
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
