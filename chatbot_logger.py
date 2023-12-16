import os, logging, inspect

# ---------------------------------------------------------------------------------------


class Logger:
    def __init__(self, level="DEBUG"):
        self.file_name = "./Log/chatbot_log.txt"
        dir_name = os.path.dirname(self.file_name)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        # self.format = '%(asctime)s [%(levelname)s] %(name)s.%(lineno)d: %(message)s'
        self.format = '%(asctime)s [%(levelname)s]: %(message)s'
        self.logger = logging.getLogger(self.file_name)
        self.logger.setLevel(level)

        logfile_handler = logging.FileHandler(self.file_name, mode='w')
        logfile_handler.setFormatter(fmt=logging.Formatter(self.format))
        self.logger.addHandler(logfile_handler)

        # Add logging to console
        console_handler = logging.StreamHandler()
        console_handler.setLevel("WARNING")
        console_handler.setFormatter(fmt=logging.Formatter('%(levelname)s:  %(message)s'))
        self.logger.addHandler(console_handler)

    # ---------------------------------------------------------------------------------------

    def change_filename(self, filename):
        """"""
        trace(log=True)

        try:
            self.logger.handlers[0].close()
            if os.path.exists(filename):
                os.remove(filename)
            os.rename("./Log/chatbot_log.txt", filename)
            self.logger.handlers[0].setStream(open(filename, "a"))
            self.file_name = filename
        except Exception as e:
            print(f"!! Critical error with log file, {e}")
            print("As a work-around, do not specify -o <file>    :P")

    # ---------------------------------------------------------------------------------------

    def __str__(self):
        return ["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"][int(self.logger.level/10)]


# ---------------------------------------------------------------------------------------

def my_stack(func_name=None):
    """"""
    if func_name is None:
        func_name = inspect.stack()[1][3]

    file_name = os.path.basename(inspect.stack()[2][1])
    line_no = inspect.stack()[2][2]

    if file_name == __file__:
        file_name = os.path.basename(inspect.stack()[1][1])
        line_no = inspect.stack()[1][2]

    return f"{func_name}({file_name},{line_no})"


# ---------------------------------------------------------------------------------------


def trace(func_name=None, log=False):
    """"""
    if func_name is None:
        func_name = inspect.stack()[1][3]

    file_name = None
    line_no = None
    called_by = None
    try:
        file_name = os.path.basename(inspect.stack()[1][1])
        line_no = inspect.stack()[1][2]
        called_by = inspect.stack()[2][3]
    except IndexError:
        # print(f"(pyInst right?): TODO TRACE({func_name}):")
        pass

    # func_name(file.py,33):
    # chat_log.logger.debug(f"{func_name}({file_name},{line_no}): called by {called_by}")
    if log:
        chat_log.logger.debug(f"{my_stack(func_name)}: called by {called_by}")

    return f"{func_name}({file_name},{line_no})"

# ---------------------------------------------------------------------------------------


chat_log = Logger()
