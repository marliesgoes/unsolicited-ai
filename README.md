# unsolicited-ai

## Installation

### Credentials

You'll need OpenAI and ElevenLabs API keys in your environment.

```
export OPENAI_API_KEY=...
export ELEVEN_API_KEY=...
```

### Dependencies
Install requirements.

```
pip install -r requirements.txt
brew install mpv
```

### Usage

1. Add your character description to the [personas.json](https://github.com/marliesgoes/unsolicited-ai/blob/main/personas.json).
2. Clone your voice with [elevenlabs.io](https://elevenlabs.io/app/voice-lab). Add the voice_id from elevenlabs to the [personas.json](https://github.com/marliesgoes/unsolicited-ai/blob/main/personas.json). If you skip this step, a default voice will be used.
3. Add the frames of your personal avatar animation in the folder `images/<YOUR NAME>/` and make sure the images are named in the format `idle*.png` and `speaking*.png`, where the `*` indicates the index of the frame within the animation. If you skip this step, a default animation will be used.


