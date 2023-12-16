import os, requests

import globals as G
from chatbot_logger import chat_log, trace
from player_recorder import audio_player
from chatbotgpt import ChatBotGpt

# https://elevenlabs.io/

voices = ChatBotGpt.voices

# ---------------------------------------------------------------------------------------


def play_tts(text, voice=None, save_mp3='content/Gpt.mp3', debug=False, **kwargs):
    """"""
    trace(log=True)

    tts_module = "tts_elevenLabs"
    save_mp3 = os.path.join(G.PY_CWD, save_mp3)

    text = text.replace(",", " ")  # tts has very long delay on commas. remove them.
    voice = voices.choose_voice(tts_module=tts_module, voice=voice)
    voice_detail = voices.get_voice_detail(tts_module, voice)

    voice_id = kwargs.pop('voice_id', voice_detail["voice_id"])
    model_id = kwargs.pop('model_id', voice_detail["model_id"])
    stability = kwargs.pop('stability', voice_detail["stability"])
    similarity_boost = kwargs.pop('similarity_boost', voice_detail["similarity_boost"])
    style = kwargs.pop('style', voice_detail["style"])
    use_speaker_boost = kwargs.pop('use_speaker_boost', voice_detail["use_speaker_boost"])

    if debug:
        print(f"{voice}:  {text}")

    body = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
            "style": style,
            "use_speaker_boost": use_speaker_boost
        }
    }

    headers = {
        "Content-Type": "application/json",
        "accept": "audio/mpeg",
        "xi-api-key": G.ELEVEN_API
    }

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    try:
        if os.path.exists(save_mp3):
            os.remove(save_mp3)

        response = requests.post(url, json=body, headers=headers)
        if response.status_code == 200:
            with open(save_mp3, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        else:
            chat_log.logger.error(f"{trace()}: http response code {response.status_code} {response.reason}")

            if response.status_code == 401:
                chat_log.logger.error(f"{trace()}: Either key is invalid or have exceeded character input limit.")
    except Exception as e:
        chat_log.logger.critical(f"{trace()}: {e}")
    else:
        audio_player(mp3_file_name=save_mp3)

# ---------------------------------------------------------------------------------------


if __name__ == "__main__":
    import globals as G
    from common import api_check_key_status, parse_dotini

    parse_dotini(file=G.DOT_INI)
    api_check_key_status(show=False)
    play_tts('O', debug=True)
