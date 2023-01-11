from PIL import Image
import torch
from torchvision import transforms
from torchvision.transforms.functional import InterpolationMode
import shutil
import os
from models.blip import blip_decoder
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", required=True, help = "path to directory with images")
args = parser.parse_args()

device = torch.device('cpu')

def load_demo_image(image_size,device, path):
    raw_image = Image.open(rf"{path}").convert('RGB')

    transform = transforms.Compose([
        transforms.Resize((image_size,image_size),interpolation=InterpolationMode.BICUBIC),
        transforms.ToTensor(),
        transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
        ]) 
    image = transform(raw_image).unsqueeze(0).to(device)   
    return image

def generate_captioning(path, device):
    names = os.listdir(path)
    image_size = 384
    model_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_large_caption.pth'

    model = blip_decoder(pretrained=model_url, image_size=image_size, vit='large')
    model.eval()
    model = model.to(device)
    
    for name in names:
        try:
            image = load_demo_image(image_size=image_size, device=device, path=f"{path}/{name}")
            
            with torch.no_grad():
                caption = model.generate(image, sample=True, top_p=0.9, max_length=20, min_length=5) 
                with open(f"{path}/metadata.jsonl", "a+") as f:
                    line = f'"file_name": "{name}", "text": "{caption[0]}"'
                    f.write("{"+line+"}\n")
        except:
            print("Error", name)

generate_captioning(args.path, device)
