import sys
import json
import warnings
from openai import OpenAI
from dotenv import load_dotenv
from audio_functions import AudioManager
from utils import call_gpt, print_robot, print_user

RECORDING_DURATION = 30

def main():
    if len(sys.argv) != 2:
        print("Usage: run.py <PERSONA>")
        sys.exit(1)

    persona = sys.argv[1].upper()

    with open('personas.json', 'r') as file:
        data = json.load(file)

    personal_prompt = data[persona]['prompt']
    voice_id = data[persona]['voice_id']

    # Ignore specific user warnings about FP16 not being supported
    warnings.filterwarnings(
        'ignore', message='FP16 is not supported on CPU; using FP32 instead')

    # Initialize OpenAI
    load_dotenv()
    client = OpenAI()

    # The AudioManager class holds functions for ASR & TTS
    am = AudioManager()

    while True:
        # Record and save the user's speech
        audio = am.record_audio(duration=RECORDING_DURATION)
        audio_path = am.save_audio(audio)

        # Transcribe the user's speech
        transcribed_audio = am.transcribe_audio(audio_path)
        print_user(transcribed_audio)

        gpt_prompt = f"""
            You are an character with the following persona: {personal_prompt}.
            You are supposed to respond to the following discussion: {transcribed_audio}.
        """

        messages = [{
            'role': 'user',
            'content': gpt_prompt
        }]

        comment = call_gpt(client, messages, "gpt-4-1106-preview")
        print_robot(comment)
        am.stream_and_play(comment, voice_id)


if __name__ == "__main__":
    main()
