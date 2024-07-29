import keras
from keras import layers
from keras.api.applications import EfficientNetB0


def get_model(input_shape, num_cls, name):
    """
    Function to create a model for Potato Disease classification.

    Parameters:
    - input_shape: Tuple, shape of the input data.
    - num_cls: Integer, number of classes for classification.

    Returns:
    - model: Keras Models, the model for Potato Disease classification.
    """
    backbone = EfficientNetB0(input_shape=input_shape,
                              include_top=False,
                              weights="imagenet")
    _input = layers.Input(shape=input_shape, name="Input")
    x = backbone(_input)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(512, activation='relu',
                     kernel_regularizer=keras.regularizers.l2(1e-5))(x)
    x = layers.Dropout(0.2)(x)
    x = layers.Dense(256, activation='relu',
                     kernel_regularizer=keras.regularizers.l2(1e-5))(x)
    x = layers.Dropout(0.2)(x)
    x = layers.Dense(num_cls, activation="softmax", name="classification")(x)

    return keras.Model(inputs=[_input], outputs=[x], name=name)


def get_augmentation():
    """
    Returns a Keras Sequential model that applies random rotation, random translation, random flip, and random contrast to an input image.

    This function creates a Keras Sequential model that applies a series of augmentation techniques to an input image. The augmentation techniques include random rotation, random translation, random flip, and random contrast. The rotation factor is set to 0.15, the translation factors for height and width are set to 0.1, and the contrast factor is set to 0.1.

    Returns:
        keras.Sequential: A Keras Sequential model that applies the augmentation techniques to an input image.
    """
    return keras.Sequential([
            layers.RandomRotation(factor=0.15),
            layers.RandomTranslation(height_factor=0.1, width_factor=0.1),
            layers.RandomFlip(),
            layers.RandomContrast(factor=0.1),
        ])
