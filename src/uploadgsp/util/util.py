import gspread
import re


def write_str_to_file(file, s: str):
    """
    fileにstrとしてsを書き込む
    """
    with open(
        file=file,
        mode="w",
        encoding="UTF-8",
    ) as f:
        f.write(s)


def read_str_from_file(file) -> str | None:
    """
    fileをstrとして読んで返す
    """
    try:
        with open(
            file=file,
            mode="r",
            encoding="UTF-8",
        ) as f:
            return f.read()
    except FileNotFoundError:
        return None


def convert_str_or_float(s: str) -> str | float:
    """sが整数or少数だったらfloatに変換して返す"""
    return float(s) if re.fullmatch(r"-?\d+(\.\d+)?", s) is not None else str(s)


async def get_google_spread_sheet(
    gc: gspread.Client,
    file_path_spreadsheet_file_id: str,
    file_name: str,
    folder_id: str,
) -> gspread.spreadsheet.Spreadsheet:
    google_spreadsheet_upload_file_id = read_str_from_file(
        file_path_spreadsheet_file_id
    )

    if google_spreadsheet_upload_file_id is not None:
        try:
            spread_sheet = gc.open_by_key(google_spreadsheet_upload_file_id)
            return spread_sheet
        except gspread.exceptions.SpreadsheetNotFound as e:
            print(e)
            print(
                f"file-id: {google_spreadsheet_upload_file_id} is invalid. create new"
            )

    spread_sheet = gc.create(file_name, folder_id)
    write_str_to_file(
        file_path_spreadsheet_file_id,
        spread_sheet.id,
    )

    return spread_sheet


async def get_google_work_sheet(
    spread_sheet: gspread.spreadsheet.Spreadsheet,
    file_path_worksheet_id: str,
    worksheet_name: str,
    rows,
    cols: int,
) -> gspread.worksheet.Worksheet:
    worksheet_id = read_str_from_file(file_path_worksheet_id)

    if worksheet_id is not None:
        try:
            work_sheet = spread_sheet.get_worksheet_by_id(worksheet_id)
            return work_sheet
        except (
            gspread.exceptions.WorksheetNotFound,
            gspread.exceptions.SpreadsheetNotFound,
        ) as e:
            print(e)
            print(f"worksheet-id: {worksheet_id} is invalid. create new")

    try:
        work_sheet = spread_sheet.add_worksheet(worksheet_name, rows, cols)
        write_str_to_file(
            file_path_worksheet_id,
            str(work_sheet.id),
        )

        return work_sheet
    except gspread.exceptions.APIError as e:
        if e.code == 400:
            work_sheet = spread_sheet.worksheet(worksheet_name)
            write_str_to_file(
                file_path_worksheet_id,
                str(work_sheet.id),
            )
            return work_sheet
        else:
            raise e
