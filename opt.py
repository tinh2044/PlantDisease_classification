import argparse


def get_opt():
    """
    A function to get training parameters using argparse and return the parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Get training parameters.")

    parser.add_argument('--root_dir', type=str, required=True, help='Path to the root directory.')
    parser.add_argument('--img_size', type=int, required=True, help='Size of the input images.')
    parser.add_argument('--batch_size', type=int, required=True, help='Batch size for training.')
    parser.add_argument('--epoch', type=int, required=True, help='Number of epochs for training.')
    parser.add_argument('--export_dir', type=str, default=None, help='Path to export the model.')
    parser.add_argument('--h5_dir', type=str, default=None, help='Path to the H5 model file.')

    return parser.parse_args()

