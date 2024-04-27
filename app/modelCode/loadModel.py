import os
import torch
from dotenv import load_dotenv
from modelCode.alphabet_models import Diffusion
load_dotenv()

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models')

diffusion_alpha = Diffusion(noise_steps=1000, beta_start=1e-4, beta_end=0.02, img_size=32, num_classes=39, c_in=1, c_out=1)
ckpt_alpha = torch.load(os.path.join(MODEL_DIR, "diffusion_alpha_ema_ckpt_45.pt", map_location=torch.device('cpu')))

new_state_dict = {}
for key, value in ckpt_alpha.items():
    if key.startswith("module."):
        new_key = key[7:]
    else:
        new_key = key
    new_state_dict[new_key] = value
diffusion_alpha.load(new_state_dict)

diffusion_animals = Diffusion(noise_steps=1000, beta_start=1e-4, beta_end = 0.02, img_size=128, num_classes=10, c_in=3, c_out=3)
ckpt_animals = torch.load(os.path.join(MODEL_DIR, 'ema_ckpt_animals.pth', map_location=torch.device('cpu')))

new_state_dict = {}
for key, value in ckpt_animals.items():
    if key.startswith("module."):
        new_key = key[7:]
    else:
        new_key = key
    new_state_dict[new_key] = value
diffusion_animals.load(new_state_dict)