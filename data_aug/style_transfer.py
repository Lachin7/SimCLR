import argparse

import matplotlib.pyplot as plt

from PAMA.main import eval
import numpy as np
import torch
from torch import nn
from torchvision.transforms import transforms
from PIL import Image
import random
import os
import requests
import zipfile


def choose_random_image_from_directory(directory_path):
    if not os.path.exists(directory_path):
        raise ValueError(f"The directory '{directory_path}' does not exist.")

    files = get_all_images_in_directory(directory_path)
    # print(files)

    # image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not files:
        raise ValueError(f"No image files found in the directory '{directory_path}'.")

    # Choose a random image from the list
    random_image = random.choice(files)

    return os.path.join(random_image)


def is_image(file_path):
    try:
        image = Image.open(file_path)
        return True
    except:
        return False


def get_all_images_in_directory(directory_path):
    image_paths = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_image(file_path):
                image_paths.append(file_path)
    return image_paths


def download_and_extract_dataset(url, save_path):
    os.makedirs(save_path, exist_ok=True)

    response = requests.get(url)
    zip_file_path = os.path.join(save_path, 'artwiki_dataset.zip')

    with open(zip_file_path, 'wb') as f:
        f.write(response.content)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(save_path)

    os.remove(zip_file_path)


class StyleTransfer(object):

    def __init__(self, style_dir='../datasets/style',
                 style_url='https://github.com/asahi417/wikiart-crawler/releases/download/v0.0.0/image_face.zip',
                 keep_if_exists=True):
        self.style_dir = style_dir
        self.style_url = style_url
        self.keep_if_exists = keep_if_exists

    def __call__(self, img):
        if os.path.exists(self.style_dir):
            files = os.listdir(self.style_dir)
            if not files:
                download_and_extract_dataset(url=self.style_url, save_path=self.style_dir)
            elif self.keep_if_exists:
                pass
        else:
            download_and_extract_dataset(url=self.style_url, save_path=self.style_dir)

        random_image_path = choose_random_image_from_directory(self.style_dir)
        random_style = Image.open(random_image_path).convert("RGB")
        res = eval(img, random_style)
        return res

"""
note: to see if the style transfer work correctly, you can uncomment the code below. It will generate a stylized image 
using the image in the datasets/content folder and a style image from the style path that you provide in the StyleTransfer object
arguments. I tested the code on the wiki art faces datasets but you can use other datasets: https://github.com/asahi417/wikiart-image-dataset
if you scrol down this github page, you can see other datasets links.

st = StyleTransfer()
image = Image.open('../datasets/content/desert1024.jpg').convert('RGB')
st(image)
"""
