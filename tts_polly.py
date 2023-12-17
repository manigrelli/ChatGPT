import os
import boto3

import globals as G
from chatbot_logger import chat_log, trace
from player_recorder import audio_player
from chatbotgpt import ChatBotGpt

# https://aws.amazon.com/polly/
# https://docs.aws.amazon.com/polly/latest/dg/API_SynthesisTask.html#polly-Type-SynthesisTask-SnsTopicArn
# https://docs.aws.amazon.com/polly/latest/dg/API_SynthesizeSpeech.html
# https://docs.aws.amazon.com/polly/latest/dg/voicelist.html


polly = None
voices = ChatBotGpt.voices


# ---------------------------------------------------------------------------------------

def play_tts(text, voice=None, save_mp3='content/Gpt.mp3', debug=False, **kwargs):
    """"""
    trace(log=True)

    global polly
    if polly is None:
        try:
            polly = boto3.client(
                'polly',
                aws_access_key_id=G.AWS_ACCESS,
                aws_secret_access_key=G.AWS_SECRET,
            )
        except Exception as e:
            chat_log.logger.critical(f"{trace()}: Trying to load pollyTTs driver: {e}")
        else:
            chat_log.logger.info(f"{trace()}: Loaded pollyTTS driver")

    tts_module = "tts_polly"
    save_mp3 = os.path.join(G.PY_CWD, save_mp3)

    text = text.replace(",", " ")  # tts has very long delay on commas. remove them.
    voice = voices.choose_voice(tts_module=tts_module, voice=voice)
    voice_detail = voices.get_voice_detail(tts_module, voice)

    if debug:
        print(f"{voice}:  {text}")

    try:
        if os.path.exists(save_mp3):
            os.remove(save_mp3)

        response = polly.synthesize_speech(Text=text, VoiceId=voice, OutputFormat='mp3')
        body = response['AudioStream'].read()

        with open(save_mp3, 'wb') as file:
            file.write(body)
    except Exception as e:
        chat_log.logger.critical(f"{trace()}: {e}")
    else:
        audio_player(mp3_file_name=save_mp3)

# ---------------------------------------------------------------------------------------


if __name__ == "__main__":
    from common import parse_dotini
    parse_dotini(file=".env")
    play_tts(f'How would you like to play with my little razor blades', voice="Giorgio", debug=True)