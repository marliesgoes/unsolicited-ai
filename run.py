import json
import time
import warnings
import argparse
from openai import OpenAI
from threading import Thread
from dotenv import load_dotenv
from audio_manager import AudioManager
from animation_manager import AnimationManager
from utils import call_gpt, print_robot, print_user

RECORDING_DURATION = 30
SLEEP_DURATION = 0

def handle_audio_and_animation(anim_manager, persona, silent_mode):
    with open('personas.json', 'r') as file:
        data = json.load(file)

    personal_prompt = data[persona]['prompt']
    voice_id = data[persona]['voice_id']

    warnings.filterwarnings('ignore', message='FP16 is not supported on CPU; using FP32 instead')
    load_dotenv()
    
    client = OpenAI()
    am = AudioManager()

    while True:
        audio = am.record_audio(duration=RECORDING_DURATION)
        audio_path = am.save_audio(audio)

        transcribed_audio = am.transcribe_audio(audio_path)
        print_user(transcribed_audio)

        gpt_prompt = f"""
            You are a character with the following persona: {personal_prompt}.
            You are supposed to respond to the following discussion: {transcribed_audio}.
        """

        messages = [{'role': 'user', 'content': gpt_prompt}]
        comment = call_gpt(client, messages, "gpt-4-1106-preview")
        print_robot(comment)

        if not silent_mode:
            anim_manager.set_speaking(True)
            am.stream_and_play(comment, voice_id)
            anim_manager.set_speaking(False)
        else:
            print("Audio output is disabled. Silent mode is active.")

        time.sleep(SLEEP_DURATION)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run conversational AI with optional silent mode.")
    parser.add_argument('persona', type=str, help='Persona to use for the conversation.')
    parser.add_argument('--silent', action='store_true', help='Toggle off audio output if set.')

    args = parser.parse_args()

    persona = args.persona.upper()
    silent_mode = args.silent

    anim_manager = AnimationManager(persona)
    audio_thread = Thread(target=handle_audio_and_animation, args=(anim_manager, persona, silent_mode,), daemon=True)
    audio_thread.start()
    anim_manager.run()