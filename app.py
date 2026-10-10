import http.server
import socketserver
import os

PORT = int(os.environ.get("PORT", 10000))

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        html = """
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
                .sub-title { color: #94a3b8; font-size: 14px; margin-bottom: 15px; }
                .card { display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; max-width: 320px; margin: 0 auto; background: #1e293b; padding: 12px; border-radius: 12px; }
                .cell { background: #334155; padding: 14px 0; font-size: 16px; font-weight: bold; border-radius: 6px; cursor: pointer; }
                .cell.marked { background: #22c55e; color: white; }
                .btn-bingo { background: #eab308; color: #000; font-weight: bold; border: none; padding: 14px; font-size: 18px; border-radius: 8px; cursor: pointer; margin-top: 15px; width: 100%; max-width: 320px; }
                .payment-box { background: #1e293b; padding: 12px; border-radius: 12px; max-width: 320px; margin: 15px auto; text-align: left; font-size: 13px; }
                .payment-box h3 { color: #38bdf8; margin: 0 0 8px 0; font-size: 14px; text-align: center; }
            </style>
        </head>
        <body>
            <h1>Ethio Bingo Game</h1>
            <div class="sub-title">እንኳን ወደ ኢትዮ ቢንጎ በደህና መጡ!</div>
            
            <div class="card" id="bingoCard"></div>

            <button class="btn-bingo" onclick="callBingo()">ቢንጎ! (BINGO)</button>

            <div class="payment-box">
                <h3>🏦 የክፍያ አማራጮች</h3>
                <p><b>ንግድ ባንክ (CBE):</b><br>1000682528641<br>ስም፦ እንያቸው አመርጋ</p>
                <p><b>ቴሌብር (Telebirr):</b><br>0944123180<br>ስም፦ እንያቸው አመርጋ</p>
            </div>

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
                    tg.showAlert("ቢንጎ ብለዋል! አሸናፊነትዎ እየተረጋገጠ ነው...");
                }
            </script>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
