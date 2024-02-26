import os
import wavio
import whisper
import sounddevice as sd

from elevenlabs import generate, play

class AudioManager:

    def __init__(self):
        self.model = whisper.load_model("base")
        self.api_key = os.environ.get('ELEVEN_API_KEY')

    def record_audio(self, duration=5, fs=44100):
        """
        Record audio from the microphone for a specified duration and sampling rate.
        """
        print("Listening...")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        print("Recording finished")
        return audio

    def save_audio(self, audio, filename="input.wav", fs=44100):
        """
        Save the recorded audio to a WAV file.
        """
        wavio.write(filename, audio, fs, sampwidth=2)
        return filename

    def transcribe_audio(self, audio_path):
        """
        Transcribe the audio at the given path using Whisper.
        """
        result = self.model.transcribe(audio_path)
        os.remove(audio_path)
        return result["text"]

    def stream_and_play(self, text, voice_id):
        """
        Use ElevenLabs' API to stream the audio and play the bot's response.
        """
        audio = generate(
            api_key=self.api_key,
            text=text,
            voice=voice_id,
        )

        with open("audio", 'wb') as audio_file:
            audio_file.write(audio)

        
        return "audio"

        # play(audio)
