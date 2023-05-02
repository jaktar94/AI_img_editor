import numpy as np
import torch
import cv2
from PIL import Image


def tensor_process_rgbimage(img):
    img = img.transpose(2, 0, 1)
    img = torch.from_numpy(img).float()
    return img


def tensor_postprocess_rgbimage(tensor, cuda=False):
    if cuda:
        img = tensor.clone().cpu().clamp(0, 255).numpy()
    else:
        img = tensor.clone().clamp(0, 255).numpy()
    img = img.transpose(1, 2, 0).astype('uint8')
    return img


def tensor_postprocess_bgrimage(tensor, cuda=False):
    (b, g, r) = torch.chunk(tensor, 3)
    tensor = torch.cat((r, g, b))
    return tensor_postprocess_rgbimage(tensor, cuda)


def preprocess_batch(batch):
    batch = batch.transpose(0, 1)
    (r, g, b) = torch.chunk(batch, 3)
    batch = torch.cat((b, g, r))
    batch = batch.transpose(0, 1)
    return batch
