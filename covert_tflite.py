import tensorflow as tf
import os
import keras
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent
model_light_dir = f"{BASE_DIR}/ModelLight"


if not os.path.exists(model_light_dir):
    os.mkdir(model_light_dir)

model_dir = f"{BASE_DIR}/SavedModel"
model_names = os.listdir(model_dir)
model_paths = [f"{model_dir}/{x}" for x in model_names]


for path, name in zip(model_paths, model_names):
    model_path = f'{model_light_dir}/{name[:-3]}.tflite'
    if os.path.exists(model_path):
        print(f"Has : {name} in {model_light_dir}, pass....!")
        continue
    converter = tf.lite.TFLiteConverter.from_saved_model(path)
    tfmodel = converter.convert()
    open(model_path, "wb").write(tfmodel)
    print(f'{model_light_dir}/{name[:-3]}.tflite')

