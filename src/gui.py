import gradio as gr
from speech_tool import SpeechTool
import os
from pathlib import Path


css = """
h1 {
    text-align: center;
    display:block;
}

.container {
        height: 10vh;
}
"""
theme = gr.themes.Default(primary_hue=gr.themes.colors.sky)
demo = gr.Blocks(css=css, theme=theme)
st = SpeechTool()
output_path = Path('data/output')


def greet(modes, file_input, output_path, speed, volume):

    output = [None, None]
    if checkbox_bttns[0] in modes:
        result = st.modify_audio(file_input, output_path, speed, volume)
        output[0] = result 

    if checkbox_bttns[1] in modes:
        result = st.transcribe_audio(file_input, output_path)
        output[1] = result 

    return output


def filter(choice):
    
    flag_output = False
    if checkbox_bttns[0] in choice:
        if checkbox_bttns[1] in choice:
            flag_output = True

        return [gr.update(visible=True), gr.update(visible=True), gr.update(visible=True),\
                gr.update(visible=True), gr.update(visible=True), gr.update(visible=flag_output)]
    
    flag_output = False
    if checkbox_bttns[1] in choice:
        if checkbox_bttns[0] in choice:
            flag_output = True
        return [gr.update(visible=True), gr.update(visible=flag_output), gr.update(visible=flag_output),\
                gr.update(visible=True), gr.update(visible=flag_output), gr.update(visible=True)]
    
    return [gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),\
            gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)]
    

with demo:
    gr.Markdown('<h1 style="font-size:36px;">Speech Tool</h1>')

    checkbox_bttns = ['Modify', 'Transcribe']
    checkboxes = gr.CheckboxGroup(checkbox_bttns, label='Run modes')
  
    file_input = gr.File(label="Input File", visible=False, interactive=True)
    output_path_box = gr.Textbox(visible=False, value=output_path)

    speed_slider = gr.Slider(0, 10, value=1, label='Speed', visible=False)
    volume_slider = gr.Slider(-10, 10, value=0, label='Volume', visible=False)

    greet_btn = gr.Button("Run", variant='primary', visible=False)
        
    file_output_modify = gr.Audio(label="Modify output", visible=False)
    file_output_transcribe = gr.Textbox(label="Transcribe output", visible=False)

    checkboxes.change(filter, inputs=checkboxes, 
                                outputs=[file_input, speed_slider, volume_slider, greet_btn, file_output_modify, file_output_transcribe])

    greet_btn.click(fn=greet, inputs=[checkboxes, file_input, output_path_box, speed_slider, volume_slider], \
                              outputs=[file_output_modify, file_output_transcribe])


demo.launch()
