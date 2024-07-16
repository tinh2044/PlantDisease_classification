from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
import fastapi
from io import BytesIO
from PIL import Image
import os
import json
from typing import Optional

import tensorflow as tf
import keras
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent

@tf.keras.utils.register_keras_serializable()
def swish(x):
    return x * tf.nn.sigmoid(x)


model_dir = f"{BASE_DIR}/Model"
model_names = os.listdir(model_dir)
model_paths = [f"{model_dir}/{x}" for x in model_names]
DICT_MODEL = {k[:k.index("_")]: keras.models.load_model(v, custom_objects={'swish': swish})
              for k, v in zip(model_names, model_paths)}

with open(f'{BASE_DIR}/class_names.json', 'r', encoding="utf-8") as f:
    DICT_CLASS_NAMES = json.load(f)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5500/test.html",
    "https://classy-monstera-8cde1a.netlify.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/diseases")
async def get_diseases():
    with open(f"{BASE_DIR}/diseases.json", 'r', encoding="utf-8") as f:
        list_diseases = json.load(f)
    return list_diseases


@app.post("/predict")
async def predict(
        file: UploadFile = File(...),
        name: Optional[str] = Query(None, description="Disease name")):
    # name = "AppleDisease"
    model = DICT_MODEL[name]
    disease_info = DICT_CLASS_NAMES[name]
    class_names = list(disease_info.keys())

    img_arr = read_file_as_image(await file.read())
    pred = model.predict(tf.expand_dims(img_arr, 0))

    confidence = np.max(pred[0])

    pred_class = class_names[np.argmax(pred[0])]
    return {
        **disease_info[pred_class],
        'class': pred_class,
        'confidence': round(confidence * 100, 2)
    }


def read_file_as_image(bytes) -> np.array:
    img = Image.open(BytesIO(bytes)).resize((224, 224))

    return np.array(img)


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=5000, reload=True)
