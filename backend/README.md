
## .env（環境変数ファイル）の準備
```dotenv
GOOGLE_CREDENTIALS
```

## venvを作成
### windowsの場合
uvを使用。
```shell
uv venv
```

### macの場合
```bash
python -m venv venv
```


## venvに入る
### windowsの場合
```bash
.venv/Scripts/activate
```

### macの場合
```bash
source env/bin/activate
```

## 依存パッケージをインストール
```bash
pip install -r requirements.txt
```
uvの場合
```shell
uv pip sync requirements.txt
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
