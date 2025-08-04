import os
import random
import io
from flask import Flask, render_template, request, send_file
from PIL import Image
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)

# --- 画像処理関数 (変更なし) ---
# ... (長いので省略) ...

# --- Flaskのルート部分 ---
@app.route('/')
def index():
    return render_template('index.html')

# ★変更点: この関数を追加
@app.route('/manual')
def manual():
    return render_template('manual.html')

@app.route('/combine', methods=['POST'])
def combine():
    # ... (この関数の中身は変更なし) ...
    try:
        # ...
    except Exception as e:
        return f"エラーが発生しました: {e}", 500

# --- Renderで動作させるための設定 (変更なし) ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
