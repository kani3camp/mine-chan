FROM python:3.12-slim
RUN apt-get -y update && apt-get -y upgrade

EXPOSE 8080
ENV HOSTNAME "0.0.0.0"
ENV PORT 8080

# アプリケーション専用のディレクトリ /app を作成し、ワークディレクトリとして設定
WORKDIR /app

# プロジェクトのルートディレクトリから全てをコンテナのワークディレクトリにコピー
COPY . .

# requirements.txt をコンテナ内の /app にコピー
COPY requirements.txt .

# コンテナ起動時に必要なモジュールをインストール
RUN pip install -r requirements.txt

# コンテナ起動時に実行するコマンドを指定
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
