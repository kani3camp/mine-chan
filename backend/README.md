

## Windowsの場合
### venvに入る
```bash
./env/Scripts/activate
```

### ローカルで実行
```bash
uvicorn app.main:app
```
#### requirements.txtを最新化
```bash
pip freeze > requirements.txt
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