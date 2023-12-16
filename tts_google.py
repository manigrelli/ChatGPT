import os
from gtts import gTTS


import globals as G
from chatbot_logger import chat_log, trace
from player_recorder import audio_player
from chatbotgpt import ChatBotGpt

# https://pypi.org/project/gTTS/
# https://www.geeksforgeeks.org/convert-text-speech-python/
# https://gtts.readthedocs.io/en/latest/module.html#localized-accents
#
# If you call "gtts-cli --all" from a command prompt, you can see that gTTS
# actually supports a lot of voices. However, you can only change the accents,
# and not the gender.


voices = ChatBotGpt.voices

# ---------------------------------------------------------------------------------------


def play_tts(text, voice=None, save_mp3='content/Gpt.mp3', debug=False, **kwargs):
    """"""
    trace(log=True)

    tts_module = "tts_google"
    # print(f"Debug: Start {tts_module}....")
    save_mp3 = os.path.join(G.PY_CWD, save_mp3)

    text = text.replace(",", " ")  # tts has very long delay on commas. remove them.
    voice = voices.choose_voice(tts_module=tts_module, voice=voice)
    voice_detail = voices.get_voice_detail(tts_module, voice)

    lang = kwargs.pop('lang', voice_detail["lang"])
    slow = kwargs.pop('slow', voice_detail["slow"])
    tld = kwargs.pop('tld', voice_detail["tld"])

    if debug:
        print(f"{voice}:  {text}")

    try:
        gTTS(text=text, lang=lang, slow=slow, tld=tld).save(save_mp3)
    except Exception as e:
        chat_log.logger.critical(f"{trace()}: {e}")
    else:
        audio_player(mp3_file_name=save_mp3)

# ---------------------------------------------------------------------------------------


if __name__ == "__main__":
    message = f"Hi, my name is Loretta.  Lets talk about life and razor blades"
    # message = "Welcome to GPTChatBot.  To exit the chat, just say 'goodbye'.  Do you want to create an introduction?"
    play_tts(f'How would you like to play with my little razor blades', slow=True, debug=True)