import gradio as gr
import numpy as np
import time
import torch
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
from diffusers import StableDiffusionPipeline


models = {"Classic model": ".model", "Figure model": ".model2"}
current_model = models["Classic model"]
disable_safety = False

def generate_image(text):  
    print("Generation based on: " + current_model)
    pipe = import_model(current_model)
    image = pipe(prompt=text).images[0]
    yield image

def import_model(model_path):
    pipe = StableDiffusionPipeline.from_pretrained(model_path, torch_dtype=torch.float16)
    pipe.to("cuda")
    pipe.safety_checker = null_safety
    return pipe

def change_path(radio_value):
    global current_model
    if(radio_value == "Figure model"):
        current_model = models['Figure model']
    else:
        current_model = models["Classic model"]

def null_safety(images, **kwargs):
      return images, False
          

with gr.Blocks(css="main.css") as app:
    gr.Markdown("<h2>Generate your OWN image in LEGO style</h2>")    
    text_input = gr.Textbox(label="Prompt")
    switch_model = gr.Radio(label="Choose Model", choices=list(models.keys()), value=list(models.keys())[0]).style(item_container=True, container=True)
    model_output = gr.Image(label="Output Image", elem_id="out_img")
    text_button = gr.Button("Generate")

    switch_model.change(change_path, inputs=switch_model)
    text_button.click(generate_image, inputs=text_input, outputs=model_output)


if __name__ == "__main__":
    app.queue()
    app.launch()  
