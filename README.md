# python-sample-upload-google-spreadsheet

TSVデータをGoogleスプレッドシートにアップロードする
Upload TSV data to Google Sheets

## initial setup
### GCP
GCPで以下の手順を実施しておく必要がある
You need to perform the following steps on GCP.
1. create GCP project (as needed)
2. Google Drive API 有効化 https://console.cloud.google.com/apis/api/drive.googleapis.com/
3. Google Sheets API 有効化 https://console.cloud.google.com/apis/api/sheets.googleapis.com/
4. OAuth 同意画面の設定 https://console.cloud.google.com/apis/credentials/
5. 認証情報の作成 https://console.cloud.google.com/apis/credentials/consent
6. download : client_secret_***************.json

### place `client_secret_***************.json` in this project root directory
GCPからダウンロードした `client_secret_***************.json` をプロジェクトルートに置く

### create `.env`
このプロジェクト直下に、.env.exampleを参考にして .env を作成する
Create .env directly under this project using .env.example as a reference.
* CLIENT_SECRET_JSON_FILE
  filename: client_secret_***************.json
* AUTHORIZED_USER_JSON_FILE
  No need to change anything
* GOOGLE_SPREADSHEET_UPLOAD_FOLDER_ID
  GoogleスプレッドシートをアップロードしたいGoogleドライブフォルダのID
  ID of the Google Drive folder where you want to upload the Google Spreadsheet
* GOOGLE_SPREADSHEET_UPLOAD_FILE_NAME
  アップロードしたいGoogleスプレッドシート名
  Google spreadsheet name you want to upload
* GOOGLE_SPREADSHEET_WORKSHEET_NAME
  データを書き込みたいGoogleスプレッドシート内のシート名
  Sheet name in Google Sheets to which you want to write data
* FILENAME_DATA_TSV
  データTSVファイル名
  Data TSV file name

### run on local

#### setup
```
python -m venv .venv
chmod 777 .venv/bin/activate
source ./.venv/bin/activate

pip install -r requirements.txt
```

#### run
```
make run
```
初回のみ、ブラウザが起動し
* Googleドライブ
* Googleスプレッドシート

へのアクセス許可を求められる
許可したらブラウザを閉じてよい
するとルートディレクトリに authorized_user.json が作成される

##### ブラウザが起動しない時
WSL内シェルなどの環境ではブラウザが起動できないため上記手続きができない
その場合、以下の手順を実行する
1. Windowsのコマンドプロンプトの環境変数PATHにChrome.exeがインストールされているパスを追加
2. 以下のコマンドをコマンドプロンプトで実行
```
cd \\wsl.localhost\Ubuntu\path\to\python-sample-upload-google-spreadsheet
python auth_token.py
```
3. Chromeが起動し authorized_user.json 作成手順が開始される

### run on docker container
authorized_user.json があれば、あとはdockerで実行できる

If you have authorized_user.json, you can run it with docker.

#### up
```
make rund
```

## development tips

### command-line help
```
python -m src -h
```

### run
all args is not required.
default value refers to .env file.
```
python -m src [args...]
```

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

## local dockerでlambda関数として動かす
### ビルド
```
docker-compose -f lambda-docker-compose.yaml up --build -d
```

### 実行
```
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"hogehoge": "fuga"}'
```

### 破棄
```
docker-compose -f lambda-docker-compose.yaml down
```
