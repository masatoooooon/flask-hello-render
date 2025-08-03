import os
import random
import io
from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from zoneinfo import ZoneInfo # ★変更点: タイムゾーンを扱うライブラリをインポート

app = Flask(__name__)

# --- 画像処理関数 (変更なし) ---
OUTPUT_SINGLE_SIZE = (1920, 1080)

def generate_source_image(data):
    w, h = OUTPUT_SINGLE_SIZE
    if hasattr(data, 'filename') and data.filename != '':
        try:
            image = Image.open(data.stream)
            if image.height > image.width:
                image = image.rotate(90, expand=True)
            return image.resize((w, h), Image.Resampling.LANCZOS)
        except:
            return None
    elif isinstance(data, tuple):
        return Image.new("RGB", (w, h), color=data)
    return None

def create_combined_image(final_sources, layout):
    w, h = OUTPUT_SINGLE_SIZE
    if layout == "5x1":
        combined_image = Image.new("RGB", (w * 5, h))
        num_to_use = 5
    elif layout == "4x1":
        combined_image = Image.new("RGB", (w * 4, h))
        num_to_use = 4
    else: # "2x2"
        combined_image = Image.new("RGB", (w * 2, h * 2))
        num_to_use = 4
    for i in range(num_to_use):
        data = final_sources[i]
        image = generate_source_image(data)
        if image is None:
            image = Image.new("RGB", OUTPUT_SINGLE_SIZE, (240, 240, 240))
        if layout in ["4x1", "5x1"]:
            x_offset, y_offset = i * w, 0
        else: # "2x2"
            x_offset, y_offset = (i % 2) * w, (i // 2) * h
        combined_image.paste(image, (x_offset, y_offset))
    return combined_image

# --- Flaskのルート部分 ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/combine', methods=['POST'])
def combine():
    try:
        files = request.files.getlist('image_files')
        layout = request.form.get('layout')
        
        if layout == "5x1": num_required = 5
        elif layout == "4x1": num_required = 4
        else: num_required = 4
        
        final_sources = list(files)
        used_colors = set()
        for i in range(num_required):
            if i >= len(final_sources) or not final_sources[i].filename:
                final_sources.insert(i, None)
            if final_sources[i] is None:
                random_color = tuple(random.randint(0, 255) for _ in range(3))
                while random_color in used_colors:
                    random_color = tuple(random.randint(0, 255) for _ in range(3))
                used_colors.add(random_color)
                final_sources[i] = random_color
        
        combined_image = create_combined_image(final_sources, layout)
        
        img_io = io.BytesIO()
        combined_image.save(img_io, 'JPEG', quality=95)
        img_io.seek(0)
        
        # ★変更点: 日本時間(JST)を指定してタイムスタンプを生成
        jst = ZoneInfo("Asia/Tokyo")
        timestamp = datetime.now(jst).strftime("%y%m%d%H%M%S")
        download_filename = f'{layout}_{timestamp}.jpg'
        
        return send_file(
            img_io,
            mimetype='image/jpeg',
            as_attachment=True,
            download_name=download_filename
        )

    except Exception as e:
        return f"エラーが発生しました: {e}", 500

# --- Renderで動作させるための設定 ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
