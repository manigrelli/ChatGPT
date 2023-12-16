import os, pyttsx3

import globals as G
from chatbot_logger import chat_log, trace
from chatbotgpt import ChatBotGpt

# https://www.geeksforgeeks.org/python-text-to-speech-by-using-pyttsx3/
# https://www.geeksforgeeks.org/text-to-speech-changing-voice-in-python/

converter = pyttsx3.init()
voices = ChatBotGpt.voices

# ---------------------------------------------------------------------------------------


def play_tts(text, voice=None, save_mp3=None, debug=False, **kwargs):
    """"""
    trace(log=True)

    tts_module = "tts_pyx3"
    voice = voices.choose_voice(tts_module=tts_module, voice=voice)
    voice_detail = voices.get_voice_detail(tts_module, voice)

    rate = kwargs.pop('rate', voice_detail["rate"])
    volume = kwargs.pop('volume', voice_detail["volume"])

    if debug:
        print(f"rate={rate}  volume={volume}")
        print(f"{voice}:  {text}")

    converter.setProperty('voice', voice_detail["ID"])
    converter.setProperty('rate', rate)  # Sets speed percent. Can be more than 100
    converter.setProperty('volume', volume)  # Set volume 0-1

    try:
        if save_mp3:
            save_mp3 = os.path.join(G.PY_CWD, save_mp3)
            converter.save_to_file(text, save_mp3)

        # Queue the entered text. There will be a pause between each one like a pause in a sentence.
        # converter.say("Hello GeeksforGeeks")
        # converter.say("I'm also a geek")
        for sentence in text.split("."):
            converter.say(sentence)

        # Empties the say() queue Program will not continue until all speech is done talking
        converter.runAndWait()
    except Exception as e:
        chat_log.logger.critical(f"{trace()}: {e}")

# ---------------------------------------------------------------------------------------


def find_ms_installed_voices():
    """"""
    trace(log=True)

    print("\nThis lists all the MS voices in the registry on this computer:")
    for voice in converter.getProperty('voices'):
        print("Voice:")
        print("\tID: %s" % voice.id)
        print("\tName: %s" % voice.name)
        print("\tAge: %s" % voice.age)
        print("\tGender: %s" % voice.gender)
        print("\tLanguages Known: %s" % voice.languages)
        print()

# ---------------------------------------------------------------------------------------


if __name__ == "__main__":
    find_ms_installed_voices()
    play_tts(f'How would you like to play with my little razor blades', voice="female", debug=True)