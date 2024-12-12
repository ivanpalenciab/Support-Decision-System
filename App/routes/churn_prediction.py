from fastapi import File, APIRouter, UploadFile
import pandas as pd 
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

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
        df.replace({"Existing Customer":0,"Attrited Customer":0},inplace=True)

        #we will imput null values if exist
        cat_cols = df.dtypes[df.dtypes == 'object'].index # get categoricals
        # Change values to lower and replace space with _ for cleaning
        for i in cat_cols:
           df[i] = df[i].apply(lambda x: x.lower().replace(" ", "_"))
        #encoded before imputing   
        data_encoded = pd.get_dummies(df, drop_first = True)
        # Using KNN Imputer
        impute = KNNImputer(n_neighbors = 5)
        data_imputed = impute.fit_transform(data_encoded)
        # Converting the imputed array to dataframe
        data_imputed = pd.DataFrame(data_imputed, columns = data_encoded.columns)
        # Replacing the old columns with imputed values for analysis
        missing_cols = df.isnull().sum()[df.isnull().sum() > 0].index

        for i in missing_cols:
           df[i] = data_imputed[i]
        info = str(type(df))#df.head().to_dict(orient="records")

        X = df.drop("Churn", axis = 1)
        X = pd.get_dummies(X,dtype=int, drop_first = True)

        df.replace({"Existing Customer":0,"Attrited Customer":0},inplace=True)
        y = df["Churn"]
        

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Data Scalation
        x_scaler = MinMaxScaler()
        y_scaler = MinMaxScaler()

        X_train = pd.DataFrame(x_scaler.fit_transform(X_train), columns=X_train.columns)
        X_test = pd.DataFrame(x_scaler.transform(X_test), columns=X_test.columns)
        y_train=y_scaler.fit_transform(y_train.values.reshape(-1,1)).ravel()
        y_test = y_scaler.transform(y_test.values.reshape(-1,1))
        
        
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "data_preview": X_train.head(5).to_dict(orient="records") # return info of data
        }
      except Exception as e:
        return {"error": f"Error al procesar el archivo: {str(e)}"}