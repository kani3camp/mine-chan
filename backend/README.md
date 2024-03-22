

## Windowsの場合
### venvに入る
```bash
./env/Scripts/activate
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