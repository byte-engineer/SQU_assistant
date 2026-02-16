import os
import wave
import pyaudio
from faster_whisper import WhisperModel


class Listener:
    def __init__(self, model_size="small", device="cpu"):
        # Initialize Whisper Model (options: tiny, base, small, medium)
        self.model = WhisperModel(model_size, device=device, compute_type="int8")
        
        # Audio Settings
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = int(16000 * 2) # Whisper expects 16kHz
        self.chunk = int(1024 * 2)
        self.temp_file = "temp_recording.wav"
        
        self.audio = pyaudio.PyAudio()

    def listen_and_transcribe(self):
        """Records audio from the mic and returns the transcribed text."""
        print("Listening...")
        self._record_audio()
        
        # Transcribe the saved file
        print("-- transcribing --")
        segments, info = self.model.transcribe(self.temp_file, beam_size=5)
        
        # Combine segments into a single string
        user_text = " ".join([segment.text for segment in segments]).strip()
        
        # Clean up
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
            
        return user_text

    def _record_audio(self, silence_threshold=1500, silence_duration=1):
        """Records until a period of silence is detected."""
        stream = self.audio.open(format=self.format, channels=self.channels,
                                 rate=self.rate, input=True,
                                 frames_per_buffer=self.chunk)
        
        frames = []
        silent_chunks = 0
        # Calculate how many chunks represent the silence duration
        max_silent_chunks = int(silence_duration * (self.rate / self.chunk))

        while True:
            data = stream.read(self.chunk)
            frames.append(data)
            
            # Simple volume-based silence detection
            import numpy as np
            audio_data = np.frombuffer(data, dtype=np.int16)
            if np.abs(audio_data).mean() < silence_threshold:
                silent_chunks += 1
            else:
                silent_chunks = 0
            
            # Stop if user stops talking
            if silent_chunks > max_silent_chunks:
                break

        stream.stop_stream()
        stream.close()

        # Save to temp wav file
        with wave.open(self.temp_file, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))


if __name__ == "__main__":
    # 1. Initialize the listener
    # You can change model_size to "tiny" for faster performance on older CPUs
    print("--- Initializing SQU Assistant Listener ---")
    assistant_listener = Listener(model_size="base", device="cpu")
    
    try:
        while True:
            print("\n[READY] Say something (or press Ctrl+C to stop)...")
            
            # 2. Run the transcription process
            text = assistant_listener.listen_and_transcribe()
            
            # 3. Output the results
            with open("logs/LOG.txt", "a") as logfile: 
                if text:
                    print(f"User said: {text}")
                    logfile.write(f"User said: {text} \n")
                else:
                    print("No speech detected.")
                    logfile.write("No speech detected. \n")

    except KeyboardInterrupt:
        print("\n--- Listener Stopped by User ---")
    except Exception as e:
        print(f"An error occurred: {e}")