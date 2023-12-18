import os, re, configparser

from dataclasses import dataclass  # https://martinheinz.dev/blog/78

from chatbot_logger import chat_log, trace
import globals as G


# ---------------------------------------------------------------------------------------


@dataclass
class RegExpNoCase(str):
    string: str
    match: re.Match = None

    def __eq__(self, pattern):
        self.match = re.search(pattern, self.string, flags=re.IGNORECASE)
        return self.match is not None


# ---------------------------------------------------------------------------------------


def str2bool(v):
    """"""
    trace(log=True)
    return v.lower() in ("yes", "true", "t", "1")


# ---------------------------------------------------------------------------------------

def parse_dotini(file="config.ini"):
    """"""
    trace(log=True)
    
    if not os.path.exists(file):
        chat_log.logger.error(f"{trace()}: File or path does not exist: '{file}'")
        return

    try:
        config = configparser.ConfigParser()
        config.read(file)

        G.GPT_MODEL = config.get('Open AI', 'gpt_model', fallback=None)
        G.STT_MODEL = config.get('Speech To Text', 'model', fallback=None)
        if not G.STT_MODEL:
            G.STT_MODEL = "AWS"

        G.OPENAI_API = config.get('Open AI', 'api_key', fallback=None)
        G.OPENAI_ORG = config.get('Open AI', 'organization_key', fallback=None)

        G.ELEVEN_API = config.get('Eleven Labs', 'api_key', fallback=None)

        G.AWS_ACCESS = config.get('Amazon Web Services', 'access_key', fallback=None)
        G.AWS_SECRET = config.get('Amazon Web Services', 'secret_access_key', fallback=None)
        G.AWS_REGION = config.get('Amazon Web Services', 'default_region', fallback=None)
        if G.AWS_REGION:
            os.environ["AWS_DEFAULT_REGION"] = G.AWS_REGION
    except Exception as e:
        chat_log.logger.critical(f"{trace()}: Trying to load dot-ini '{file}': {e}")


# ---------------------------------------------------------------------------------------


def api_check_key_status(show=True):
    """ Checks the environment vars are 'present' for each API key and then sets their global variable"""
    trace(log=True)

    rv = 1
    print_rv = []

    try:
        driver = "ElevenLabs"
        if G.ELEVEN_API:
            G.API_STATE[driver] = True
    except Exception as e:
        chat_log.logger.error(f"{trace()}: {driver} error: {e}")
        rv = 0

    try:
        driver = "OpenAI"
        key_list = (G.OPENAI_API, G.OPENAI_ORG)
        if len([k for k in key_list if k]) == len(key_list):
            G.API_STATE[driver] = True
    except Exception as e:
        chat_log.logger.error(f"{trace()}: {driver} error: {e}")
        rv = 0

    try:
        driver = "AWS"
        key_list = G.AWS_ACCESS , G.AWS_SECRET , G.AWS_REGION
        if len([k for k in key_list if k]) == len(key_list):
            G.API_STATE[driver] = True
    except Exception as e:
        chat_log.logger.error(f"{trace()}: {driver} error: {e}")
        rv = 0

    if show:
        print("\n{0:30} {1}".format("API_KEY_FILE", G.DOT_INI))
        print_rv.append("{0:30} {1}".format("ELEVENLABS_KEY", G.ELEVEN_API))
        print_rv.append("{0:30} {1}".format("OPEN_AI_KEY", G.OPENAI_API))
        print_rv.append("{0:30} {1}".format("OPEN_AI_ORG", G.OPENAI_ORG))
        print_rv.append("{0:30} {1}".format("AWS_ACCESS_KEY_ID", G.AWS_ACCESS))
        print_rv.append("{0:30} {1}".format("AWS_SECRET_ACCESS_KEY", G.AWS_SECRET))
        print_rv.append("{0:30} {1}".format("AWS_DEFAULT_REGION", G.AWS_REGION))
        print("\n".join(print_rv))
        for k, v in G.API_STATE.items():
            v = ["Not Configured", "Configured"][v]
            print("{0:30} {1}".format(k, v))
        print()
    return rv


# ---------------------------------------------------------------------------------------

def check_var_range(var_name, val, min_value, max_value):
    """"""
    trace(log=True)

    try:
        if val in ("True", "False"):
            val = str2bool(val)
        x = int(val)
        if x < min_value or x > max_value:
            x = x / 0
        else:
            return True
    except ZeroDivisionError:
        print(f"Error: {var_name} value ({val}) out of bounds [{min_value}..{max_value}]")
    except Exception as e:
        chat_log.logger.error(f"{trace()}: {e}")
    return False


# ---------------------------------------------------------------------------------------


def menu_set_voice(botobj, voice):
    """"""
    trace(log=True)

    # from menu:
    # set voice <int|str> : Change voice using index or voice name
    if voice.isdigit():
        try:
            voice = int(voice) - 1
            if voice < 0:
                voice = voice / 0
            chatbot_voice = botobj.voices.list_of_names[voice]
        except Exception:
            print(f"hmmm...expected 1..{len(botobj.voices.names)}")
            chatbot_voice = None
    else:
        if voice in botobj.voices.names:
            chatbot_voice = voice
        else:
            print(f"Sorry, the '{voice}' voice is not programmed")
            chatbot_voice = None

    if chatbot_voice:
        botobj.change_voice(new_voice=chatbot_voice, change_filename=False)


# ---------------------------------------------------------------------------------------


def parse_user_answer(ans):
    """"""
    trace(log=True)

    arg1 = arg2 = ""
    argv = re.sub('\s+', ' ', ans)
    arg1, arg2 = (argv + " ").split(" ", maxsplit=1)
    arg2 = arg2.strip()
    ans = ans.strip()
    return ans, argv, arg1, arg2


# ---------------------------------------------------------------------------------------


if __name__ == "__main__":
    # parse_dotini()
    # api_check_key_status()
    pass
