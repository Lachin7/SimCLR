import argparse

import matplotlib.pyplot as plt

from PAMA.main import eval
import numpy as np
import torch
from torch import nn
from torchvision.transforms import transforms
from PIL import Image
import random, os


def choose_random_image_from_directory(directory_path):
    if not os.path.exists(directory_path):
        raise ValueError(f"The directory '{directory_path}' does not exist.")

    files = os.listdir(directory_path)

    image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        raise ValueError(f"No image files found in the directory '{directory_path}'.")

    # Choose a random image from the list
    random_image = random.choice(image_files)

    return os.path.join(directory_path, random_image)


class StyleTransfer(object):

    def __init__(self, style_dir='../datasets/style'):
        self.style_dir = style_dir
        # self.pil_to_tensor = transforms.ToTensor()
        # self.tensor_to_pil = transforms.ToPILImage()

    def __call__(self, img):
        random_image_path = choose_random_image_from_directory(self.style_dir)
        random_style = Image.open(random_image_path).convert("RGB")
        res = eval(img, random_style)
        return res


""" 
st = StyleTransfer()
image = Image.open('../datasets/content/desert1024.jpg').convert('RGB')
st(image)
"""
