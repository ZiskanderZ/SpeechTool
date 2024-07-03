import argparse
import json
import os
from pydub import AudioSegment
from transformers import pipeline
import warnings
warnings.simplefilter("ignore")


class SpeechTool:


    def __init__(self, model_name="openai/whisper-small"):

        self.model_name = model_name

        self.transcriber = pipeline(task="automatic-speech-recognition", model=model_name)

    
    def speed_change(self, sound: AudioSegment, speed: float = 1.0) -> AudioSegment:
        """
        Changes the speed of the input audio segment.

        Args:
            sound (AudioSegment): The input audio segment to be altered.
            speed (float, optional): Speed multiplier for the audio. Defaults to 1.0.

        Returns:
            AudioSegment: Audio segment with altered speed.
        """

        sound_with_altered_frame_rate = sound._spawn(sound.raw_data, 
                                                     overrides={"frame_rate": int(sound.frame_rate * speed)})

        return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


    def modify_audio(self, input_path: str, output_path: str, speed: float = 1.0, volume: float = 0.0) -> str:
        """
        Modifies audio file by adjusting speed and volume if specified.

        Args:
            input_path (str): Path to the input audio file (must be WAV format).
            output_path (str): Path to save the modified audio file.
            speed (float, optional): Speed multiplier for the audio. Defaults to 1.0.
            volume (float, optional): Volume adjustment in dB. Defaults to 0.0.

        Returns:
            str: Path to the modified audio file.
        """

        audio = AudioSegment.from_wav(input_path)
        
        if speed != 1.0:
            audio = self.speed_change(audio, speed)
        
        if volume != 0.0:
            audio = audio + volume 

        output_file = os.path.basename(input_path).split(".")[0]
        output_path = os.path.join(output_path, f"modified_{output_file}.wav")
        audio.export(output_path, format="wav")
        print(f"Modified audio saved as {output_path}")
        return output_path
    

    def transcribe_audio(self, input_path: str, output_path: str) -> dict:
        """
        Transcribes audio from the input file and saves the transcription as JSON.

        Args:
            input_path (str): Path to the input audio file (format must be compatible with the transcriber).
            output_path (str): Directory path where the transcription JSON file will be saved.

        Returns:
            str: Transcription result.
        """

        result = self.transcriber(input_path)
        
        output_file = os.path.basename(input_path).split(".")[0]
        output_path = os.path.join(output_path, f"transcription_{output_file}.json")
        with open(output_path, "w", encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        
        print(f"Transcription saved as {output_path}")
        return result['text']


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="WAV Audio Processing Tool")
    parser.add_argument("input_path", type=str, help="Input WAV file path")
    parser.add_argument("output_path", type=str, help="Output folder path")
    parser.add_argument("--speed", type=float, default=1.0, help="Speed adjustment factor (default=1.0)")
    parser.add_argument("--volume", type=float, default=0.0, help="Volume adjustment in dB (default=0.0)")
    parser.add_argument("--transcribe", action="store_true", help="Transcribe audio to text")
    parser.add_argument("--modify", action="store_true", help="Modify audio (speed/volume)")

    args = parser.parse_args()

    tool = SpeechTool()

    if args.modify:
        tool.modify_audio(args.input_path, args.output_path, speed=args.speed, volume=args.volume)
    
    if args.transcribe:
        tool.transcribe_audio(args.input_path, args.output_path)