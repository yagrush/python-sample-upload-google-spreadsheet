"""TSVデータをGoogleスプレッドシートにアップロードする"""

from pathlib import Path
import csv

import gspread

from .util import get_google_spread_sheet, convert_str_or_float, get_google_work_sheet

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
    """TSVデータをGoogleスプレッドシートにアップロードする"""
    gc = gspread.oauth(
        credentials_filename=credentials_filepath,  # 認証用のJSONファイル
        authorized_user_filename=authorized_user_filepath,  # 証明書の出力ファイル（初回アクセス時に１度だけ作成させられる）
    )

    # スプレッドシートを取得
    spread_sheet = await get_google_spread_sheet(
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
        lines = [[convert_str_or_float(col) for col in row] for row in csv_reader]
        if len(lines) < 1:
            print("data file line_num < 1. no data")
            return

        # スプレッドシート内のシートを取得
        work_sheet = await get_google_work_sheet(
            spread_sheet=spread_sheet,
            file_path_worksheet_id=file_path_worksheet_id,
            worksheet_name=worksheet_name,
            rows=len(lines),
            cols=len(lines[0]),
        )

        work_sheet.clear()  # 一度シートをまっさらにする
        work_sheet.append_rows(lines)  # 改めてTSVの内容を書き込む
