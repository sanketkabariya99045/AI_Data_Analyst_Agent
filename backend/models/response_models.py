from typing import List

from pydantic import BaseModel, ConfigDict


class SheetInfo(BaseModel):
    """
    Information about a single sheet in a dataset.
    """

    sheet_name: str
    rows: int
    columns: int
    column_names: List[str]


class UploadedFileResponse(BaseModel):
    """
    Information about one uploaded file.
    """

    filename: str
    path: str
    sheets: List[SheetInfo]


class UploadResponse(BaseModel):
    """
    API response returned after file upload.
    """

    success: bool
    message: str
    total_files: int
    files: List[UploadedFileResponse]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Files uploaded successfully.",
                "total_files": 1,
                "files": [
                    {
                        "filename": "sales.xlsx",
                        "path": "uploads/sales.xlsx",
                        "sheets": [
                            {
                                "sheet_name": "Sales",
                                "rows": 1200,
                                "columns": 6,
                                "column_names": [
                                    "Date",
                                    "Product",
                                    "Revenue",
                                    "Profit",
                                    "Quantity",
                                    "Region"
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    )