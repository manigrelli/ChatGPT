import json, textwrap
from pprint import pprint

from tts_voices import Voices
from player_recorder import audio_recorder, audio_recorder_stt

from common import *
import globals as G
# from chat_logger import chat_log

# ---------------------------------------------------------------------------------------


help_top_menu = """
    <text>           : Play <text> out speaker using TTS 
    chat     | c     : Start a fresh chat session
    listen   | l     : Listen to 'Bot vs Bot' 
    set      | s     : Show 'set' commands
    show     | sh    : Show 'show' commands
    help     | h     : For this help message
    quit     | q     : To return to Top Menu
    exit             : To exit application
    """

help_chat_menu = f"""
    [3..10]          : Number of seconds to record yourself
    <text>           : Type a message in lieu of recording yourself
    clear    | cl    : Clear chat session (same intro)
    start    | st    : Start a random preset chat
    set      | s     : Show 'set' commands
    show     | sh    : Show 'show' commands
    help     | h     : For this help message
    quit     | q     : To return to Top Menu
    exit             : To exit application
    """


debug_menu = f"""
   test <option>    : Short: 't <option>'
   .     gpt        : Test Open-AI GPT
   .     mic        : Test recording & speech-to-text
   .     stt        : Test each speech-to-text driver
   .     tts        : Test each text-to-speech driver
   .     voices     : Test all voices
   debug <option>   : Short: 'd <option>'
   .     api-key    : Show api key status
   .     interview  : Set intro to Python Interview
   .     logging    : Show logging info
   .     version    : Show version 
   """

show_menu = """
   show  <option>   : Short: 'sh <option>'
   .     chat       : Show current chat exchange
   .     config     : Show configuration
   .     history    : Show entire chat history
   .     intro      : Show chat introduction
   .     voices     : Show detail of all voices
   .     more       : Show more commands
   """

set_menu = f"""
   set <arg> <val>  : Short: 'se <arg> <val>'
   .   intro        : Set the introduction for a chat session
   .   log_level    : [0]Debug, [1]Info, [2]Warn, [3]Error, [4][Critical] 
   .   max_chat     : Limit the ChatGPT chat count [0..15]
   .   max_words    : Limit the ChatGPT word count [3..500]
   .   text_wrap    : Limit the console text length [25.150]
   .   stt_model    : set the STT model (AWS Polly or model directory name)
   .   voice <id>   : Change voice id using index or name
   .                : See 'show voices' for list
   """

for var in ["show_menu", "set_menu", "help_top_menu", "help_chat_menu", "debug_menu"]:
    new_table = re.sub('\n\s+', '\n', eval(var))
    new_table = re.sub('\n\.', '\n ', new_table)
    exec(f"{var} = new_table")


# ---------------------------------------------------------------------------------------


def ans_matched_common(args=None, botobj=None, ret_bool=True):
    """"""
    trace(log=True)

    ready_to_chat = False
    restart_db = False

    # this api is called by chat_with_bot (ret_boo=True) and chatbat_topmenu (ret_boo=False)
    if not ret_bool:
        ...

    test_string = "Testing 1 2 3"
    mp3_file_name = botobj.mp3_filename

    choice, argv, arg1, arg2 = args
    match RegExpNoCase(argv):
        # Common Set Commands: set param value
        case '^s[et]*\\s*\\??$':
            print(set_menu)

        case '^set [a-z_]+ .+$':
            param, value = arg2.split(" ", maxsplit=1)
            match RegExpNoCase(param):
                case '^int[ro]*$':
                    if value.lower() in ['none', '""', '-']:
                        botobj.intro = None
                    else:
                        # Change system introduction
                        botobj.intro = botobj.clean_chat_message(text=value, add_limit=True)
                    restart_db = True

                case '^enable_limit$':
                    # do not put this in 'set cli' help
                    if check_var_range(var_name=param, val=value, min_value=0, max_value=1):
                        G.ENABLE_LIMIT = str2bool(value)

                case '^log_level$':
                    if check_var_range(var_name=param, val=value, min_value=1, max_value=5):
                        value = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"][int(value)]
                        chat_log.logger.setLevel(value)

                case '^max_chat$':
                    if check_var_range(var_name=param, val=value, min_value=0, max_value=15):
                        G.MAX_CHAT = int(value)

                case '^max_words$':
                    if check_var_range(var_name=param, val=value, min_value=3, max_value=100):
                        G.MAX_WORDS = int(value)

                case '^stt_model$':
                    if value != "AWS Polly" and not os.path.exists(os.path.join("models", value)):
                        print(f"Error: param value ({value}) is invalid.  Expected 'AWS Polly' or a directory in ./models")
                    else:
                        G.STT_MODEL = value

                case '^text_wrap$':
                    if check_var_range(var_name=param, val=value, min_value=25, max_value=150):
                        G.TEXT_WRAP = int(value)

                case '^voi[ces]*$':
                    # Change voice using index or voice name
                    menu_set_voice(botobj=botobj, voice=value)
                    botobj.text_to_speech(f"I am now set to be {botobj.voice}", voice=botobj.voice)

                case _:
                    print(f"oops, cannot set '{param}'", end="\n\n")

        # Common: Show Commands
        case '^sh[ow]*\\s*\\??$':
            print(show_menu)

        case '^((sh|show) (\\?|voi[ces]*|int[ro]*|mor[e]*|con[fig]*|cha[t]*|log|his[tory]*))$':
            if not arg2: arg2 = arg1
            match RegExpNoCase(arg2):
                case '^con[fig]*$':
                    print()
                    print("{0:30} {1}".format("Parameter", "Value"))
                    print("=" * 50)
                    print("{0:30} {1}".format("Introduction", botobj.intro))
                    print("{0:30} {1}".format("GPT Voice", botobj.voice))
                    print("{0:30} {1}".format("TTS Driver", botobj.voices.get_module_name(botobj.voice)))
                    print("{0:30} {1}".format("max_words", G.MAX_WORDS))
                    print("{0:30} {1}".format("text_wrap", G.TEXT_WRAP))
                    print("{0:30} {1}".format("max_chat", G.MAX_CHAT))
                    print("{0:30} {1}".format("log_level", chat_log))
                    print("{0:30} {1}".format("enable_limit", bool(G.ENABLE_LIMIT)))

                    print("{0:30} {1}".format("ini_file", G.DOT_INI))
                    print("{0:30} {1}".format("gpt_model", G.GPT_MODEL))

                    print("{0:30} {1}".format("stt_model", G.STT_MODEL), end=" ")
                    if G.STT_MODEL != "AWS Polly" and not os.path.exists(os.path.join("models", G.STT_MODEL)):
                        print("(Invalid)")
                    else:
                        print()

                    for k, v in G.API_STATE.items():
                        v = ["Not Configured", "Configured"][v]
                        print("{0:30} {1}".format(k, v))
                    print()

                case '^int[ro]*$':
                    if botobj.intro is None:
                        print("Introduction has not been set")
                    else:
                        print("Introduction:\n" + "\n".join(textwrap.wrap(botobj.intro, G.TEXT_WRAP)))

                case '^(log|cha[t]*|his[tory]*)$':
                    if not os.path.exists(botobj.db_filename):
                        print("No history for the current chat")
                    else:
                        print()
                        c = 0
                        with open(botobj.db_filename) as db_file:
                            data = json.load(db_file)

                            if G.ENABLE_LIMIT and "his" not in arg2:
                                # This is the last chat exchange
                                if (len(data) - 1) / 2 > G.MAX_CHAT:
                                    chat = data[-2:]
                                    if G.MAX_CHAT:
                                        chat = data[-G.MAX_CHAT * 2:]
                                    data = [data[0]] + chat

                            for x, item in enumerate(data):
                                if item["role"] == "system":
                                    print("-----")
                                    print("----- Introduction:  ", end="")
                                    print("\n".join(textwrap.wrap(item["content"], G.TEXT_WRAP)))
                                    print("-----", end="\n\n")
                                    continue
                                else:
                                    if x % 2:
                                        c += 1
                                        print("", f"    #{c}    ", "", sep="-" * int(G.TEXT_WRAP / 2))
                                    if item["role"] == "user":
                                        print(f"You: ", end="")
                                    else:
                                        print(f"\nChatbot: ", end="")
                                    print("\n".join(textwrap.wrap(item["content"], G.TEXT_WRAP)))

                            print("-" * (G.TEXT_WRAP + 10), end="\n\n")

                case '^more$':
                    print(debug_menu)

                case '^voi[ces]*$':
                    for index, name in enumerate(botobj.voices.names):
                        print(f"\t{index + 1}\t{name}")

                case _:
                    print(f"oops, '{arg1}' command can not find an option for '{arg2}'", end="\n\n")

        # Common Test Commands
        case '^(t .+|(t|test )(gpt|mic|stt|tts|voices))$':
            if not arg2: arg2 = arg1
            match RegExpNoCase(arg2):
                case 'gpt':
                    botobj.intro = "Finish this rhyme in a humors way. Respond under 15 words"
                    print("\nIntroduction:", botobj.intro)
                    gpt_response = botobj.get_chat_response("Roses are red", gpt_name=f"ChatGPT")
                    botobj.text_to_speech(gpt_response, voice="David")
                    botobj.intro = None
                    print()

                case 'mic':
                    # Test microphone/recording and speech-to-text
                    audio_recorder(duration=3, mp3_file_name=mp3_file_name, playback=True)
                    botobj.transcribe_audio(mp3_file_name)

                case 'stt':
                    # Test speech-to-text drivers
                    if "y" == input("Do you want to test 'AWS Polly' [y|n]: ").lower():
                        audio_recorder(duration=3, mp3_file_name="content/user.mp3")
                        botobj.transcribe_audio("content/user.mp3")

                    sub_folders = [os.path.basename(f.path) for f in os.scandir("models") if f.is_dir()]
                    if not sub_folders:
                        print("There are no models saved in the './models' directory")
                    else:
                        for model in sub_folders:
                            if "y" == input(f"Do you want to test '{model}' model [y|n]: ").lower():
                                text = audio_recorder_stt(model=model, print_status=False)
                                print("User:  ", text)

                case 'tts':
                    # Test each text-to-speech drivers
                    print(f"The current test string is '{test_string}'")
                    choice = ""
                    while choice not in ["y", "n"]:
                        choice = input("Do you want to change it (y|n): ").strip().lower()
                        if choice == "y":
                            test_string = input("New text string: ").strip().lower()

                        for module in botobj.voices.supported_tts_modules:
                            voice = botobj.voices.get_voices(module=module)[0]
                            print(f"\nTesting TTS Module '{module}' with voiceId '{voice}'")
                            botobj.change_voice(new_voice=voice)
                            botobj.text_to_speech(test_string, voice=voice, save_mp3=botobj.mp3_filename)
                        print()

                case 'voices':
                    # Test all voices
                    print(f"The current text-to-speech string is '{test_string}'")
                    choice = ""
                    while choice not in ["y", "n"]:
                        choice = input("Do you want to change it (y|n): ").strip().lower()
                        if choice == "y":
                            test_string = input("New text-to-speech string: ").strip()

                    i = 0
                    total = len(botobj.voices.names)
                    for voice, param in botobj.voices.names.items():
                        if i and "y" != input("Do you want to continue (y|n): ").strip().lower():
                            break

                        i += 1
                        print(f"{i}/{total}: Testing module {param['module']} with {voice}...\n")
                        botobj.change_voice(new_voice=voice, change_filename=True)
                        # To Do: how to not have to send voice=voice...already set it above.
                        botobj.text_to_speech(test_string, voice=voice, save_mp3=botobj.mp3_filename)

                case _:
                    print(f"oops, '{arg1}' command can not find an option for '{arg2}'", end="\n\n")

        # TOP Menu: Debug Commands
        case '^(d .+|(d|debug )(info|voice|api-key|interview|version|logging))$':
            if not arg2: arg2 = arg1
            match RegExpNoCase(arg2):
                case 'api-key':
                    api_check_key_status()

                case 'info':
                    # Show debug information
                    print("*" * 80)
                    print("Total ChatBots Created:", botobj.created)
                    print("Total ChatBots Active:", len(botobj.objects))
                    print("*" * 80 + "\nChatBotGpt Info:\n" + "*" * 80)
                    pprint(botobj.__dict__)

                    for index, gpt in enumerate(botobj.objects):
                        print("*" * 80 + f"\nGPT Object {index}:\n" + "*" * 80)
                        pprint(gpt.__dict__)
                        # print("*" * 80)

                    print("*" * 80 + "\nVoices Info:\n" + "*" * 80)
                    pprint(Voices.__dict__)

                case 'interview':
                    # Set introduction to python interview
                    botobj.intro = f"""
                        You are interviewing the user for a python QA developer position. 
                        Ask short questions that are relevant to an advanced level developer. 
                        Keep responses under {G.MAX_WORDS} words and be funny sometimes.
                    """
                    botobj.intro = botobj.clean_chat_message(text=botobj.intro, add_limit=False)

                case 'logging':
                    print("{0:30} {1}".format("logging Level", chat_log))
                    print("{0:30} {1}".format("log file", chat_log.file_name))

                case 'version':
                    print(G.VERSION)

                case 'voice':
                    # Show detail of all voices
                    pprint(botobj.voices.names)

                case _:
                    print(f"oops, '{arg1}' command can not find an option for '{arg2}'", end="\n\n")
        case _:
            return False

    if ret_bool:
        return True
    else:
        return ready_to_chat, restart_db

# ---------------------------------------------------------------------------------------
