from keras.api.preprocessing import image_dataset_from_directory


def get_dataset(root_dir, size, batch_size):
    """
    Retrieves datasets for training, validation, and testing from the specified root directory.

    Parameters:
    - root_dir: The root directory containing the datasets.
    - size: The size of the input images.
    - batch_size: The batch size for the datasets.

    Returns:
    A tuple containing the training dataset, validation dataset, and testing dataset.
    """
    train_dataset = image_dataset_from_directory(directory=f"{root_dir}/train",
                                                 shuffle=True,
                                                 image_size=size,
                                                 batch_size=batch_size,
                                                 label_mode="categorical")
    val_dataset = image_dataset_from_directory(directory=f"{root_dir}/val",
                                               shuffle=True,
                                               image_size=size,
                                               batch_size=batch_size, label_mode="categorical")
    test_dataset = image_dataset_from_directory(directory=f"{root_dir}/test",
                                                shuffle=True,
                                                image_size=size,
                                                batch_size=batch_size, label_mode="categorical")

    return train_dataset, val_dataset, test_dataset
