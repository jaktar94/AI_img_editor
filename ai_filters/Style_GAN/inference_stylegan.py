import numpy as np
import torch
from torch.autograd import Variable
import cv2

from .model import Net
from .utils import *


def run(input_image, input_size=512, style="candy", style_size=512):
    content_image = tensor_process_rgbimage(input_image).unsqueeze(0)
    style_image = cv2.imread(f'ai_filters/Style_GAN/images/{style}.jpg', cv2.IMREAD_UNCHANGED)
    style_image = cv2.cvtColor(style_image, cv2.COLOR_BGR2RGB)
    style_image = tensor_process_rgbimage(style_image).unsqueeze(0)
    style_image = preprocess_batch(style_image)
    
    style_model = Net(ngf=128)
    model_dict = torch.load('ai_filters/Style_GAN/weights/21styles.model')
    model_dict_clone = model_dict.copy()
    for key, value in model_dict_clone.items():
        if key.endswith(('running_mean', 'running_var')):
            del model_dict[key]
    style_model.load_state_dict(model_dict, False)
    
    style_v = Variable(style_image)
    content_image = Variable(preprocess_batch(content_image))
    style_model.setTarget(style_v)
    output = style_model(content_image)
    output = tensor_postprocess_bgrimage(output.data[0])
    
    return output
