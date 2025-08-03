from flask import Flask, render_template, request
import os

app = Flask(__name__)

# トップページを表示
@app.route('/')
def index():
    return render_template('index.html')

# ファイルがアップロードされたときの処理
@app.route('/combine', methods=['POST'])
def combine():
    # 複数のファイルを取得
    files = request.files.getlist('image_files')
    # 選択されたレイアウトを取得
    layout = request.form.get('layout')

    # 受け取ったファイルの名前をリストにする
    uploaded_filenames = [f.filename for f in files if f.filename]
    
    # 簡単なデバッグメッセージを生成
    message = (
        f"データを受け取りました！<br>"
        f"選択されたレイアウト: {layout}<br>"
        f"アップロードされたファイル数: {len(uploaded_filenames)}<br>"
        f"ファイル名: {', '.join(uploaded_filenames) if uploaded_filenames else 'なし'}"
    )

    return message

# --- Renderで動作させるための設定 ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
