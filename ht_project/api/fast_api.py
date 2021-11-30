from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

import joblib
from datetime import datetime

import pytz

from fastapi import FastAPI

app = FastAPI()

df = pd.read_csv(
    "/Users/fenice/code/QZKZ3/ht_project/raw_data/final_df_26_11.csv")


@app.get("/")
def read_root():
    return {"Hello": "World"}



@app.get("/insights")
def predict(departure):
    X=df["arrival_1"][df["departure"]==departure]

    return {"arrival_1": X}
