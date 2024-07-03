# Speech Tool

## Overview

`SpeechTool` is a Python-based tool for processing and transcribing WAV audio files. It allows you to adjust the speed and volume of audio files and transcribe speech to text using pre-trained models. The tool supports both command-line usage and a simple graphical interface using Gradio.

## Features

- Modify the speed and volume of WAV audio files.
- Transcribe audio to text in English and Russian using state-of-the-art machine learning models.
- Simple command-line interface for batch processing.
- Graphical interface for easy interaction.

## Installation

### To local

1. Clone the repository:
    ```sh
    git clone https://github.com/your-repo/SpeechTool.git
    cd SpeechTool
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    sudo apt-get install -y ffmpeg
    ```

### From Docker

```
docker build -t speechtool .
docker run -it  speechtool
```


## Usage

### Command-Line Interface

The main script for processing audio files is `src/speech_tool.py`. It accepts several command-line arguments:

```sh
usage: src/speech_tool.py [-h] [--speed SPEED] [--volume VOLUME] [--transcribe] [--modify] input_path output_path

WAV Audio Processing Tool

positional arguments:
  input_path            Input WAV file path
  output_path           Output folder path

optional arguments:
  -h, --help            show this help message and exit
  --speed SPEED         Speed adjustment factor (default=1.0)
  --volume VOLUME       Volume adjustment in dB (default=0.0)
  --transcribe          Transcribe audio to text
  --modify              Modify audio (speed/volume)
```

### Graphical Interface

You can also use the graphical interface provided by Gradio for a more user-friendly experience. To launch the Gradio interface, run:

```sh
python src/gui.py
```

## Examples

### To modify the speed and volume of an audio file:
```sh
python src/speech_tool.py data/input/en_example.wav data/output --speed 1.5 --volume 5 --modify
```

### To transcribe the audio to text:

```sh
python src/speech_tool.py data/input/en_example.wav data/output --transcribe
```

### To modify the speed and volume of an audio file and transcribe the audio to text:

```sh
python src/speech_tool.py data/input/en_example.wav data/output --speed 1.5 --volume 5 --modify --transcribe
```

## Data

Test audio files are located in the `data/input` directory:

`en_example.wav`: Example audio file in English.

`ru_example.wav`: Example audio file in Russian.

Processed audio files and transcriptions will be saved in the `data/output` directory.