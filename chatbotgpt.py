import openai, json, textwrap
from importlib import import_module

from common import *
from chatbot_logger import chat_log, trace, my_stack
from tts_voices import Voices


# #####################################################################################
#
#        ,gggg,                                      ,ggggggggggg,
#      ,88"""Y8b, ,dPYb,                   I8       dP"""88""""""Y8,               I8
#     d8"     `Y8 IP'`Yb                   I8       Yb,  88      `8b               I8
#    d8'   8b  d8 I8  8I                88888888     `"  88      ,8P            88888888
#   ,8I    "Y88P' I8  8'                   I8            88aaaad8P"                I8
#   I8'           I8 dPgg,     ,gggg,gg    I8            88""""Y8ba    ,ggggg,     I8
#   d8            I8dP" "8I   dP"  "Y8I    I8            88      `8b  dP"  "Y8ggg  I8
#   Y8,           I8P    I8  i8'    ,8I   ,I8,           88      ,8P i8'    ,8I   ,I8,
#   `Yba,,_____, ,d8     I8,,d8,   ,d8b, ,d88b,          88_____,d8',d8,   ,d8'  ,d88b,
#     `"Y8888888 88P     `Y8P"Y8888P"`Y888P""Y88        88888888P"  P"Y8888P"   88P""Y88
#
# #######################################################################################

class ChatBotGpt:
    created = 0
    objects = list()
    voices = Voices()

    def __init__(self, name, voice, intro=None, welcome_file=None, restart_db=True):
        trace(__name__, log=True)
        chat_log.logger.info(f"{my_stack(__name__)}: Init {name}")
        ChatBotGpt.created += 1
        ChatBotGpt.objects.append(self)

        self.name = name

        self.voice = voice
        tts_module = ChatBotGpt.voices.get_module_name(voice)
        self.text_to_speech = getattr(import_module(tts_module), "play_tts")

        self.intro = intro
        if intro is not None:
            self.intro = intro
            self.intro = ChatBotGpt.clean_chat_message(text=intro)

        # todo: what is this for: welcome
        self.welcome_file = welcome_file
        if welcome_file is None:
            self.welcome_file = "content/welcome.mp3"

        # These files may or may not be present.  No big deal.
        self.mp3_filename = os.path.join(G.PY_CWD, "content", f"{self.name}.mp3")
        self.db_filename = os.path.join(G.PY_CWD, "databases", f"db_{self.name}.json")

        if restart_db:
            if os.path.exists(self.db_filename):
                os.remove(self.db_filename)

        # tokens:  roughly 1 token ~= 4 chars in English
        # https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them
        # i don't know if these are counted for each transaction (including the entire json) or just the latest?
        # So this is not implemented right now...
        # self.token_cnt = 0
        # self.bytes_cnt = 0

    # ---------------------------------------------------------------------------------------

    @staticmethod
    def clean_chat_message(text, add_limit=True):
        """"""
        trace(log=True)

        # To Do: research good method of cleaning to save on tokens
        # could get fancy and have lots of different models and assign to
        # different tts engines

        text = re.sub('[\s]+', ' ', text)
        text = re.sub(',', ' ', text)
        if add_limit:
            text += f". Keep responses UNDER {G.MAX_WORDS} words"
        return text.strip()

    # ---------------------------------------------------------------------------------------

    @staticmethod
    def transcribe_audio(file):
        """"""
        trace(log=True)

        openai.api_key = G.OPENAI_API
        openai.organization = G.OPENAI_ORG

        if type(file) is str:
            # received a filename 'string'
            filename = file
            if not os.path.isabs(filename):
                # Needed for pyInstaller environment
                filename = os.path.join(G.PY_CWD, filename)

        else:
            # received file content (ie from postman)
            filename = file.filename
            # Save the blob first
            with open(file.filename, 'wb') as buffer:
                buffer.write(file.file.read())

        try:
            audio_file = open(filename, "rb")
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            print("\nUser: ", "\n".join(textwrap.wrap(transcript["text"], G.TEXT_WRAP)) + "\n")
            chat_log.logger.info(f"{trace()} Open-AI STT: {transcript['text']}")
            return transcript["text"]
        except Exception as e:
            chat_log.logger.critical(f"{trace()}: {e}")

    # def num_tokens_from_string(text, encoding_name="cl100k_base"):
    #     encoding = tiktoken.get_encoding(encoding_name)
    #     num_tokens = len(encoding.encode(text))
    #     return num_tokens

    # ---------------------------------------------------------------------------------------

    def change_voice(self, new_voice, change_filename=True):
        """"""
        trace(log=True)

        tts_module = ChatBotGpt.voices.get_module_name(new_voice)
        self.voice = new_voice
        self.text_to_speech = getattr(import_module(tts_module), "play_tts")

        if change_filename:
            self.mp3_filename = os.path.join(G.PY_CWD, "content", f"{new_voice}.mp3")

    # ---------------------------------------------------------------------------------------

    def get_chat_response(self, user_message, gpt_name="GptBot"):
        """"""
        trace(log=True)

        openai.api_key = G.OPENAI_API
        openai.organization = G.OPENAI_ORG

        messages = self.load_messages()

        if G.ENABLE_LIMIT:
            # chat log will remain small to keep tokens low
            if (len(messages) -1)/2 > G.MAX_CHAT:
                chat = []
                if G.MAX_CHAT:
                    chat = messages[-G.MAX_CHAT*2:]
                messages = [messages[0]] + chat

        messages.append({"role": "user", "content": user_message})

        chat_log.logger.info(f"{trace()}: User message -> {user_message}")
        # from pprint import pprint
        # pprint(messages)

        try:
            # Send to ChatGpt/OpenAi
            gpt_response = gpt_response = openai.ChatCompletion.create(
                model=G.GPT_MODEL,
                messages=messages
            )

            parsed_gpt_response = gpt_response['choices'][0]['message']['content']
            chat_log.logger.info(f"{trace()}: Open-AI Chat-GBT response length: {len(parsed_gpt_response)} bytes")

            # Save messages
            self.save_messages(user_message, parsed_gpt_response)
            print(f"\n{gpt_name}:\n" + "\n".join(textwrap.wrap(parsed_gpt_response, G.TEXT_WRAP)))
            return parsed_gpt_response
        except Exception as e:
            chat_log.logger.critical(f"{trace()}: {e}")

    # ---------------------------------------------------------------------------------------

    def load_messages(self):
        """"""
        trace(log=True)

        messages = []
        if not os.path.exists(self.db_filename):
            empty = True
        else:
            empty = os.stat(self.db_filename).st_size == 0

        if not empty:
            with open(self.db_filename) as db_file:
                data = json.load(db_file)
                for item in data:
                    messages.append(item)
        else:
            messages.append(
                {"role": "system", "content": self.intro.strip()}
            )
        return messages

    # ---------------------------------------------------------------------------------------

    def save_messages(self, user_message, gpt_response):
        """"""
        trace(log=True)

        file = self.db_filename

        messages = self.load_messages()
        messages.append({"role": "user", "content": user_message})
        messages.append({"role": "assistant", "content": gpt_response})

        with open(file, 'w') as f:
            json.dump(messages, f)
    # ---------------------------------------------------------------------------------------


if __name__ == "__main__":
    pass
