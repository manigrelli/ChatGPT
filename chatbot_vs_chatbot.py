import textwrap

from common import trace
from chatbotgpt import ChatBotGpt
import globals as G
# from chat_logger import chat_log


# ##################################################################################
#
#     888888ba                                     888888ba
#    88    `8b            8P                      88    `8b            8P
#   a88aaaa8P' .d8888b. d8888P    dP   .dP       a88aaaa8P' .d8888b. d8888P
#    88   `8b. 88'  `88   88      88   d8'        88   `8b. 88'  `88   88
#    88    .88 88.  .88   88      88 .88'         88    .88 88.  .88   88
#    88888888P `88888P'   dP      8888P'   88     88888888P `88888P'   dP
#
# ##################################################################################


def bot_v_bot():
    """"""
    trace(log=True)

    male_voice = "David"
    female_voice = "Jane"
    male_role = "Rainy days are great. Jane's opinions are wacky. Add humor."
    female_role = "You disagree with David's view on weather. Add humor."

    print()
    print("-" * G.TEXT_WRAP)
    print("Male Role:\n" + "\n".join(textwrap.wrap(male_role, G.TEXT_WRAP)))
    print("\nFemale Role:\n" + "\n".join(textwrap.wrap(female_role, G.TEXT_WRAP)))
    print("-" * G.TEXT_WRAP, end="\n\n")

    choice = ""
    while choice not in ["y", "n", "q"]:
        choice = input("Do you want to change the roles (y|n|q): ").strip().lower()
        if choice == "q":
            return
        if choice == "y":
            male_role = input("Male Role: ")
            female_role = input("Female Role: ")

    choice = ""
    while choice not in ["y", "n", "q"]:
        choice = input("Do you want to change voices (y|n|q): ").strip().lower()
        if choice == "q":
            return
        if choice == "y":
            try:
                choice = int(input("[1]David [2]Brian [3]Pauly: ").strip())
                male_voice = ["David", "Brian", "Pauly"][choice-1]
            except Exception:
                print(f"hmmm...expected 1, 2, or 3.  Using default, '{male_voice}.")

            try:
                choice = int(input("[1]Jane  [2]Amy [3]Aditi: ").strip())
                female_voice = ["Jane", "Amy", "Aditi"][choice-1]
            except Exception:
                print(f"hmmm...expected 1, 2, or 3.  Using default, '{female_voice}.")
            break

    chatbot_man = ChatBotGpt(
        name="Husband",
        intro=ChatBotGpt.clean_chat_message(male_role),
        voice=male_voice,
        restart_db=True)

    chatbot_woman = ChatBotGpt(
        name="Wife",
        intro=ChatBotGpt.clean_chat_message(female_role),
        voice=female_voice,
        restart_db=True)

    woman_response = "Tell me why"

    keep_playing = True
    while keep_playing:
        man_response = chatbot_man.get_chat_response(woman_response, gpt_name=male_voice)
        chatbot_man.text_to_speech(man_response, voice=chatbot_man.voice)

        woman_response = chatbot_woman.get_chat_response(man_response, gpt_name=female_voice)
        chatbot_woman.text_to_speech(woman_response, voice=chatbot_woman.voice)
        print()

        choice = ""
        while len(choice) != 1:
            choice = input("Do you want to continue (y|n): ").strip()
        if choice != "y":
            break

    print("Thanks for listening!  Goodbye...")
    return


# ---------------------------------------------------------------------------------------


if __name__ == "__main__":
    from common import parse_dotini, api_check_key_status
    parse_dotini(file=G.DOT_INI)
    api_check_key_status(show=False)
    bot_v_bot()
