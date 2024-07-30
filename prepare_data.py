import os
import shutil
from tqdm import tqdm
import cv2 as cv


def merge_dir(dir_1: str, dir_2: str) -> None:
    """
    Merge the contents of two directories.

    Args:
        dir_1 (str): The path to the first directory.
        dir_2 (str): The path to the second directory.

    This function merges the contents of `dir_2` into `dir_1`. If a subdirectory
    with the same name exists in both directories, the files from `dir_2` are moved
    into the corresponding subdirectory in `dir_1`. If a subdirectory does not exist
    in `dir_1`, it is copied from `dir_2` into `dir_1`. After the merge, `dir_2` is
    deleted.

    """

    # Get the list of subdirectories in dir_1 and dir_2
    sub_folder_1 = os.listdir(dir_1)
    sub_folder_2 = os.listdir(dir_2)

    # Iterate over the subdirectories in dir_2
    for name in tqdm(sub_folder_2, desc=f"Merging {dir_2} with {dir_1}: "):
        # Check if the subdirectory exists in dir_1
        if name in sub_folder_1:
            # If it does, move the files from dir_2 into dir_1
            name_path = os.path.join(dir_2, name)
            for path in os.listdir(name_path):
                if os.path.exists(f"{dir_1}/{name}/{path}"):
                    continue
                shutil.move(
                    f'{name_path}/{path}',
                    f'{dir_1}/{name}/'
                )
        else:
            # If it doesn't exist, copy the subdirectory from dir_2 into dir_1
            shutil.copytree(
                f'{dir_2}/{name}/',
                f'{dir_1}/{name}/',
            )

    # Delete dir_2 after the merge
    shutil.rmtree(dir_2)


def format_cls(root_dir):
    sub = [f'{root_dir}/{x}' for x in os.listdir(root_dir)]
    if os.path.isdir(sub[0]):
        for x in sub:
            format_cls(x)
    else:
        new_dir = root_dir.replace(" ", "_").lower()
        if new_dir != root_dir:
            os.rename(root_dir, new_dir)


def format_file_in_cls(root_dir):
    sub = [f'{root_dir}/{x}' for x in os.listdir(root_dir)]
    if os.path.isdir(sub[0]):
        for x in sub:
            format_file_in_cls(x)
    else:
        for i, path in enumerate(sub, start=1):
            cls_name = root_dir.split("/")[-1]
            new_path = f"{root_dir}/{cls_name}_{i}.{path.split('.')[-1]}"

            os.rename(path, new_path)


def copy_file(root_dir, list_path):
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    for path in list_path:
        shutil.copy(
            path,
            root_dir
        )


def splitting_data(root_dir, train_ratio, val_ratio):
    cls_names = os.listdir(root_dir)

    for name in cls_names:
        if name in ["train", "val", "test"]:
            continue
        name_dir = f"{root_dir}/{name}"
        list_img_path = [f"{name_dir}/{x}" for x in os.listdir(name_dir)]

        size = int(len(list_img_path) * train_ratio)
        val_size = int(len(list_img_path) * val_ratio)
        train_list = list_img_path[:size]
        val_list = list_img_path[size:size + val_size]
        test_list = list_img_path[size + val_size:]

        copy_file(f"{root_dir}/train/{name}", train_list)
        copy_file(f"{root_dir}/val/{name}", val_list)
        copy_file(f"{root_dir}/test/{name}", test_list)

        shutil.rmtree(name_dir)


def covert_image(root_dir, _format="jpg"):
    sub = [f'{root_dir}/{x}' for x in os.listdir(root_dir)]
    if os.path.isdir(sub[0]):
        for x in sub:
            covert_image(x)
    else:
        for i, path in tqdm(enumerate(sub), desc=f"Convert image in {root_dir} to {_format}", total=len(sub)):
            if path.endswith(f".{_format}"):
                continue
            # if not os.path.exists(f"{path[:-4]}.{_format}"):
            img = cv.imread(path)
            cv.imwrite(f"{path[:-4]}.{_format}", img)
            # os.remove(path)


def count_file(root_dir):
    total = 0
    sub = [f'{root_dir}/{x}' for x in os.listdir(root_dir)]
    if os.path.isdir(sub[0]):
        for x in sub:
            total += count_file(x)
    else:
        return len(sub)


def process_multi_dataset(root_dir, train_ratio, val_ratio):
    data_names = os.listdir(root_dir)

    for data_name in data_names:
        data_dir = f"{root_dir}/{data_name}"
        format_cls(data_dir)
        format_file_in_cls(data_dir)

        splitting_data(data_dir, train_ratio, val_ratio)
        covert_image(data_dir)


if __name__ == "__main__":
    # process_multi_dataset("./Datasets", 0.7, 0.1)
    data_dir = "./Datasets/"

    # splitting_data(data_dir, 0.7, 0.1)

