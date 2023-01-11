import gradio as gr
import numpy as np
import time


def fake_diffusion(input_val):  
    print(input_val)
    for _ in range(1,100):
        time.sleep(1)
        image = np.random.random((600, 600, 3))
        yield image
    image = "https://i.picsum.photos/id/867/600/600.jpg?hmac=qE7QFJwLmlE_WKI7zMH6SgH5iY5fx8ec6ZJQBwKRT44" 
    yield image


with gr.Blocks() as app:
    gr.Markdown("<h2>Generate your OWN image in LEGO style</h2>")

    text_input = gr.Textbox()
    model_output = gr.Image()
    text_button = gr.Button("Generate")

    text_button.click(fake_diffusion, inputs=text_input, outputs=model_output)
    

if __name__ == "__main__":
    app.queue()
    app.launch()  
