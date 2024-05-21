import os
import numpy as np
import imageio
from PIL import Image
import torch
from torchvision.transforms import ToTensor, ToPILImage
from RRDBNet_arch import RRDBNet

# Función para cargar un modelo preentrenado de ESRGAN
def load_model():
    model_path = 'models/RRDB_ESRGAN_x4.pth'
    model = RRDBNet(in_nc=3, out_nc=3, nf=64, nb=23)
    model.load_state_dict(torch.load(model_path), strict=True)
    model.eval()
    return model

# Función para procesar un frame
def process_frame(model, frame):
    transform = ToTensor()
    inverse_transform = ToPILImage()
    
    frame_tensor = transform(frame).unsqueeze(0)
    with torch.no_grad():
        sr_frame_tensor = model(frame_tensor)
    
    sr_frame = inverse_transform(sr_frame_tensor.squeeze(0))
    return sr_frame

# Función para subir la resolución de un GIF
def upscale_gif(input_gif, output_gif):
    # Cargar el GIF
    gif = Image.open(input_gif)
    frames = []
    try:
        while True:
            frame = gif.copy()
            frames.append(frame)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    # Cargar el modelo de superresolución
    model = load_model()

    # Procesar cada frame
    sr_frames = [process_frame(model, frame) for frame in frames]

    # Guardar el nuevo GIF
    sr_frames[0].save(output_gif, save_all=True, append_images=sr_frames[1:], loop=0)

# Ruta del GIF de entrada y salida
input_gif = 'input.gif'
output_gif = 'output_upscaled.gif'

# Ejecutar la función de subida de resolución
upscale_gif(input_gif, output_gif)
