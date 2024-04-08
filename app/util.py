import gspread


def write_str_to_file(file, s: str):
    with open(
        file=file,
        mode="w",
        encoding="UTF-8",
    ) as f:
        f.write(s)


def read_str_from_file(file) -> str | None:
    try:
        with open(
            file=file,
            mode="r",
            encoding="UTF-8",
        ) as f:
            return f.read()
    except FileNotFoundError:
        return None


def get_google_spread_sheet(
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


def get_google_work_sheet(
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
        except gspread.exceptions.SpreadsheetNotFound as e:
            print(e)
            print(f"worksheet-id: {worksheet_id} is invalid. create new")

    work_sheet = spread_sheet.add_worksheet(worksheet_name, rows, cols)
    write_str_to_file(
        file_path_worksheet_id,
        str(work_sheet.id),
    )

    return work_sheet