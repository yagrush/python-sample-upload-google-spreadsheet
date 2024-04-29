# python-sample-upload-google-spreadsheet

TSVデータをGoogleスプレッドシートにアップロードするプログラム。

## 事前作業
### GCPの設定
GCPで以下の手順を実施しておく必要がある。

1. プロジェクト作成（必要に応じて）
2. Google Drive API 有効化 https://console.cloud.google.com/apis/api/drive.googleapis.com/
3. Google Sheets API 有効化 https://console.cloud.google.com/apis/api/sheets.googleapis.com/
4. OAuth 同意画面の設定 https://console.cloud.google.com/apis/credentials/
5. 認証情報の作成 https://console.cloud.google.com/apis/credentials/consent
6. 認証情報JSONのダウンロード : client_secret_***************.json
7. ダウンロードした `client_secret_***************.json` をプロジェクトルートに置く。

### `.env`ファイルを作成する
このプロジェクト直下に、.env.exampleを参考にして .env を作成する。
#### CLIENT_SECRET_JSON_FILE
filename: client_secret_***************.json
#### AUTHORIZED_USER_JSON_FILE
（変更不要）
#### GOOGLE_SPREADSHEET_UPLOAD_FOLDER_ID
GoogleスプレッドシートをアップロードしたいGoogleドライブフォルダのID
#### GOOGLE_SPREADSHEET_UPLOAD_FILE_NAME
アップロードしたいGoogleスプレッドシート名
#### GOOGLE_SPREADSHEET_WORKSHEET_NAME
データを書き込みたいGoogleスプレッドシート内のシート名
#### FILENAME_DATA_TSV
データTSVファイル名

### ローカルで一度実行する
`authorized_user.json`を作成するために、ローカルで一度プログラムを実行する必要があります。

#### python実行仮想環境の設定
```
python -m venv .venv
chmod 777 .venv/bin/activate
source ./.venv/bin/activate

pip install -r requirements.txt
```

#### 実行
```
make run
```
初回のみ、ブラウザが起動し

* Googleドライブ
* Googleスプレッドシート

へのアクセス許可を求められる。

許可したらブラウザを閉じてよい。

するとルートディレクトリに `authorized_user.json` が作成される。

##### ブラウザが起動しない場合
WSL内シェルなどの環境ではブラウザが起動できないため上記手続きができない。

その場合、以下の手順を実行する。

1. Windowsのコマンドプロンプトの環境変数PATHにChrome.exeがインストールされているパスを追加
2. 以下のコマンドをコマンドプロンプトで実行
```
cd \\wsl.localhost\Ubuntu\path\to\python-sample-upload-google-spreadsheet
python auth_token.py
```
3. Chromeが起動し authorized_user.json 作成手順が開始される

### dockerとして実行する
authorized_user.json があれば、あとはdockerで実行できる。

#### 起動
```
make rund
```

## その他備考

### 本プログラムのヘルプを表示する
```
python -m src -h
```

### venvを抜けたい時
```
deactivate
```

## lambda関数として動かす（ローカル）
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
