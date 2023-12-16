import traceback
from menus_shared import *
from common import *

from chatbotgpt import ChatBotGpt
from chatbot_vs_human import chat_with_bot
from chatbot_vs_chatbot import bot_v_bot
# from chat_logger import chat_log

# ##########################################################################
#    _______  _______  _______    __   __  _______  __    _  __   __
#   |       ||       ||       |  |  |_|  ||       ||  |  | ||  | |  |
#   |_     _||   _   ||    _  |  |       ||    ___||   |_| ||  | |  |
#     |   |  |  | |  ||   |_| |  |       ||   |___ |       ||  |_|  |
#     |   |  |  |_|  ||    ___|  |       ||    ___||  _    ||       |
#     |   |  |       ||   |      | ||_|| ||   |___ | | |   ||       |
#     |___|  |_______||___|      |_|   |_||_______||_|  |__||_______|
# ##########################################################################


# ---------------------------------------------------------------------------------------

def top_menu():
    """"""
    trace(log=True)

    # tons of tokens ($$$) are wasted with the accumulation of a chat.  unless you really want
    # to 'continue' an interactive chat, there's no need to waste these tokens.  so, by default
    # each conversation is 'fresh', unless the user explicitly 'set ENABLE_LIMIT False' in cli.

    free_voice = "David"
    chatbot = ChatBotGpt(name="GeeBeeTee", voice=free_voice, restart_db=True)

    while True:
        choice = ""
        while choice.strip() == "":
            choice = input(f"[{G.PROMPT_COUNTER}] Home> ")
        else:
            G.PROMPT_COUNTER += 1

        args = parse_user_answer(choice)
        choice, argv, arg1, arg2 = args

        match RegExpNoCase(argv):
            # Top Menu: Start a fresh chat session
            case '^c[hat]*$':
                try:
                    if chat_with_bot(chatbot=chatbot):
                        return
                except Exception as e:
                    chat_log.logger.critical(f"{trace()}: {e}")
                    details = traceback.format_tb(e.__traceback__)
                    chat_log.logger.critical(f"{trace}: {details}")

            # Top Menu: Listen to 'Bot vs Bot'
            case '^l[isten]*$':
                try:
                    if bot_v_bot():
                        return
                except Exception as e:
                    chat_log.logger.critical(f"{trace()}: {e}")
                    details = traceback.format_tb(e.__traceback__)
                    chat_log.logger.critical(f"{trace}: {details}")

            # Top Menu Help
            case '^(\\?|h|help|help (mor[e]*))$':
                if not arg2: arg2 = arg1
                match RegExpNoCase(arg2):
                    case '^mor':
                        print(debug_menu)
                    case _:
                        print(help_top_menu)
            case '^(q|quit)$':
                choice = input("Are up REALLY sure you want to leave (y|n): ").strip().lower()
                if choice != "n":
                    print("See you next time!  Goodbye...")
                    return 0
            case '^exit$':
                return 1
            case _:
                if ans_matched_common(args=args, botobj=chatbot):
                    continue
                else:
                    # Send string to text-to-speech driver
                    chatbot.text_to_speech(choice, voice=chatbot.voice)
        continue


if __name__ == "__main__":
    parse_dotini(file=G.DOT_INI)
    api_check_key_status(show=False)
    top_menu()