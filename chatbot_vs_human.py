from random import choice as random_choice

from common import *
from menus_shared import help_chat_menu, ans_matched_common
from player_recorder import audio_recorder
from chatbotgpt import ChatBotGpt
# from chat_logger import chat_log


# ##################################################################################################
#
#     a88888b. dP                  dP                 oo   dP   dP           888888ba             dP
#   d8'   `88 88                  88                      88   88           88    `8b            88
#   88        88d888b. .d8888b. d8888P    dP  dP  dP dP d8888P 88d888b.    a88aaaa8P' .d8888b. d8888P
#   88        88'  `88 88'  `88   88      88  88  88 88   88   88'  `88     88   `8b. 88'  `88   88
#   Y8.   .88 88    88 88.  .88   88      88.88b.88' 88   88   88    88     88    .88 88.  .88   88
#    Y88888P' dP    dP `88888P8   dP      8888P Y8P  dP   dP   dP    dP     88888888P `88888P'   dP
#
# ###################################################################################################


# ---------------------------------------------------------------------------------------


def chat_with_bot(chatbot=None):
    """"""
    trace(log=True)

    # 1. Record audio and have it transcribed.
    # 2. Send transcribed audio to chatgpt, get a text response, and play the audio.
    # 3. Save the chat history to send back and forth for context.

    # originally, this was designed to save the log of the entire chat.  That can be useful.
    # But, most chats my family and i do here are just kicking around and having fun.  Rarely
    # do we care or need a long history or are aware ... (tokens =$$$). So for now, each chat
    # is BRAND NEW. KISS - i'm not gonna get fancy with options.  As the chat continues only
    # carry the last carry_over (configurable) roles.  Keep in mind.. The user can clear
    # (aka) start over or change the intro at any time.
    start_new_chat = True

    fun_intros = [
        "play a new game",
        "play i spy with my little eye"
        "make a ryhme",
        "explain something interesting like i am 5",
        "explain how play dough is useful. i am a rocket scientist",
        "tell new jokes for all ages",
        "meaning of life",
        "be really funny",
        "classic rock music trivia",
        "chat with puns and cats",
        "chat with sarcasm",
        "geography quiz",
        "country quiz",
        "funniest jokes for kids",
        "math quiz for junior high",
        "you are a doctor",
        "you are an alien invading earth",
        "tell jim gaffigan jokes",
        "sports trivia",
        "periodic table trivia",
    ]

    count = 0
    default_greeting = "ok?"
    user_message = default_greeting
    free_voice = "David"
    restart_db = start_new_chat
    mp3_file_name = "content/user.mp3"

    if chatbot is None:
        chatbot = ChatBotGpt(name="Greg", voice=free_voice, restart_db=True)

    choice = ""  # starts right into a chat.  if you set intro earlier, it will use that or create a random one.
    if chatbot.intro is None:
        choice = None  # drops the user right into the prompt

    while True:
        # Chat away...

        if restart_db:
            count = 0
            if os.path.exists(chatbot.db_filename):
                os.remove(chatbot.db_filename)
            restart_db = False

        count += 1
        seconds = 5
        ready_to_chat = False

        if choice is not None:
            if chatbot.intro is None:
                chatbot.intro = chatbot.clean_chat_message(random_choice(fun_intros), add_limit=True)

            gpt_response = chatbot.get_chat_response(user_message, gpt_name=f"ChatBot #{count}")
            chatbot.text_to_speech(gpt_response, voice=chatbot.voice)
            print()

        while not ready_to_chat:
            choice = ""
            while choice == "":
                choice = input(f"[{G.PROMPT_COUNTER}] Home(Chat)> ")
            else:
                G.PROMPT_COUNTER += 1

            args = parse_user_answer(choice)
            choice, argv, arg1, arg2 = args

            match RegExpNoCase(argv):
                # Number of seconds to record yourself
                case '^[3-9]|10$':
                    seconds = argv
                    ready_to_chat = True

                # Clear database - keep same intro
                case '^(cl|cle[ar]*)$':
                    seconds = 0
                    restart_db = True
                    ready_to_chat = True
                    user_message = default_greeting

                # Start a random preset chat
                case '^(st|st[art]*)$':
                    seconds = 0
                    restart_db = True
                    ready_to_chat = True
                    user_message = default_greeting
                    intro = arg2
                    if intro == "":
                        intro = random_choice(fun_intros)
                    chatbot.intro = chatbot.clean_chat_message(intro, add_limit=True)

                case '^(\\?|h|help|)$':
                    print(help_chat_menu)
                case '^(q|quit)$':
                    return 0
                case '^exit$':
                    return 1
                case _:
                    match = ans_matched_common(args=args, botobj=chatbot, ret_bool=False)
                    if type(match) is tuple:
                        ready_to_chat, restart_db = match
                    else:
                        # Send the <text> instead of recording your voice
                        seconds = 0
                        user_message = argv
                        ready_to_chat = True
            continue

        if seconds:
            audio_recorder(duration=seconds, mp3_file_name=mp3_file_name)
            user_message = ChatBotGpt.transcribe_audio(mp3_file_name)

# ---------------------------------------------------------------------------------------


if __name__ == "__main__":
    parse_dotini(file=G.DOT_INI)
    api_check_key_status(show=False)

    print('G.OPENAI_API', G.OPENAI_API )  # this is from env var: OPEN_AI_KEY
    print('G.OPENAI_ORG', G.OPENAI_ORG)   # this is from env var: OPEN_AI_ORG
    chat_with_bot()
