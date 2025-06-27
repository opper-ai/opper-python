import asyncio
import base64
import os
import sys

from opperai import Opper


opper = Opper(
    http_bearer=os.getenv("OPPER_API_KEY"),
)


async def async_transcribe_audio(path: str):
    media_input = f"data:audio/mp3;base64,{base64.b64encode(open(path, 'rb').read()).decode('utf-8')}"
    response = await opper.call_async(
        name="async_transcribe_audio",
        instructions="given an audio file, return the transcription of the audio",
        input={
            "_opper_media_input": media_input,  # this field name is required by opper
        },
        model="gcp/gemini-2.5-pro",
    )

    return response.message


def transcribe_audio(path: str):
    media_input = f"data:audio/mp3;base64,{base64.b64encode(open(path, 'rb').read()).decode('utf-8')}"
    response = opper.call(
        name="async_transcribe_audio",
        instructions="given an audio file, return the transcription of the audio",
        input={
            "_opper_media_input": media_input,  # this field name is required by opper
        },
        model="gcp/gemini-2.5-pro",
    )
    return response.message


if __name__ == "__main__":
    audio_path = "sample.mp3"
    run_type = sys.argv[1] if len(sys.argv) > 1 else "both"
    if run_type == "sync":
        print(transcribe_audio(audio_path))
    elif run_type == "async":
        print(asyncio.run(async_transcribe_audio(audio_path)))
    else:
        print("running both sync and async...")
        print(transcribe_audio(audio_path))
        print(asyncio.run(async_transcribe_audio(audio_path)))
