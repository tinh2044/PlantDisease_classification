<h1 align="center">Plant Disease Classification</h1>
<img src="./Images/bg.png" alt="bg"/>

## Introduction

This project leverages the power of EfficientNet model to help farmers and gardeners quickly and accurately identify plant diseases using images of plant leaves. Upon detecting a disease, the application provides information about the disease, including its name, cause, and symptoms.

## Project Overview

1. Training Pipeline
2. Build a simple server
3. Build client

## Dataset

Data is collected from various sources on Kaggle and aggregated together. The dataset has 22 plants with corresponding diseases splitting into train, val, and test.

**Data Description**


| Name           | Disease                                                                                                                        |
|:--------------:| :----------------------------------------------------------------------------------------------------------------------------- |
|     Apple      | alternate leaf spot, brown spot, gray spot, healthy leaf,                                                                      |
|  Bell pepper   | bacterial spot, healthy                                                                                                        |
|    Cassava     | bacterial blight, brown streak, green mottle, healthy mosaic                                                                   |
|     Cherry     | healthy, powdery mildew                                                                                                        |
|     Chili      | healthy, leaf curl, leaf spot, whitefly, yellowish                                                                             |
|     Citrus     | black spot, canker, greening, healthy, melanoma                                                                                |
|    Coconut     | caterpillars, drying of leaflets, flaccidity, leaflets, yellowing                                                              |
|     Coffee     | healthy, red spider mite, rust                                                                                                 |
|      Corn      | common rust, gray leaf spot, healthy                                                                                           |
|     Grape      | black rot, blight, esca, healthy                                                                                               |
|     Guava      | canker, dot, healthy, mummification, rust                                                                                      |
|   Jack fruit   | algal spot, black spot, healthy                                                                                                |
|     Mango      | anthracnose, back die, bacterial canker, cutting weevil, gall midge, healthy, mildew powder mould sooty,                       |
|     Peach      | bacterial spot, healthy,                                                                                                       |
|     Potato     | early blight, healthy, late blight                                                                                             |
|      Rice      | blast, blight, brown spot, healthy, narrow brown spot, scald                                                                   |
|    Soybean     | bacterial blight, caterpillar, diabrotica speciosa, downy mildew, healthy, mosaic virus, powdery mildew, rust, southern blight |
|   Strawberry   | healthy, leaf scorch                                                                                                           |
|   Sugarcane    | healthy, red rot, red stripe, rust,                                                                                            |
|      Tea       | bird eye spot, brown blight, healthy, leaf spot                                                                                |
|     Tomato     | bacterial spot, curl virus, early blight, healthy, late blight, leaf mold, mosaic virus, septoria leaf spot, spot              |
|     Wheat      | brown rust, healthy, yellow rust                                                                                               |

## Set-up

- Clone this repo to your Local Machine and move into it.

```Terminal
$ git clone git@github.com:tinh2044/PlantDisease_classification.git
$ cd PlantDisease_classification
```

- Create virtual environments with [conda](https://conda.io/projects/conda/en/latest/index.html) to avoid conflicts

```Terminal
conda create --name plantDisease
conda activate plantDisease
```

- Install requirements.

```Terminal
pip install -r ./requirements.txt
```

## Training

Download dataset from kaggle [link](https://www.kaggle.com/datasets/nguyenchitinh/plantdisease-with-20-plant) and extract its to `Datasets` folder

Or download datasets using Kaggle CLI
```
kaggle datasets download -d nguyenchitinh/plantdisease-with-20-plant
```

Make sure after extracted, your `Datasets` folder has struct like this
```
|——Datasets
   |——AppleDisease
        |——train
       |——class_name_1
       |——class_name_2
       ......
       |——class_name_n
  |——valid
       |——class_name_1
       |——class_name_2
       ......
       |——class_name_n
  |—-test
       |——class_name_1
       |——class_name_2
       ......
       |——class_name_n
   |——BellPepperDisease
       ......
```
- To train the models run

```Terminal
python train_multiple_model.py --epoch 100 --batch_size 32 --root_dir ./Datasets --img_size 224 --export_dir ./SavedModels --h5_dir ./Models
```
After training is complete. Weights of model is saved to ```./Model``` and  SavedModel is saved to ```./SavedModels```
- Evaluate the model
```Terminal
python evaluate.py --root_dir ./Datasets --h5_dir ./Models
```

- Convert model to tflite 
```Terminal
python covert_tflite.py
```
## Server
Make sure you have to copy all tflite model in ``ModelLight`` to ``server/ModelLight``

Move to server directory 

```Terminal
cd server
```
- Run server by command

```Terminal
uvicorn app.main:app --host 127.0.0.1 --port 5000
```

- Or using docker 
```Terminal
docker compose up
```
## Client
Move to client directory
```Terminal
cd client
```
Run client by command
```Terminal
npm start
```
**Note**: You need to create `.env` file in client folder and type
```javascript
REACT_APP_API_URL=your_server_api
```

## References
- [New Plant Diseases Dataset](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)
- [Plant Disease Classification Merged Dataset](https://www.kaggle.com/datasets/alinedobrovsky/plant-disease-classification-merged-dataset)
- [EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks](https://arxiv.org/abs/1905.11946)
- [Transfer learning and fine-tuning](https://www.tensorflow.org/tutorials/images/transfer_learning)
