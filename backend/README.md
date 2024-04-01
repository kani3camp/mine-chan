
## .env（環境変数ファイル）の準備
```dotenv
GOOGLE_CREDENTIALS
```

## venvを作成
### windowsの場合
TODO

### macの場合
```bash
python -m venv venv
```


## venvに入る
### windowsの場合
```bash
./env/Scripts/activate
```

### macの場合
```bash
source env/bin/activate
```

## 依存パッケージをインストール
```bash
pip install -r requirements.txt
```

### ローカルで実行
```bash
uvicorn app.main:app
```
#### requirements.txtを最新化
```bash
pip freeze > requirements.txt
```

## venvから出る
```bash
deactivate
```

### Cloud Runにデプロイする
#### 初めての場合
```bash
gcloud auth login   
```
```bash
gcloud config set project mine-chan
```

```bash
gcloud auth configure-docker
```

#### ビルド、デプロイする
```bash
docker build . -t app 
```
```bash
docker tag app gcr.io/mine-chan/mine-chan-app
```
```bash
docker push gcr.io/mine-chan/mine-chan-app
```