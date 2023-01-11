import gradio as gr
import numpy as np
import time
import torch
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
from diffusers import StableDiffusionPipeline


def fake_diffusion(text):  
    pipe = import_model()
    image = pipe(prompt=text).images[0]
    yield image

def import_model():
    model_path = ".model"
    pipe = StableDiffusionPipeline.from_pretrained(model_path, torch_dtype=torch.float16)
    pipe.to("cuda")
    return pipe


with gr.Blocks(css="main.css") as app:
    gr.Markdown("<h2>Generate your OWN image in LEGO style</h2>")

    text_input = gr.Textbox(label="Prompt")
    model_output = gr.Image(elem_id="out_img").style(height=512, width=512)
    text_button = gr.Button("Generate")

    text_button.click(fake_diffusion, inputs=text_input, outputs=model_output)
    

if __name__ == "__main__":
    app.queue()
    app.launch()  
