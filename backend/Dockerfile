FROM python:3.12-slim

# システムパッケージの更新と必要なパッケージのインストール
RUN apt-get -y update && apt-get -y upgrade && \
    apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

# 作業ディレクトリの作成
WORKDIR /app

# 依存関係を先にコピーしてインストール（キャッシュの活用）
COPY requirements.txt .

# デバッグ: /app ディレクトリの内容を確認
RUN ls -l /app

# pip のアップグレード
RUN python -m pip install --upgrade pip

# Pythonパッケージのインストールと確認
RUN python -m pip install --no-cache-dir -r requirements.txt && \
    python -m pip list

# アプリケーションコードをコピー
COPY . .

# ポートのエクスポート
EXPOSE 8080

# 環境変数の設定
ENV HOSTNAME "0.0.0.0"
ENV PORT 8080

# Uvicorn サーバーの起動コマンド
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
