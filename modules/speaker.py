import subprocess
import os

class Speaker:
    def __init__(self, model_path="models/piper/en_US-lessac-medium.onnx", config_path="models/piper/en_US-lessac-medium.onnx.json"):
        self.model = model_path
        self.config = config_path
        self.executable = "piper" # Assumes piper is in your PATH

    def say(self, text):
        if not text:
            return

        # We pipe the text into piper, then pipe piper's output into aplay
        # This avoids writing large files to the SD card constantly
        command = (
            f'echo "{text}" | '
            f'{self.executable} --model {self.model} --config {self.config} --output_raw | '
            f'aplay -r 22050 -f S16_LE -t raw'
        )
        
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error in TTS playback: {e}")