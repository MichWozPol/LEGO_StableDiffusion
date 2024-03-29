import gradio as gr
import torch
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "2,3" #choose GPU index
from diffusers import StableDiffusionPipeline


model_names = ["Classic model 1", "Classic model 2", "Figure model"]
available_devices = ['cuda', 'cpu']
models = {model_names[0]: "./app/.model_1_30", model_names[1]: "./app/.model_1_60", model_names[2]: "./app/.model_2_30"}
current_device = available_devices[0]
current_model = models[model_names[0]]
disable_safety = False

def generate_image(text):  
    print("Generation based on: " + current_model)
    pipe = import_model(current_model)
    image = pipe(prompt=text).images[0]
    yield image

def import_model(model_path):
    pipe = StableDiffusionPipeline.from_pretrained(model_path, safety_checker=None)
    pipe.to(current_device)
    pipe.safety_checker = null_safety
    return pipe

def change_device(radio_value):
    global current_device
    current_device = radio_value

def change_path(radio_value):
    global current_model
    current_model = models[radio_value]

def null_safety(images, **kwargs):
      return images, False
          

with gr.Blocks(css="./app/main.css") as app:
    gr.Markdown("<h2>Generate your OWN image in LEGO style</h2>")    
    text_input = gr.Textbox(label="Prompt")
    switch_model = gr.Radio(label="Choose Model", choices=model_names, value=model_names[0]).style(item_container=True, container=True)
    # uncomment if you want to choose between cpu and gpu, otherwise gpu will be chosen
    # switch_device = gr.Radio(label="Choose Device", choices=available_devices, value=available_devices[0]).style(item_container=True, container=True) 
    model_output = gr.Image(label="Output Image", elem_id="out_img")
    text_button = gr.Button("Generate")

    switch_model.change(change_path, inputs=switch_model)
    # switch_device.change(change_device, inputs=switch_device) # uncomment if you want to choose between cpu and gpu, otherwise gpu will be chosen
    text_button.click(generate_image, inputs=text_input, outputs=model_output)


if __name__ == "__main__":
    app.queue()
    app.launch(share=True)  
