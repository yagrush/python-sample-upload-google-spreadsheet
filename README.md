# python-sample-upload-google-spreadsheet

TSVデータをGoogleスプレッドシートにアップロードする

## run on docker container
### up
```
make up
```

### down container with clearing cache
```
make down-v
```

## development setup
### GCP
GCPで以下の手順を実施しておく必要がある
1. プロジェクト作成（必要であれば
2. Google Drive API 有効化
3. Google Sheets API 有効化
4. OAuth 同意画面の設定
5. 認証情報の作成
6. client_secret_***************.jsonをダウンロード

### local
```
python -m venv .venv
chmod 777 .venv/bin/activate
source ./.venv/bin/activate

pip install pytest
pip install gspread
pip install python-dotenv
pip install PyYAML
```

### `client_secret_***************.json`を配備する
GCPからダウンロードした `client_secret_***************.json` をプロジェクトルートに置く

### `.env` を作成する
このプロジェクト直下に、.env.exampleを参考にして .env を作成する
* CLIENT_SECRET_JSON_FILE
  GCPからダウンロードした client_secret_***************.json ファイル名
* AUTHORIZED_USER_JSON_FILE
  特に変更しなくて良い
* GOOGLE_SPREADSHEET_UPLOAD_FOLDER_ID
  GoogleスプレッドシートをアップロードしたいGoogleドライブフォルダのID
* GOOGLE_SPREADSHEET_UPLOAD_FILE_NAME
  アップロードしたいGoogleスプレッドシート名
* GOOGLE_SPREADSHEET_WORKSHEET_NAME
  データを書き込みたいGoogleスプレッドシート内のシート名
* FILENAME_DATA_TSV
  データTSVファイル名

## development tips
### to exit venv
venvを抜けたい時
```
deactivate
```

### output requirements.txt
新しいライブラリをimportした場合に必ず実行してください
```
make req
```
