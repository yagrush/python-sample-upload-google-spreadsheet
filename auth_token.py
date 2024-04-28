"""
WSL環境などで could not locate runnable browser が発生し、
ブラウザが起動せず authorized_user.json が作れない場合、
このプログラムをMS-DOSコマンドプロンプトで実行する
"""
from google_auth_oauthlib.flow import InstalledAppFlow

# アクセス許可を要請したいスコープのリスト
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def main():
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    creds = flow.run_local_server(port=0)
   
    with open("authorized_user.json", "w") as token:
        token.write(creds.to_json())


if __name__ == "__main__":
    main()