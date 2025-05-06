from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(TEMPLATE)

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Live QR Code Scanner</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- html5-qrcode CDN -->
    <script src="https://unpkg.com/html5-qrcode@2.3.8/html5-qrcode.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: #f7f9fa;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 420px;
            margin: 40px auto;
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            padding: 32px 24px;
            text-align: center;
        }
        h1 {
            color: #234567;
            margin-bottom: 12px;
        }
        #reader {
            margin: 0 auto 16px auto;
            width: 320px;
        }
        .result-box {
            background: #e6f7e6;
            color: #1a5d1a;
            border: 1px solid #b6e3b6;
            border-radius: 8px;
            padding: 16px;
            margin-top: 18px;
            word-break: break-all;
            font-size: 1.08em;
            text-align: left;
            display: inline-block;
        }
        .footer {
            margin-top: 30px;
            color: #aaa;
            font-size: 0.95em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Live QR Code Scanner</h1>
        <div id="reader"></div>
        <div id="result" class="result-box" style="display:none;"></div>
    </div>
    <script>
        function parseVCard(vcard) {
            // Extract FN, TEL, EMAIL
            let name = '';
            let phone = '';
            let email = '';
            let lines = vcard.split(/\\r?\\n/);
            for (let line of lines) {
                if (line.startsWith('FN:')) {
                    name = line.substring(3).trim();
                }
                if (line.startsWith('TEL')) {
                    let idx = line.indexOf(':');
                    if (idx !== -1) phone = line.substring(idx+1).trim();
                }
                if (line.startsWith('EMAIL')) {
                    let idx = line.indexOf(':');
                    if (idx !== -1) email = line.substring(idx+1).trim();
                }
            }
            let result = '';
            if (name) result += `<b>Name:</b> ${name}<br>`;
            if (phone) result += `<b>Phone:</b> ${phone}<br>`;
            if (email) result += `<b>Email:</b> ${email}`;
            return result || "No valid vCard data found.";
        }

        function onScanSuccess(decodedText, decodedResult) {
            let resultBox = document.getElementById('result');
            // Check if it's a vCard
            if (decodedText.startsWith('BEGIN:VCARD')) {
                resultBox.innerHTML = parseVCard(decodedText);
            } else {
                resultBox.innerText = decodedText;
            }
            resultBox.style.display = 'block';
            html5QrcodeScanner.clear();
        }
        function onScanFailure(error) {
            // Optionally handle scan errors
        }
        let html5QrcodeScanner = new Html5QrcodeScanner(
            "reader", { fps: 10, qrbox: 250 });
        html5QrcodeScanner.render(onScanSuccess, onScanFailure);
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
