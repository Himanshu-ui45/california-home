from fastapi import FastAPI
import numpy as np
import joblib
import uvicorn

app = FastAPI()


obj= joblib.load("california.joblib")
model = obj["model"]
cols = obj["columns"]



@app.get("/")
def greek1():
    return ('welcome')



@app.post("/predict")
def predict(MedInc: float, HouseAge: float,
            AveRooms: float, AveBedrms: float,
            Population: float, AveOccup: float,
            Latitude: float, Longitude: float):
    Input = [[MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude]]

    output = model.predict(Input)
    return {f"california housing value is : {output}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)