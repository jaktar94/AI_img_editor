from PIL import Image

from src.filter_names_enum import FilterNamesEnum
import ai_filters.Style_GAN.inference_stylegan as style_gan
import numpy as np


class AIFilter:
    def apply_filter(self, image: Image, filter_name: FilterNamesEnum) -> Image:
        image = np.asarray(image)
        result = style_gan.run(image, input_size=image.shape[0], style=filter_name.value.lower())
        return Image.fromarray(np.uint8(result)).convert('RGB')
