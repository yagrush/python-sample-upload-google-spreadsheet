import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

from .uploadgsp import upload_google_spreadsheet

FILENAME_GOOGLE_SPREADSHEET_UPLOAD_FILE_ID = "GOOGLE_SPREADSHEET_UPLOAD_FILE_ID"
GOOGLE_SPREADSHEET_WORKSHEET_ID = "GOOGLE_SPREADSHEET_WORKSHEET_ID"

dir_path = Path(__file__).resolve().parent.parent


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
            dir_path, FILENAME_GOOGLE_SPREADSHEET_UPLOAD_FILE_ID
        ),
        google_spreadsheet_upload_file_name=os.environ[
            "GOOGLE_SPREADSHEET_UPLOAD_FILE_NAME"
        ],
        google_spreadsheet_upload_folder_id=os.environ[
            "GOOGLE_SPREADSHEET_UPLOAD_FOLDER_ID"
        ],
        tsv_file_path=os.path.join(dir_path, os.environ["FILENAME_DATA_TSV"]),
        worksheet_name=os.environ["GOOGLE_SPREADSHEET_WORKSHEET_NAME"],
        file_path_worksheet_id=os.path.join(dir_path, GOOGLE_SPREADSHEET_WORKSHEET_ID),
    )


if __name__ == "__main__":
    asyncio.run(main())
