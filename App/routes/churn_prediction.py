from fastapi import File, APIRouter, UploadFile
import pandas as pd 

churn_prediction = APIRouter()

@churn_prediction.post("/churn-prediction/")
async def prediction(file:UploadFile = File(...)):
      """
    This endpoint receive a file with the data of your costumer and predict churn.
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