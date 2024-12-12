from fastapi import FastAPI

from routes.file import file
from routes.churn_prediction import churn_prediction 

app = FastAPI()

app.include_router(file)
app.include_router(churn_prediction)

@app.get("/")
def root():
    return "<h1>Hello welcome to my support decision sistem </h1>"
