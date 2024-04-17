import asyncio
import os
from pathlib import Path
import argparse
import sys
from dotenv import load_dotenv

from .uploadgsp import upload_google_spreadsheet

FILENAME_GOOGLE_SPREADSHEET_UPLOAD_FILE_ID = "GOOGLE_SPREADSHEET_UPLOAD_FILE_ID"
GOOGLE_SPREADSHEET_WORKSHEET_ID = "GOOGLE_SPREADSHEET_WORKSHEET_ID"

dir_path = Path(__file__).resolve().parent.parent


def main(args):
    load_dotenv(override=True)

    parser = argparse.ArgumentParser(
        prog="uploadgsp",
        usage="python -m src []",
        description="sample upload TSV as Google spreadsheet.",
        epilog="end",
        add_help=True,
    )

    parser.add_argument(
        "-c",
        "--client_secret_json_filepath",
        type=str,
        default=os.path.join(dir_path, os.environ["CLIENT_SECRET_JSON_FILE"]),
        help="filepath of: client_secret_***************.json",
        required=False,
    )
    parser.add_argument(
        "-a",
        "--authorized_user_filepath",
        type=str,
        default=os.environ["AUTHORIZED_USER_JSON_FILE"],
        help="File path for authenticated user's certificate generated after initial authentication",
        required=False,
    )
    parser.add_argument(
        "-s",
        "--spreadsheet_name",
        type=str,
        default=os.environ["GOOGLE_SPREADSHEET_UPLOAD_FILE_NAME"],
        help="Google spreadsheet name for upload",
        required=False,
    )
    parser.add_argument(
        "-t",
        "--tsv_file_path",
        type=str,
        default=os.path.join(dir_path, os.environ["FILENAME_DATA_TSV"]),
        help="TSV filepath for upload as Google spreadsheet",
        required=False,
    )
    parser.add_argument(
        "-f",
        "--upload_folder_id",
        type=str,
        default=os.environ["GOOGLE_SPREADSHEET_UPLOAD_FOLDER_ID"],
        help="upload destination folder-ID of GoogleDrive",
        required=False,
    )
    parser.add_argument(
        "-w",
        "--worksheet_name",
        type=str,
        default=os.environ["GOOGLE_SPREADSHEET_WORKSHEET_NAME"],
        help="Name of worksheet for writing TSV data",
        required=False,
    )
    parser.add_argument(
        "-i",
        "--spreadsheet_id_filepath",
        type=str,
        default=os.path.join(dir_path, FILENAME_GOOGLE_SPREADSHEET_UPLOAD_FILE_ID),
        help="Path to the file that stores spreadsheet ID",
        required=False,
    )
    parser.add_argument(
        "-j",
        "--worksheet_id_filepath",
        type=str,
        default=os.path.join(dir_path, GOOGLE_SPREADSHEET_WORKSHEET_ID),
        help="Path to the file that stores worksheet ID",
        required=False,
    )

    args_parsed = parser.parse_args(args)

    asyncio.run(
        upload_google_spreadsheet(
            client_secret_json_filepath=args_parsed.client_secret_json_filepath,
            authorized_user_filepath=args_parsed.authorized_user_filepath,
            spreadsheet_name=args_parsed.spreadsheet_name,
            upload_folder_id=args_parsed.upload_folder_id,
            tsv_file_path=args_parsed.tsv_file_path,
            worksheet_name=args_parsed.worksheet_name,
            spreadsheet_id_filepath=args_parsed.spreadsheet_id_filepath,
            worksheet_id_filepath=args_parsed.worksheet_id_filepath,
        )
    )


if __name__ == "__main__":
    main(sys.argv[1:])
