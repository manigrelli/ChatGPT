import version

# Global Variable Declarations.
VERSION = version.build_date
PY_CWD = "."

PROMPT_COUNTER = 1
TEXT_WRAP = 100
MAX_WORDS = 35
ENABLE_LIMIT = True
MAX_CHAT = 0

DOT_INI = "config.ini"
API_STATE = {"OpenAI": False, "ElevenLabs": False, "AWS": False}
OPENAI_API = None
OPENAI_ORG = None

ELEVEN_API = None

AWS_ACCESS = None
AWS_SECRET = None
AWS_REGION = None

GPT_MODEL="gpt-3.5-turbo"
STT_MODEL=None

MP3_PLAYER = "bin\\mpg123.exe"
WAV_TO_MP3 = "bin\\lame.exe"






