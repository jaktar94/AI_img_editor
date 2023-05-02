from PIL import Image
import numpy as np


def greyscale_filter(image: Image) -> Image:
    return image.convert('L').convert('RGB')


def brown_filter(image: Image) -> Image:
    color = [104, 54, 33]
    channel_count = len(image.getbands())
    image_height, image_width = image.size
    output = np.array(image.getdata()).reshape(image_width, image_height, channel_count)
    for y in range(image_height):
        for x in range(image_width):
            for c in range(channel_count):
                output[x, y, c] = (color[c] + output[x, y, c]) / 2
    return Image.fromarray(output.astype(np.uint8))


def invert_filter(image: Image) -> Image:
    channel_count = len(image.getbands())
    image_height, image_width = image.size
    output = np.array(image.getdata()).reshape(image_width, image_height, channel_count)
    for y in range(image_height):
        for x in range(image_width):
            for c in range(channel_count):
                output[x, y, c] = 255 - output[x, y, c]
    return Image.fromarray(output.astype(np.uint8))


def hand_drawn_filter(image: Image) -> Image:
    a = np.asarray(image.convert('L')).astype('float')
    depth = 10.
    grad = np.gradient(a)
    grad_x, grad_y = grad
    grad_x = grad_x * depth / 100.0
    grad_y = grad_y * depth / 100.0
    A = np.sqrt(grad_x ** 2 + grad_y ** 2 + 1.)
    uni_x = grad_x / A
    uni_y = grad_y / A
    uni_z = 1. / A
    vec_el = np.pi / 2.2
    vec_az = np.pi / 4.0
    dx = np.cos(vec_el) * np.cos(vec_az)
    dy = np.cos(vec_el) * np.sin(vec_az)
    dz = np.sin(vec_el)
    output = 255 * (dx * uni_x + dy * uni_y + dz * uni_z)
    output = output.clip(0, 255)
    return Image.fromarray(output.astype('uint8')).convert('RGB')


def emboss_filter(image: Image) -> Image:
    kernel = np.array([[-1, -1, 0], [-1, 0, 1], [0, 1, 1]])
    factor = 1.0
    bias = 128.0

    channel_count = len(image.getbands())
    image_width, image_height = image.size
    input = np.array(image.getdata()).reshape(image_height, image_width, channel_count)
    output = np.zeros((image_height, image_width, channel_count))
    kernel_height = kernel.shape[0]
    kernel_width = kernel.shape[1]

    for y in range(image_height):
        for x in range(image_width):
            color = [0, 0, 0]
            for kernel_y in range(kernel_height):
                for kernel_x in range(kernel_width):
                    image_x = (x - kernel_width // 2 + kernel_x + image_width) % image_width
                    image_y = (y - kernel_height // 2 + kernel_y + image_height) % image_height
                    for c in range(channel_count):
                        color[c] += input[image_y, image_x, c] * kernel[kernel_y, kernel_x]
            for c in range(channel_count):
                output[y, x, c] = min(max(int(factor * color[c] + bias), 0), 255)

    output = Image.fromarray(output.astype('uint8'))
    return output.convert('L').convert('RGB')
