from pathlib import Path
from typing import Dict

import pandas as pd
from fastapi import UploadFile

# Upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Supported extensions
ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}


def get_file_extension(filename: str) -> str:
    """
    Return the file extension.
    """
    return Path(filename).suffix.lower()


def validate_file_extension(filename: str) -> bool:
    """
    Validate supported file types.
    """
    return get_file_extension(filename) in ALLOWED_EXTENSIONS


async def save_upload_file(file: UploadFile) -> Path:
    """
    Save uploaded file to uploads folder.
    """
    destination = UPLOAD_DIR / file.filename

    with destination.open("wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return destination


def load_dataframe(file_path: Path) -> Dict[str, pd.DataFrame]:
    """
    Read CSV or Excel and return dictionary of DataFrames.

    CSV:
        {"Sheet1": dataframe}

    Excel:
        {"Sales": dataframe,
         "Orders": dataframe}
    """

    extension = file_path.suffix.lower()

    if extension == ".csv":
        try:
            df = pd.read_csv(file_path, encoding="utf-8")
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(file_path, encoding="latin1")
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, encoding="cp1252")
        return {"Sheet1": df}

    if extension in [".xlsx", ".xls"]:
        sheets = pd.read_excel(
            file_path,
            sheet_name=None
        )
        return sheets

    raise ValueError("Unsupported file type")