"""TSVデータをGoogleスプレッドシートにアップロードする"""

import os
from pathlib import Path
import csv

import gspread
from dotenv import load_dotenv

from app import const, util

const.FILENAME_GOOGLE_SPREADSHEET_UPLOAD_FILE_ID = "GOOGLE_SPREADSHEET_UPLOAD_FILE_ID"
const.GOOGLE_SPREADSHEET_WORKSHEET_ID = "GOOGLE_SPREADSHEET_WORKSHEET_ID"


def main():
    load_dotenv()

    dir_path = Path(__file__).resolve().parent

    gc = gspread.oauth(
        credentials_filename=os.path.join(
            dir_path, os.environ["CLIENT_SECRET_JSON_FILE"]
        ),  # 認証用のJSONファイル
        authorized_user_filename=os.path.join(
            dir_path, os.environ["AUTHORIZED_USER_JSON_FILE"]
        ),  # 証明書の出力ファイル（初回アクセス時に１度だけ作成させられる）
    )

    # スプレッドシートを取得
    spread_sheet = util.get_google_spread_sheet(
        gc=gc,
        file_path_spreadsheet_file_id=os.path.join(
            dir_path, const.FILENAME_GOOGLE_SPREADSHEET_UPLOAD_FILE_ID
        ),
        file_name=os.environ["GOOGLE_SPREADSHEET_UPLOAD_FILE_NAME"],
        folder_id=os.environ["GOOGLE_SPREADSHEET_UPLOAD_FOLDER_ID"],
    )

    # TSVファイルを準備
    tsv_file_path = os.path.join(dir_path, os.environ["FILENAME_DATA_TSV"])
    with open(tsv_file_path, encoding="utf8", newline="\n") as f:
        csv_reader = csv.reader(f, delimiter="\t", lineterminator="\n")
        if csv_reader is None:
            raise Exception("data file invalid")

        # TSVデータを２次元配列に変換
        lines = [row for row in csv_reader]
        if len(lines) < 1:
            print("data file line_num < 1. no data")
            return

        # スプレッドシート内のシートを取得
        work_sheet = util.get_google_work_sheet(
            spread_sheet=spread_sheet,
            file_path_worksheet_id=os.path.join(
                dir_path, const.GOOGLE_SPREADSHEET_WORKSHEET_ID
            ),
            worksheet_name=os.environ["GOOGLE_SPREADSHEET_WORKSHEET_NAME"],
            rows=len(lines),
            cols=len(lines[0]),
        )

        work_sheet.clear()  # 一度シートをまっさらにする
        work_sheet.append_rows(lines)  # 改めてTSVの内容を書き込む


if __name__ == "__main__":
    main()
