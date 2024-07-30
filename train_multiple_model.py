import keras
import os
from model import get_model, get_augmentation
from opt import get_opt
from keras.api.preprocessing import image_dataset_from_directory


def get_dataset(root_dir, img_size, batch_size):
    """
    Retrieves datasets for training, validation, and testing from the specified root directory.

    Parameters:
    - root_dir: The root directory containing the datasets.
    - size: The size of the input images.
    - batch_size: The batch size for the datasets.

    Returns:
    A tuple containing the training dataset, validation dataset, and class names.
    """
    train_dataset = image_dataset_from_directory(directory=f"{root_dir}/train",
                                                 shuffle=True,
                                                 image_size=img_size,
                                                 batch_size=batch_size,
                                                 label_mode="categorical")
    val_dataset = image_dataset_from_directory(directory=f"{root_dir}/val",
                                               shuffle=True,
                                               image_size=img_size,
                                               batch_size=batch_size, label_mode="categorical")
    class_names = train_dataset.class_names
    augmentation = get_augmentation()

    train_dataset = train_dataset.map(lambda x, y: (augmentation(x, training=True), y))
    val_dataset = val_dataset.map(lambda x, y: (augmentation(x, training=True), y))
    train_ds = train_dataset.cache().shuffle(len(train_dataset))
    val_dataset = val_dataset.cache().shuffle(len(train_ds))

    return train_dataset, val_dataset,class_names


def train_single(model, train_ds, val_ds, epoch, export_dir=None, h5_dir=None):
    """
    Trains a single model using the provided dataset and parameters.

    Parameters:
    - model: The model to train.
    - train_ds: The training dataset.
    - val_ds: The validation dataset.
    - epoch: The number of epochs to train.
    - export_dir: The directory to export the trained model.
    - h5_dir: The directory to save the model in h5 format.

    Returns:
    None
    """
    model.fit(train_ds, epochs=epoch, validation_data=val_ds)
    if export_dir:
        if not os.path.exists(export_dir):
            os.makedirs(export_dir, exist_ok=True)
        print(f"Export model to {export_dir}")
        model.export(f"{export_dir}/{model.name}")
    if h5_dir:
        if not os.path.exists(h5_dir):
            os.makedirs(h5_dir, exist_ok=True)
        print(f"Save model to {h5_dir}")
        model.save(f"{h5_dir}/{model.name}.h5")


def train_disease_classification(root_dir, img_size, batch_size, epoch, export_dir=None, h5_dir=None):
    """
    Trains a disease classification model based on datasets in the specified root directory.

    Parameters:
    - root_dir: The root directory containing the datasets.
    - size: The size of the input images.
    - batch_size: The batch size for training.
    - epoch: The number of epochs to train the model.
    - export_dir: Path to export the trained model.
    - h5_dir: Path to save the model in h5 format.

    Returns:
    None
    """
    list_dataset_name = os.listdir(root_dir)
    print(f"Found {len(list_dataset_name)} dataset in {root_dir}")
    print("Start training...")

    for name in list_dataset_name:
        model_name = f"{name}_classification"
        data_root = f"{root_dir}/{name}"
        print(f"Get train, val, test ds in {data_root}")
        train_ds, val_ds, class_names = get_dataset(f"{root_dir}/{name}", (img_size, img_size), batch_size)
        
        print(f"Get model for {name} dataset")
        model = get_model((img_size, img_size, 3), len(class_names), model_name)

        model.compile(
            loss=keras.losses.CategoricalCrossentropy(),
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            metrics=["accuracy"], )

        print(f"Training model with {epoch} epochs")
        train_single(model, train_ds, val_ds, epoch, export_dir, h5_dir)


def trainer():
    opt = get_opt()
    train_disease_classification(**vars(opt))


if __name__ == "__main__":
    trainer()
