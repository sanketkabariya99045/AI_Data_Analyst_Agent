from typing import Any, Dict, List

from fastapi import HTTPException, UploadFile

from backend.database.loader import loader

from backend.utils.file_utils import (
    load_dataframe,
    save_upload_file,
    validate_file_extension,
)
from backend.profiling.dataset_profiler import (
    dataset_profiler,
)
from backend.suggestions.suggestion_engine import (
    suggestion_engine,
)

class UploadService:
    """
    Business logic for file uploads.
    """

    async def process_files(
        self,
        files: List[UploadFile]
    ) -> List[Dict[str, Any]]:

        uploaded_data = []

        for file in files:

            # Validate file type
            if not validate_file_extension(file.filename):
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file: {file.filename}"
                )

            # Save file
            saved_path = await save_upload_file(file)

            # Load DataFrame(s)
            dataframes = load_dataframe(saved_path)
            
            # ---------------------------------------
            # Register DataFrames in DuckDB
            # ---------------------------------------

            created_tables = loader.load_multiple_dataframes(
                dataframes
            )

            file_result = {
                "filename": file.filename,
                "path": str(saved_path),
                "tables": created_tables,
                "sheets": []
            }

            for sheet_name, df in dataframes.items():
                
                profile = dataset_profiler.profile(df)
                suggestions = suggestion_engine.generate(
                    profile.business_columns
                )   
                file_result["sheets"].append({

                    "sheet_name": sheet_name,

                    "rows": int(df.shape[0]),

                    "columns": int(df.shape[1]),

                    "column_names": df.columns.tolist(),

                    "profile": profile.model_dump(),

                    "suggestions": [
                        suggestion.model_dump()
                        for suggestion in suggestions.suggestions
                    ],
                })  

            uploaded_data.append(file_result)

        return uploaded_data    