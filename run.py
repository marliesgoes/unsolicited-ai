import sys
import json
import time
import warnings
from openai import OpenAI
from dotenv import load_dotenv
from audio_manager import AudioManager
from utils import call_gpt, print_robot, print_user
from animation_manager import AnimationManager

RECORDING_DURATION = 5
SLEEP_DURATION = 3

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
    anim_manager = AnimationManager()

    while True:
        # Record and save the user's speech
        print("top")
        audio = am.record_audio(duration=RECORDING_DURATION)
        audio_path = am.save_audio(audio)

        # Transcribe the user's speech
        transcribed_audio = am.transcribe_audio(audio_path)
        print_user(transcribed_audio)

        gpt_prompt = f"""
            You are an character with the following persona: {personal_prompt}.
            You are supposed to respond to the following discussion: {transcribed_audio}.
            Repeat the part of the discussion you are commenting on, before giving your opinion.
        """

        messages = [{
            'role': 'user',
            'content': gpt_prompt
        }]

        comment = call_gpt(client, messages, "gpt-4-1106-preview")
        print_robot(comment)
        # am.stream_and_play(comment, voice_id)
        print("about to stream")
        audio_path = am.stream_and_play(comment, voice_id)
        anim_manager.animate_character_with_audio(audio_path, speaking=True)

        # anim_manager.animate_character(speaking=True)
        time.sleep(SLEEP_DURATION)
    
    # pygame.quit()


if __name__ == "__main__":
    main()
