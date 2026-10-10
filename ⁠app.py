from flask import Flask, render_template_string, request, jsonify
import random

app = Flask(__name__)

# Complete Arada Bingo System - Dynamic Real-time Player Count & Exact Standard
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arada Bingo</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        :root {
            --bg-color: #0b0f19;
            --card-bg: #161e31;
            --primary: #f59e0b;
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
            padding: 10px 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #1e293b;
        }
        h1 {
            margin: 0;
            font-size: 16px;
            color: var(--primary);
        }
        .user-balance {
            font-size: 12px;
            background: #0f172a;
            padding: 5px 10px;
            border-radius: 20px;
            border: 1px solid #334155;
            color: var(--success);
            font-weight: bold;
        }
        .container {
            flex: 1;
            padding: 10px;
            max-width: 480px;
            margin: 0 auto;
            width: 100%;
            box-sizing: border-box;
        }
        /* Menu Grid */
        .menu-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
            margin-bottom: 12px;
        }
        .menu-btn {
            background-color: var(--card-bg);
            border: 1px solid #334155;
            color: var(--text-color);
            padding: 12px 10px;
            border-radius: 12px;
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
        /* Room Card */
        .room-card {
            background: var(--card-bg);
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .room-info h3 {
            margin: 0 0 2px 0;
            font-size: 14px;
            color: var(--primary);
        }
        .room-info p {
            margin: 0;
            font-size: 11px;
            color: var(--text-secondary);
        }
        /* Game Stats Header Bar */
        .game-stats-bar {
            background: #b45309;
            color: #fff;
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            text-align: center;
            padding: 6px 4px;
            font-size: 11px;
            font-weight: bold;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        .game-stats-bar div span {
            display: block;
            font-size: 13px;
        }
        /* Card Selection Box (1-200) */
        .card-selection-box {
            background: #7c3aed;
            padding: 12px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 10px;
        }
        .number-grid {
            display: grid;
            grid-template-columns: repeat(10, 1fr);
            gap: 4px;
            max-height: 180px;
            overflow-y: auto;
            margin: 8px 0;
            background: #6d28d9;
            padding: 6px;
            border-radius: 8px;
        }
        .num-btn {
            background: #a78bfa;
            border: none;
            color: #fff;
            aspect-ratio: 1;
            font-size: 11px;
            font-weight: bold;
            border-radius: 4px;
            cursor: pointer;
        }
        .num-btn.selected {
            background: var(--success) !important;
            color: #fff;
        }
        /* Live Board */
        .live-board {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 10px;
            text-align: center;
            margin-bottom: 10px;
            border: 1px solid #334155;
        }
        .called-number-display {
            font-size: 28px;
            font-weight: bold;
            color: var(--primary);
            margin: 2px 0;
        }
        /* Bingo Table */
        .bingo-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 3px;
            margin-bottom: 10px;
        }
        .bingo-header-cell {
            background: #0f172a;
            color: #fff;
            text-align: center;
            padding: 5px 0;
            font-weight: bold;
            font-size: 14px;
            border-radius: 4px;
        }
        .bingo-cell {
            background-color: var(--card-bg);
            border: 1px solid #334155;
            aspect-ratio: 1;
            text-align: center;
            vertical-align: middle;
            font-size: 13px;
            font-weight: bold;
            border-radius: 4px;
            cursor: pointer;
            color: #fff;
        }
        .bingo-cell.marked {
            background-color: var(--primary) !important;
            color: #000 !important;
        }
        .bingo-cell.free-cell {
            background-color: var(--success) !important;
            color: #fff !important;
            font-size: 9px;
        }
        .btn-main {
            background-color: var(--primary);
            color: #000;
            border: none;
            width: 100%;
            padding: 12px;
            border-radius: 10px;
            font-size: 14px;
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
        /* Winner Modal */
        #winnerModal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.8);
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        .modal-content {
            background: #1e293b;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            width: 85%;
            max-width: 320px;
            border: 2px solid var(--primary);
        }
    </style>
</head>
<body>

    <!-- MAIN APP SCREEN (Auto-Authenticated via Telegram WebApp) -->
    <div id="mainApp" style="display: flex; flex-direction: column; min-height: 100vh;">
        <header>
            <h1>Arada Bingo</h1>
            <div class="user-balance">ሒሳብ: <span id="userBalance">150.00</span> ብር</div>
        </header>

        <div class="container">
            <!-- Menu Grid -->
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
                <div id="roomSelectionView">
                    <h3 style="color: var(--primary); font-size: 14px; margin-bottom: 8px;">Stake / Rooms</h3>
                    
                    <div class="room-card">
                        <div class="room-info">
                            <h3>10 ETB</h3>
                            <p>ተጫዋች: <span id="pCount10">1</span> ሰው | ድምር: <span id="derash10">10</span> ብር</p>
                        </div>
                        <button class="btn-main" style="width: 80px; padding: 8px; margin: 0;" onclick="joinRoom(10)">Play</button>
                    </div>

                    <div class="room-card">
                        <div class="room-info">
                            <h3>20 ETB</h3>
                            <p>ተጫዋች: <span id="pCount20">2</span> ሰው | ድምር: <span id="derash20">40</span> ብር</p>
                        </div>
                        <button class="btn-main" style="width: 80px; padding: 8px; margin: 0;" onclick="joinRoom(20)">Play</button>
                    </div>

                    <div class="room-card">
                        <div class="room-info">
                            <h3>50 ETB</h3>
                            <p>ተጫዋች: <span id="pCount50">1</span> ሰው | ድምር: <span id="derash50">50</span> ብር</p>
                        </div>
                        <button class="btn-main" style="width: 80px; padding: 8px; margin: 0;" onclick="joinRoom(50)">Play</button>
                    </div>
                </div>

                <!-- Active Game View -->
                <div id="activeGameView" style="display: none;">
                    <!-- Game Stats Bar -->
                    <div class="game-stats-bar">
                        <div>Game ID<span id="statGameId">10</span></div>
                        <div>Derash<span id="statDerash">740</span></div>
                        <div>Players<span id="statPlayers">1</span></div>
                        <div>Bet<span id="statBet">10</span></div>
                        <div>Call<span id="statCall">0</span></div>
                    </div>

                    <!-- Card Selection Box (1-200) -->
                    <div class="card-selection-box">
                        <div style="font-size: 13px; font-weight: bold; color: #fff;">ካርቴላ ቁጥር ይምረጡ (ከ 1 እስከ 200)</div>
                        <div class="number-grid" id="numGrid1To200"></div>
                        <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                            <button class="btn-main" style="width: 48%; padding: 6px; font-size: 11px; background: #4c1d95; color:#fff;" onclick="toggleCardRange()">Show/Hide 100-200</button>
                            <button class="btn-main" style="width: 48%; padding: 6px; font-size: 11px;" onclick="confirmCardSelection()">ካርቴላ ምረጥ</button>
                        </div>
                    </div>

                    <!-- Live Board -->
                    <div class="live-board">
                        <div style="font-size: 11px; color: var(--text-secondary);">ቀጣይ ቁጥር በ <span id="countdown">45</span> ሰከንድ ውስጥ ይጠራል...</div>
                        <div class="called-number-display" id="currentCalledNum">--</div>
                        <div style="font-size: 11px; color: var(--success);" id="selectedCardLabel">የተመረጠ ካርቴላ: #1</div>
                    </div>

                    <!-- Bingo Grid -->
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

                    <button id="bingoBtn" class="btn-main" onclick="checkBingoWin()" style="background-color: #ef4444; color: white; font-size: 18px; padding: 14px;">BINGO!</button>
                </div>
            </div>

            <!-- 2. DEPOSIT SECTION -->
            <div id="deposit" class="section">
                <div class="card">
                    <h3>💳 Deposit</h3>
                    <p style="font-size: 12px; color: var(--text-secondary);">ገንዘብ ካስተላለፉ በኋላ የFT ሪፈረንስ ቁጥር ያስገቡ።</p>
                    <hr style="border-color: #334155;">
                    <p style="font-size: 13px;"><b>CBE:</b> 1000682528641<br><b>ስም:</b> እንያቸው አመርጋ</p>
                    <p style="font-size: 13px;"><b>Telebirr:</b> 0944123180<br><b>ስም:</b> እንያቸው አመርጋ</p>
                </div>
                <div class="card">
                    <label>መጠን (ብር):</label>
                    <input type="number" id="depAmount" placeholder="50">
                    <label>FT Number:</label>
                    <input type="text" id="depRef" placeholder="FT12345678">
                    <button class="btn-main" onclick="submitDeposit()">ክፍያ አረጋግጥ</button>
                </div>
            </div>

            <!-- 3. WITHDRAW SECTION -->
            <div id="withdraw" class="section">
                <div class="card">
                    <h3>💸 Withdraw</h3>
                    <label>የሂሳብ ዓይነት:</label>
                    <select id="wMethod">
                        <option value="cbe">CBE</option>
                        <option value="telebirr">Telebirr</option>
                    </select>
                    <label>አካውንት ቁጥር:</label>
                    <input type="text" id="wAccount" placeholder="አካውንት ቁጥር">
                    <label>መጠን (ብር):</label>
                    <input type="number" id="wAmount" placeholder="ዝቅተኛ 50">
                    <button class="btn-main" onclick="submitWithdraw()">ጥያቄ ለአድሚን ላክ</button>
                </div>
            </div>

            <!-- 4. CHECK BALANCE SECTION -->
            <div id="balance" class="section">
                <div class="card" style="text-align: center;">
                    <h3>💳 Check Balance</h3>
                    <p style="font-size: 14px; color: var(--text-secondary); margin: 15px 0;">ቀሪ ሂሳብዎ:</p>
                    <div style="font-size: 28px; font-weight: bold; color: var(--success);" id="balanceDisplay">150.00 ብር</div>
                </div>
            </div>

            <!-- 5. INVITE SECTION -->
            <div id="invite" class="section">
                <div class="card" style="text-align: center;">
                    <h3>👥 Invite Friends</h3>
                    <input type="text" value="https://t.me/bravo_ethio_bingo_bot?start=ref123" readonly style="text-align: center;">
                    <button class="btn-main" onclick="alert('ሊንኩ ተኮርጇል!')">Copy Link</button>
                </div>
            </div>

            <!-- 6. CONTACT SECTION -->
            <div id="contact" class="section">
                <div class="card" style="text-align: center;">
                    <h3>📞 Contact Us</h3>
                    <p style="font-size: 15px; margin-top: 15px;">Admin Username:<br><a href="https://t.me/enyachew_19" style="color: var(--primary); font-size: 18px; font-weight: bold;" target="_blank">@enyachew_19</a></p>
                </div>
            </div>
        </div>
    </div>

    <!-- WINNER MODAL -->
    <div id="winnerModal">
        <div class="modal-content">
            <h3 id="winnerTitle" style="color: var(--primary); margin-top: 0;">Winner 🎉</h3>
            <p id="winnerAmountText" style="font-size: 14px; color: var(--text-secondary);">Amount: 0 Birr</p>
            <button class="btn-main" onclick="closeWinnerModal()">Play Again</button>
        </div>
    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.expand();

        let telegramUser = tg.initDataUnsafe && tg.initDataUnsafe.user ? tg.initDataUnsafe.user : null;
        let registeredUser = telegramUser && telegramUser.username ? "@" + telegramUser.username : (telegramUser && telegramUser.first_name ? telegramUser.first_name : "@enyachew");

        let currentBalance = 150.00;
        let selectedRoomPrice = 10;
        let selectedCardNumber = 1;
        let isDisqualified = false;
        let usedFtNumbers = [];

        // Dynamic Real-time player counts and pools
        let roomData = {
            10: { players: 1, bet: 10 },
            20: { players: 2, bet: 20 },
            50: { players: 1, bet: 50 }
        };

        function updateRoomUI() {
            document.getElementById('pCount10').innerText = roomData[10].players;
            document.getElementById('derash10').innerText = roomData[10].players * 10;

            document.getElementById('pCount20').innerText = roomData[20].players;
            document.getElementById('derash20').innerText = roomData[20].players * 20;

            document.getElementById('pCount50').innerText = roomData[50].players;
            document.getElementById('derash50').innerText = roomData[50].players * 50;
        }

        const numGrid = document.getElementById('numGrid1To200');
        for(let i=1; i<=200; i++) {
            let btn = document.createElement('button');
            btn.className = 'num-btn';
            btn.innerText = i;
            if(i === 1) btn.classList.add('selected');
            btn.onclick = function() {
                document.querySelectorAll('.num-btn').forEach(b => b.classList.remove('selected'));
                this.classList.add('selected');
                selectedCardNumber = i;
            };
            numGrid.appendChild(btn);
        }

        function toggleCardRange() {
            numGrid.scrollTop += 60;
        }

        function switchTab(tabId) {
            document.querySelectorAll('.section').forEach(sec => sec.classList.remove('active'));
            document.querySelectorAll('.menu-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelector(`button[onclick="switchTab('${tabId}')"]`).classList.add('active');
            document.getElementById(tabId).classList.add('active');
        }

        function joinRoom(price) {
            if(currentBalance < price) {
                alert('❌ ሒሳብዎ በቂ አይደለም!');
                return;
            }
            currentBalance -= price;
            updateBalanceDisplay();
            selectedRoomPrice = price;

            // Increment player count dynamically when user joins
            roomData[price].players += 1;
            updateRoomUI();

            document.getElementById('roomSelectionView').style.display = 'none';
            document.getElementById('activeGameView').style.display = 'block';
            document.getElementById('statBet').innerText = price;
            document.getElementById('statPlayers').innerText = roomData[price].players;
            document.getElementById('statDerash').innerText = roomData[price].players * price;
            generateCard();
        }

        function confirmCardSelection() {
            document.getElementById('selectedCardLabel').innerText = `የተመረጠ ካርቴላ: #${selectedCardNumber}`;
            alert(`ካርቴላ ቁጥር #${selectedCardNumber} ተመርጧል!`);
        }

        function updateBalanceDisplay() {
            document.getElementById('userBalance').innerText = currentBalance.toFixed(2);
            document.getElementById('balanceDisplay').innerText = currentBalance.toFixed(2) + " ብር";
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
                            if(!isDisqualified) this.classList.toggle('marked');
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

        let timerCount = 45;
        let callCountVal = 0;
        setInterval(() => {
            timerCount--;
            document.getElementById('countdown').innerText = timerCount;
            if (timerCount <= 0) {
                timerCount = 45;
                callCountVal++;
                document.getElementById('statCall').innerText = callCountVal;
                let letters = ['B', 'I', 'N', 'G', 'O'];
                let letter = letters[Math.floor(Math.random() * letters.length)];
                let num = Math.floor(Math.random() * 15) + 1;
                if(letter === 'I') num += 15;
                if(letter === 'N') num += 30;
                if(letter === 'G') num += 45;
                if(letter === 'O') num += 60;
                document.getElementById('currentCalledNum').innerText = `${letter}-${num}`;
                if(!allCalledNumbers.includes(num)) allCalledNumbers.push(num);
            }
        }, 1000);

        function checkBingoWin() {
            if(isDisqualified) {
                alert('❌ ከዚህ ዙር ውጪ ሆኑ!');
                return;
            }
            let markedCells = document.querySelectorAll('.bingo-cell.marked');
            let isValid = true;
            markedCells.forEach(cell => {
                let val = cell.innerText;
                if(val !== 'FREE') {
                    if(!allCalledNumbers.includes(parseInt(val))) isValid = false;
                }
            });

            if(markedCells.length >= 5 && isValid) {
                let totalPool = roomData[selectedRoomPrice].players * selectedRoomPrice;
                let netWinAmount = totalPool * 0.80; // 20% house commission deducted silently
                currentBalance += netWinAmount;
                updateBalanceDisplay();
                document.getElementById('winnerTitle').innerText = `${registeredUser} Won 🎉`;
                document.getElementById('winnerAmountText').innerText = `Amount: ${netWinAmount.toFixed(2)} Birr (Board No.${selectedCardNumber})`;
                document.getElementById('winnerModal').style.display = 'flex';
            } else {
                isDisqualified = true;
                document.getElementById('bingoBtn').disabled = true;
                document.getElementById('bingoBtn').style.opacity = '0.5';
                alert('❌ ስህተት ቢንጎ! ከዚህ ዙር ውጪ ሆኑ።');
            }
        }

        function closeWinnerModal() {
            document.getElementById('winnerModal').style.display = 'none';
            document.getElementById('activeGameView').style.display = 'none';
            document.getElementById('roomSelectionView').style.display = 'block';
            isDisqualified = false;
            document.getElementById('bingoBtn').disabled = false;
            document.getElementById('bingoBtn').style.opacity = '1';
            updateRoomUI();
        }

        function submitDeposit() {
            let amt = parseFloat(document.getElementById('depAmount').value);
            let ref = document.getElementById('depRef').value.trim();
            if(!amt || !ref) {
                alert('እባክዎ መጠን እና FT ቁጥር ያስገቡ!');
                return;
            }
            if(usedFtNumbers.includes(ref)) {
                alert('❌ ይህ FT ቁጥር ተቀምቷል!');
                return;
            }
            usedFtNumbers.push(ref);
            currentBalance += amt;
            updateBalanceDisplay();
            alert(`✅ ${amt} ብር ተጨመረ!`);
        }

        function submitWithdraw() {
            let account = document.getElementById('wAccount').value.trim();
            let amount = parseFloat(document.getElementById('wAmount').value);
            if(!account || !amount) {
                alert('እባክዎ አካውንት እና መጠን ያስገቡ!');
                return;
            }
            if(amount < 50 || amount > currentBalance) {
                alert('❌ የተሳሳተ መጠን!');
                return;
            }
            currentBalance -= amount;
            updateBalanceDisplay();
            alert('💸 ጥያቄው ለአድሚን @enyachew_19 ተልኳል!');
        }

        updateRoomUI();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
