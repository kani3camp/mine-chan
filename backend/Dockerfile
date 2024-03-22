FROM python:3.12-slim
RUN apt-get -y update && apt-get -y upgrade
WORKDIR root

RUN mkdir app
#main.pyを/root/appに以下にコピー。
COPY app/main.py app/
#requirements.txtをコンテナ内のroot配下にコピー。
COPY requirements.txt requirements.txt
# コンテナ起動時にモジュールをインストール。
RUN pip install -r requirements.txt
#コンテナ起動時に実行するコマンドを指定。
ENTRYPOINT ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]