import gradio as gr
from speech_tool import SpeechTool
from pathlib import Path

class GUI:

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
    checkbox_bttns = ['Modify', 'Transcribe']

    def __init__(self) -> None:
        """
        Initialize the GUI class.
        """

        self.contstruct()


    def process(self, modes: list[str], file_input: dict, output_path: str, speed: float, volume: float) -> list:
        """
        Process the audio file based on selected modes.
        
        Args:
            modes (list[str]): List of selected modes ('Modify' and/or 'Transcribe').
            file_input (dict): The input audio file.
            output_path (str): Path to the output folder.
            speed (float): Speed adjustment factor.
            volume (float): Volume adjustment in dB.
        
        Returns:
            list: The output results for each mode.
        """

        output = [None, None]
        if self.checkbox_bttns[0] in modes:
            result = self.st.modify_audio(file_input, output_path, speed, volume)
            output[0] = result 

        if self.checkbox_bttns[1] in modes:
            result = self.st.transcribe_audio(file_input, output_path)
            output[1] = result 

        return output


    def filter(self, choice: list[str]) -> list:
        """
        Filter the visibility of UI elements based on selected modes.
        
        Args:
            choice (list[str]): List of selected modes.
        
        Returns:
            list: List of visibility updates for UI elements.
        """
        
        flag_output = False
        if self.checkbox_bttns[0] in choice:
            if self.checkbox_bttns[1] in choice:
                flag_output = True

            return [gr.update(visible=True), gr.update(visible=True), gr.update(visible=True),\
                    gr.update(visible=True), gr.update(visible=True), gr.update(visible=flag_output)]
        
        flag_output = False
        if self.checkbox_bttns[1] in choice:
            if self.checkbox_bttns[0] in choice:
                flag_output = True
            return [gr.update(visible=True), gr.update(visible=flag_output), gr.update(visible=flag_output),\
                    gr.update(visible=True), gr.update(visible=flag_output), gr.update(visible=True)]
        
        return [gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),\
                gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)]
        

    def contstruct(self) -> None:
        """
        Construct the GUI layout.
        """

        with self.demo:
            gr.Markdown('<h1 style="font-size:36px;">Speech Tool</h1>')

            checkboxes = gr.CheckboxGroup(self.checkbox_bttns, label='Run modes')
        
            file_input = gr.File(label="Input File", visible=False, interactive=True)
            output_path_box = gr.Textbox(visible=False, value=self.output_path)

            speed_slider = gr.Slider(0, 10, value=1, label='Speed', visible=False)
            volume_slider = gr.Slider(-10, 10, value=0, label='Volume', visible=False)

            greet_btn = gr.Button("Run", variant='primary', visible=False)
                
            file_output_modify = gr.Audio(label="Modify output", visible=False)
            file_output_transcribe = gr.Textbox(label="Transcribe output", visible=False)

            checkboxes.change(self.filter, inputs=checkboxes, 
                                        outputs=[file_input, speed_slider, volume_slider, greet_btn, file_output_modify, file_output_transcribe])

            greet_btn.click(fn=self.process, inputs=[checkboxes, file_input, output_path_box, speed_slider, volume_slider],\
                                    outputs=[file_output_modify, file_output_transcribe])


    def run(self) -> None:
        """
        Run the GUI application.
        """

        self.demo.launch()


if __name__ == '__main__':

    gui = GUI()
    gui.run()
