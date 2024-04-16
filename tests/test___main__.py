"""__main__.pyの単体テスト"""

import asyncio
import os
from pathlib import Path
import csv
import gspread
import pytest
from dotenv import load_dotenv
from app import util
import app.__main__

FILENAME_GOOGLE_SPREADSHEET_UPLOAD_FILE_ID = (
    "TEST_FILENAME_GOOGLE_SPREADSHEET_UPLOAD_FILE_ID"
)

TEST_GOOGLE_SPREADSHEET_WORKSHEET_ID = "TEST_GOOGLE_SPREADSHEET_WORKSHEET_ID"

dir_path = Path(__file__).resolve().parent.parent
load_dotenv()

TEST_TSV_PATH = os.path.join(dir_path, "test.tsv")
TEST_TSV_DATA = """日時	売上（日本）	売上（アメリカ）	売上（中国）
2024-04-01	1	2	3
2024-04-02	1	2	3
2024-04-03	1	2	3
2024-04-04	1	2	3
2024-04-05	1	2	3
2024-04-06	1	2	3
2024-04-07	1	2	3
2024-04-08	1	2	3
2024-04-09	1	2	3
2024-04-10	1	2	3"""


@pytest.fixture()
def setup_test(tmpdir):
    """テストの前処理、パラメータわたし、後処理"""

    # テストの前処理： テストデータTSV作成
    tmpfile = tmpdir.join("test.tsv")

    with tmpfile.open(
        mode="w",
        encoding="UTF-8",
    ) as f:
        f.write(TEST_TSV_DATA)

    csv_file_path = str(tmpfile)
    path_filename_google_spreadsheet_upload_file_id = os.path.join(
        dir_path, FILENAME_GOOGLE_SPREADSHEET_UPLOAD_FILE_ID
    )

    # テスト関数に渡すパラメータを順次返す
    yield (
        os.path.join(dir_path, os.environ["CLIENT_SECRET_JSON_FILE"]),
        os.path.join(dir_path, os.environ["AUTHORIZED_USER_JSON_FILE"]),
        path_filename_google_spreadsheet_upload_file_id,
        "test",
        os.environ["GOOGLE_SPREADSHEET_UPLOAD_FOLDER_ID"],
        csv_file_path,
        "test",
        os.path.join(dir_path, TEST_GOOGLE_SPREADSHEET_WORKSHEET_ID),
    )

    # テストの後処理： 不要なファイルを消す
    tmpfile.remove()
    os.remove(path_filename_google_spreadsheet_upload_file_id)
    os.remove(os.path.join(dir_path, TEST_GOOGLE_SPREADSHEET_WORKSHEET_ID))


def test_upload_google_spreadsheet(setup_test):
    """upload_google_spreadsheet()の単体テスト"""
    try:

        (
            credentials_filepath,
            authorized_user_filepath,
            file_path_spreadsheet_file_id,
            google_spreadsheet_upload_file_name,
            google_spreadsheet_upload_folder_id,
            tsv_file_path,
            worksheet_name,
            file_path_worksheet_id,
        ) = setup_test

        asyncio.run(
            app.__main__.upload_google_spreadsheet(
                credentials_filepath,
                authorized_user_filepath,
                file_path_spreadsheet_file_id,
                google_spreadsheet_upload_file_name,
                google_spreadsheet_upload_folder_id,
                tsv_file_path,
                worksheet_name,
                file_path_worksheet_id,
            )
        )

        gc = gspread.oauth(
            credentials_filename=credentials_filepath,
            authorized_user_filename=authorized_user_filepath,
        )

        spread_sheet = asyncio.run(
            util.get_google_spread_sheet(
                gc=gc,
                file_path_spreadsheet_file_id=file_path_spreadsheet_file_id,
                file_name=google_spreadsheet_upload_file_name,
                folder_id=google_spreadsheet_upload_folder_id,
            )
        )

        try:
            with open(tsv_file_path, encoding="utf8", newline="\n") as f:
                csv_reader = csv.reader(f, delimiter="\t", lineterminator="\n")
                if csv_reader is None:
                    raise Exception("data file invalid")

                lines = [
                    [
                        col if line_no == 0 or i == 0 else str(col)
                        for i, col in enumerate(row)
                    ]
                    for line_no, row in enumerate(csv_reader)
                ]
                if len(lines) < 1:
                    print("data file line_num < 1. no data")
                    return

                work_sheet = asyncio.run(
                    util.get_google_work_sheet(
                        spread_sheet=spread_sheet,
                        file_path_worksheet_id=file_path_worksheet_id,
                        worksheet_name=worksheet_name,
                        rows=len(lines),
                        cols=len(lines[0]),
                    )
                )

                assert all(
                    [
                        str(row[header]) == lines[i + 1][j]
                        for i, row in enumerate(work_sheet.get_all_records())
                        for j, header in enumerate(lines[0])
                    ]
                )
        finally:
            gc.del_spreadsheet(spread_sheet.id)

    except Exception as e:
        print(f"!!!!!!error!!!!!! {e}")
        pytest.fail()
