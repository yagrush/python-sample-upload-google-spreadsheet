"""TSVデータをGoogleスプレッドシートにアップロードする"""

import asyncio
import os
from pathlib import Path
import csv

import gspread
from dotenv import load_dotenv

from app import const, util

const.FILENAME_GOOGLE_SPREADSHEET_UPLOAD_FILE_ID = "GOOGLE_SPREADSHEET_UPLOAD_FILE_ID"
const.GOOGLE_SPREADSHEET_WORKSHEET_ID = "GOOGLE_SPREADSHEET_WORKSHEET_ID"

dir_path = Path(__file__).resolve().parent.parent


async def upload_google_spreadsheet(
    credentials_filepath,
    authorized_user_filepath,
    file_path_spreadsheet_file_id,
    google_spreadsheet_upload_file_name,
    google_spreadsheet_upload_folder_id,
    tsv_file_path,
    worksheet_name,
    file_path_worksheet_id: str,
) -> None:
    gc = gspread.oauth(
        credentials_filename=credentials_filepath,  # 認証用のJSONファイル
        authorized_user_filename=authorized_user_filepath,  # 証明書の出力ファイル（初回アクセス時に１度だけ作成させられる）
    )

    # スプレッドシートを取得
    spread_sheet = await util.get_google_spread_sheet(
        gc=gc,
        file_path_spreadsheet_file_id=file_path_spreadsheet_file_id,
        file_name=google_spreadsheet_upload_file_name,
        folder_id=google_spreadsheet_upload_folder_id,
    )

    # TSVファイルを準備
    with open(tsv_file_path, encoding="utf8", newline="\n") as f:
        csv_reader = csv.reader(f, delimiter="\t", lineterminator="\n")
        if csv_reader is None:
            raise Exception("data file invalid")

        # TSVデータを２次元配列に変換
        lines = [
            [col if line_no == 0 or i == 0 else float(col) for i, col in enumerate(row)]
            for line_no, row in enumerate(csv_reader)
        ]
        if len(lines) < 1:
            print("data file line_num < 1. no data")
            return

        # スプレッドシート内のシートを取得
        work_sheet = await util.get_google_work_sheet(
            spread_sheet=spread_sheet,
            file_path_worksheet_id=file_path_worksheet_id,
            worksheet_name=worksheet_name,
            rows=len(lines),
            cols=len(lines[0]),
        )

        work_sheet.clear()  # 一度シートをまっさらにする
        work_sheet.append_rows(lines)  # 改めてTSVの内容を書き込む


async def main():
    load_dotenv(override=True)

    dir_path = Path(__file__).resolve().parent.parent

    await upload_google_spreadsheet(
        credentials_filepath=os.path.join(
            dir_path, os.environ["CLIENT_SECRET_JSON_FILE"]
        ),
        authorized_user_filepath=os.path.join(
            dir_path, os.environ["AUTHORIZED_USER_JSON_FILE"]
        ),
        file_path_spreadsheet_file_id=os.path.join(
            dir_path, const.FILENAME_GOOGLE_SPREADSHEET_UPLOAD_FILE_ID
        ),
        google_spreadsheet_upload_file_name=os.environ[
            "GOOGLE_SPREADSHEET_UPLOAD_FILE_NAME"
        ],
        google_spreadsheet_upload_folder_id=os.environ[
            "GOOGLE_SPREADSHEET_UPLOAD_FOLDER_ID"
        ],
        tsv_file_path=os.path.join(dir_path, os.environ["FILENAME_DATA_TSV"]),
        worksheet_name=os.environ["GOOGLE_SPREADSHEET_WORKSHEET_NAME"],
        file_path_worksheet_id=os.path.join(
            dir_path, const.GOOGLE_SPREADSHEET_WORKSHEET_ID
        ),
    )


if __name__ == "__main__":
    asyncio.run(main())
