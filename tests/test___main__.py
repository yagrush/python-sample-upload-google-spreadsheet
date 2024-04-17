"""__main__.pyの単体テスト"""

import asyncio
import os
from pathlib import Path
import csv
import gspread
import pytest
from dotenv import load_dotenv
from src.uploadgsp import upload_google_spreadsheet
from src.uploadgsp.util import get_google_spread_sheet, get_google_work_sheet

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
2024-04-03	1	2124.2144	3
2024-04-04	1	2	314214
2024-04-05	-111	2	3
2024-04-06	1	2	3
2024-04-07	1	2	-1414.124412
2024-04-08	1	2	3
2024-04-09	1	2	3
2024-04-10	1	2.12441	3"""


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

    client_secret_json_filepath = os.path.join(
        dir_path, os.environ["CLIENT_SECRET_JSON_FILE"]
    )
    authorized_user_filename = os.path.join(
        dir_path, os.environ["AUTHORIZED_USER_JSON_FILE"]
    )
    spreadsheet_name = "testspread"
    upload_folder_id = os.environ["GOOGLE_SPREADSHEET_UPLOAD_FOLDER_ID"]
    tsv_file_path = str(tmpfile)
    worksheet_name = "testwork"
    spreadsheet_id_filepath = os.path.join(
        dir_path, FILENAME_GOOGLE_SPREADSHEET_UPLOAD_FILE_ID
    )
    worksheet_id_filepath = os.path.join(dir_path, TEST_GOOGLE_SPREADSHEET_WORKSHEET_ID)

    # テスト関数に渡すパラメータを順次返す
    yield (
        client_secret_json_filepath,
        authorized_user_filename,
        spreadsheet_name,
        upload_folder_id,
        tsv_file_path,
        worksheet_name,
        spreadsheet_id_filepath,
        worksheet_id_filepath,
    )

    # テストの後処理： 不要なファイルを消す
    tmpfile.remove()
    os.remove(spreadsheet_id_filepath)
    os.remove(worksheet_id_filepath)


def test_upload_google_spreadsheet(setup_test):
    """
    upload_google_spreadsheet()の単体テスト
    実行するには .env を作成し設定してください
    """
    try:
        (
            client_secret_json_filepath,
            authorized_user_filename,
            spreadsheet_name,
            upload_folder_id,
            tsv_file_path,
            worksheet_name,
            spreadsheet_id_filepath,
            worksheet_id_filepath,
        ) = setup_test

        asyncio.run(
            upload_google_spreadsheet(
                client_secret_json_filepath=client_secret_json_filepath,
                authorized_user_filename=authorized_user_filename,
                spreadsheet_name=spreadsheet_name,
                upload_folder_id=upload_folder_id,
                tsv_file_path=tsv_file_path,
                worksheet_name=worksheet_name,
                spreadsheet_id_filepath=spreadsheet_id_filepath,
                worksheet_id_filepath=worksheet_id_filepath,
            )
        )

        gc = gspread.oauth(
            credentials_filename=client_secret_json_filepath,
            authorized_user_filename=authorized_user_filename,
        )

        spread_sheet = asyncio.run(
            get_google_spread_sheet(
                gc=gc,
                file_path_spreadsheet_file_id=spreadsheet_id_filepath,
                file_name=spreadsheet_name,
                folder_id=upload_folder_id,
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
                    get_google_work_sheet(
                        spread_sheet=spread_sheet,
                        file_path_worksheet_id=worksheet_id_filepath,
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
