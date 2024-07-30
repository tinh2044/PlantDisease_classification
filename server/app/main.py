from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import os
import json
from typing import Optional

import tensorflow as tf
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent


model_dir = f"{BASE_DIR}/ModelLight"
model_names = os.listdir(model_dir)
model_paths = [f"{model_dir}/{x}" for x in model_names]
DICT_MODEL = {k[:k.index("_")]: tf.lite.Interpreter(model_path=v)
              for k, v in zip(model_names, model_paths)}

with open(f'{BASE_DIR}/info_disease.json', 'r', encoding="utf-8") as f:
    DICT_CLASS_NAMES = json.load(f)

app = FastAPI()


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
        list_diseases.sort(key=lambda x: x['key'])
    return list_diseases


@app.post("/predict")
async def predict(
        file: UploadFile = File(...),
        name: Optional[str] = Query(None, description="Disease name")):
    # name = "AppleDisease"
    model = DICT_MODEL[name]

    model.allocate_tensors()
    input_details = model.get_input_details()
    output_details = model.get_output_details()

    disease_info = DICT_CLASS_NAMES[name]
    class_names = list(disease_info.keys())

    img_arr = read_file_as_image(await file.read())
    model.set_tensor(input_details[0]['index'], [img_arr])

    model.invoke()

    pred = model.get_tensor(output_details[0]['index'])

    confidence = np.max(pred[0])

    pred_class = class_names[np.argmax(pred[0])]
    return {
        **disease_info[pred_class],
        'class': pred_class,
        'confidence': round(confidence * 100, 2)
    }


def read_file_as_image(bytes) -> np.array:
    img = Image.open(BytesIO(bytes)).resize((224, 224))

    return np.array(img).astype(np.float32)


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=5000, reload=True)
