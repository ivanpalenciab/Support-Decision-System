from fastapi import File, APIRouter, UploadFile
import pandas as pd 


file = APIRouter()

@file.post("/upload/")
async def upload_file(file:UploadFile = File(...)):
    """
    This endpoint receive a file, it should be in csv or excel format otrherwise 
    you will receive a mistake message.
    """
    if file.content_type not in ["text/csv", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
        return {"error": "The file should be CSV or Excel."}
    
    try:
        # read the file by type
        if file.content_type == "text/csv":
            df = pd.read_csv(file.file)
        elif file.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(file.file)
    # procesing with dataframe
        data_preview = df.head().to_dict(orient="records")
        
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "data_preview": data_preview  # Retornamos los primeros registros como ejemplo
        }
    except Exception as e:
        return {"error": f"Error al procesar el archivo: {str(e)}"}

