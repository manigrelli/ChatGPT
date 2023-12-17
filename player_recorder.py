import os
from time import time
import sounddevice as sd
from scipy.io.wavfile import write

from vosk import Model, KaldiRecognizer
import pyaudio

import globals as G
from chatbot_logger import chat_log, trace

# ---------------------------------------------------------------------------------------


def audio_player(mp3_file_name="content/user.mp3"):
    """"""
    trace()

    mp3_file_name = os.path.join(G.PY_CWD, mp3_file_name)
    try:
        assert os.path.exists(mp3_file_name) is True
        dos_cmd = f"{G.MP3_PLAYER} -q {mp3_file_name}"
        os.system(dos_cmd)
    except Exception as e:
        chat_log.logger.critical(f"{trace()}: {e}")
        # print(f"Debug: play_file = '{play_file}'")
        # print(f"Debug: mp3_file_name = '{mp3_file_name}'")
        # print(f"Debug: mp3 file exists = {os.path.exists(mp3_file_name)}")
        return False
    return True


# ---------------------------------------------------------------------------------------

def audio_recorder_stt(duration=15, model=None):
    """"""
    trace()

    if model is None:
        chat_log.logger.critical(f"{trace()}: model not defined (None)'")
        return

    model = os.path.join("models", model)
    if not os.path.exists(model):
        chat_log.logger.error(f"{trace()}: model directory does not exist '{model}'")
        return

    try:
        model = Model(model)
        recognizer = KaldiRecognizer(model, 16000)

        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        stream.start_stream()

        buffer = []
        watchdog = int(time() + duration)

        # records for the duration or a text buffer comes up empty (silence detected)
        print("** Start Recording...")

        while int(time()) <= watchdog:
            data = stream.read(4096)
            if recognizer.AcceptWaveform(data):
                text = recognizer.Result()[14:-3]
                if text:
                    print(f"{text}.")
                    buffer.append(text)
                else:
                    break

        print("** Stop!")
        text = ". ".join(buffer)
    except Exception as e:
        chat_log.logger.critical(f"{trace()}: Exception {e}'")
        return
    else:
        text = text.strip()
        if not text:
            print("Nothing recorded?")
        return text


# ---------------------------------------------------------------------------------------

def audio_recorder(duration=5, freq=44100, mp3_file_name="content/user.mp3", playback=False):
    """"""
    trace()

    try:
        duration = int(duration)
    except ValueError:
        print(f"ERROR: Rx duration='{duration}'. Expect an integer")
        chat_log.logger.error(f"{trace()}: Passed in duration of wrong type")
        duration = 5

    mp3_file_name = os.path.join(G.PY_CWD, mp3_file_name)
    audio_path = os.path.dirname(mp3_file_name)
    wav_file_name = f"{audio_path}/microphone.wav"

    for file_name in [wav_file_name, mp3_file_name]:
        if os.path.exists(file_name):
            os.remove(file_name)

    assert os.path.exists(mp3_file_name) is False
    assert os.path.exists(wav_file_name) is False
    # raise Exception(f"Why does {mp3_file_name} file exist? We just deleted it...")

    # Start recorder with the given values of duration and sample frequency
    print(f"** Start Recording...{duration} seconds")

    try:
        recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)

        # Record audio for the given number of seconds
        sd.wait()
        print("** Stop!")

        # Option 1: This will convert the NumPy array to an audio file with the given sampling frequency
        write(wav_file_name, freq, recording)

        # Option 2: Convert the NumPy array to audio file
        # wv.write(wav_file_name, recording, freq, sampwidth=2)
        assert os.path.exists(wav_file_name) is True
    except Exception as e:
        chat_log.logger.critical(f"{trace()}: {e}")
    else:
        try:
            dos_cmd = f"{G.WAV_TO_MP3} -b 128 --silent {wav_file_name}  {mp3_file_name}"
            os.system(dos_cmd)
        except Exception as e:
            chat_log.logger.critical(f"{trace()}: {e}")
        else:
            if not playback:
                return os.path.exists(wav_file_name)
            if os.path.exists(mp3_file_name):
                print("Playing back recording...")
                return audio_player(mp3_file_name=mp3_file_name)
    return False


if __name__ == '__main__':
    from common import parse_dotini
    parse_dotini(file=".env")

    if os.path.exists(os.path.join("models", G.STT_MODEL)):
        if audio_recorder_stt(duration=10):
            print("INFO: Recording successful")
        else:
            print("ERROR: Recording failed!!!")
    else:
        if audio_recorder(mp3_file_name="./content/test_mic.mp3", playback=False):
            print("INFO: Recording successful")
            if audio_player(mp3_file_name="./content/test_mic.mp3"):
                print("INFO: Playback successful")
            else:
                print("ERROR: Playback failed!!!")
        else:
            print("ERROR: Recording failed!!!")
