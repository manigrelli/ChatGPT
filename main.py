import os, argparse, traceback
from chatbot_logger import chat_log, trace
import globals as G
from common import api_check_key_status, parse_dotini
from menu import top_menu

# ---------------------------------------------------------------------------------------

logo = f"""
   ___ ___ _____        ___ _         _     ___      _   
  / __| _ \_   _|      / __| |_  __ _| |_  | _ ) ___| |_ 
 | (_ |  _/ | |       | (__| ' \/ _` |  _| | _ \/ _ \  _|
  \___|_|   |_|        \___|_||_\__,_|\__| |___/\___/\__|

{G.VERSION}
"""


# ---------------------------------------------------------------------------------------

def main(py_cwd=""):
    """"""
    trace(log=True)

    my_name = os.path.basename(__file__)
    G.PY_CWD = py_cwd

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        metavar="<file>",
        help='dot-ini file path',
        default=G.DOT_INI,
        dest="key_file"
    )

    parser.add_argument(
        '-l',
        help='logging level',
        choices=["DEBUG", "INFO", "WARNING", "CRITICAL"],
        metavar="<level>",
        default="INFO",
        dest="log_level"
    )

    parser.add_argument(
        '-o',
        metavar="<file>",
        help='log-file file path',
        dest="log_file"
    )

    parser.add_argument(
        '-v',
        help='show version and exit',
        default=False,
        action="store_true",
        dest="return_version"
    )

    args = parser.parse_args()
    if args.return_version:
        print(G.VERSION)
        return

    args = parser.parse_args()
    if args.key_file:
        chat_log.logger.info(f"{my_name}: CLI changing key file to '{args.key_file}'")
        G.DOT_INI = args.key_file

    if args.log_file:
        chat_log.logger.info(f"{my_name}: CLI changing log file to '{args.log_file}'")
        chat_log.change_filename(args.log_file)

    log_level = "INFO"
    if args.log_level:
        chat_log.logger.info(f"{my_name}: CLI changing log level to '{args.log_level}'")
        log_level = args.log_level
    chat_log.logger.setLevel(log_level)

    # Check API Keys are loaded.  Not all are needed. You just won't have that service
    parse_dotini(file=G.DOT_INI)
    api_check_key_status(show=(log_level == "DEBUG"))

    # # Check and make sure binaries are present:
    G.MP3_PLAYER = os.path.join(py_cwd, G.MP3_PLAYER)
    G.WAV_TO_MP3 = os.path.join(py_cwd, G.WAV_TO_MP3)

    for file_name in [G.MP3_PLAYER, G.WAV_TO_MP3]:
        if not os.path.exists(file_name):
            chat_log.logger.critical(f"{my_name}: Detected {file_name} does not exist...")

    # Check and make sure binaries are present:
    for file_name in [G.MP3_PLAYER, G.WAV_TO_MP3]:
        if not os.path.exists(file_name):
            chat_log.logger.critical(f"{my_name}: Detected {file_name} does not exist...")

    try:
        print(logo)
        print("Welcome to GPT ChatBot!  Enter 'help' to get started.\n")
        parse_dotini(file=G.DOT_INI)
        api_check_key_status(show=False)
        top_menu()
    except Exception as e:
        chat_log.logger.critical(f"{my_name}: {e}")
        details = traceback.format_tb(e.__traceback__)
        chat_log.logger.critical(f"{my_name}: {details}")
        print(f"Exception occurred.  See log file for details.")

# ---------------------------------------------------------------------------------------


if __name__ == '__main__':
    main()
