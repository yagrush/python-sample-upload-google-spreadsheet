"""TSVデータをGoogleスプレッドシートにアップロードする"""

from pathlib import Path
import csv

import gspread

from .util import get_google_spread_sheet, convert_str_or_float, get_google_work_sheet

dir_path = Path(__file__).resolve().parent.parent


async def upload_google_spreadsheet(
    client_secret_json_filepath,
    authorized_user_filename,
    spreadsheet_name,
    upload_folder_id,
    tsv_file_path,
    worksheet_name,
    spreadsheet_id_filepath,
    worksheet_id_filepath: str,
) -> None:
    """TSVデータをGoogleスプレッドシートにアップロードする"""
    gc = gspread.oauth(
        credentials_filename=client_secret_json_filepath,  # 認証用のJSONファイル
        authorized_user_filename=authorized_user_filename,  # 証明書の出力ファイル（初回アクセス時に１度だけ作成させられる）
    )

    # スプレッドシートを取得
    spread_sheet = await get_google_spread_sheet(
        gc=gc,
        file_path_spreadsheet_file_id=spreadsheet_id_filepath,
        file_name=spreadsheet_name,
        folder_id=upload_folder_id,
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
            file_path_worksheet_id=worksheet_id_filepath,
            worksheet_name=worksheet_name,
            rows=len(lines),
            cols=len(lines[0]),
        )

        work_sheet.clear()  # 一度シートをまっさらにする
        work_sheet.append_rows(lines)  # 改めてTSVの内容を書き込む
        work_sheet.freeze(rows=1, cols=1)
