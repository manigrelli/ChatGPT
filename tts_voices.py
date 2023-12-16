from random import choice
from chatbot_logger import chat_log, trace, my_stack

# Module              Source            Quality    Voices       $       Subscription
# ===================================================================================================
# tts_elevenLabs.py   elevenLabs.io     Awesome    Tons         $$$     YES (free - used up quickly)
# pollyTTs.py         Amazon Web Svc    Good       Many         $       YES
# tts_pyx3.py         Python            okay       2 ?          $0
# tts_google.py       Google            ok         many Female  $0


class Voices:
    created = 0

    def __init__(self):
        trace(__name__, log=True)
        chat_log.logger.info(f"{my_stack(__name__)}: Init voice object")
        Voices.created += 1
        self.supported_tts_modules = ("tts_polly", "tts_elevenLabs", "tts_google", "tts_pyx3")

        # elevenlabs.io
        self.tts_elevenLabs = {
            "Pauly": {
                "gender": "male",
                "module": "tts_elevenLabs",
                "voice_id": "pNInz6obpgDQGcFmaJgB",
                "model_id": "eleven_monolingual_v1",
                "stability": 0,
                "similarity_boost": 0,
                "style": 0.5,
                "use_speaker_boost": True
            },
        }

        # AWS: Polly
        self.tts_polly = {
            "Brian": {
                "gender": "male",
                "module": "tts_polly",
            },
            "Giorgio": {
                "gender": "male",
                "module": "tts_polly",
            },
            "Geraint": {
                "gender": "male",
                "module": "tts_polly",
            },
            "Matthew": {
                "gender": "male",
                "module": "tts_polly",
            },
            "Salli": {
                "gender": "female",
                "module": "tts_polly",
            },
            "Amy": {
                "gender": "female",
                "module": "tts_polly",
            },
            "Raveena": {
                "gender": "female",
                "module": "tts_polly",
            },
            "Aditi": {
                "gender": "female",
                "module": "tts_polly",
            },
        }

        # Python: pyTTSx3
        self.tts_pyx3 = {
            "David": {
                "gender": "male",
                "module": "tts_pyx3",
                "ID": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0",
                "rate": 150,
                "volume": 1,
            },
            "Zira": {
                "gender": "female",
                "module": "tts_pyx3",
                "ID": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0",
                "rate": 150,
                "volume": 1,
            },
        }

        # Google: gTTS
        self.tts_google = {
            "Jane": {
                "gender": "female",
                "module": "tts_google",
                "lang": "en",
                "tld": "us",
                "slow": False,
            },
            "LadyEspanol": {
                "gender": "female",
                "module": "tts_google",
                "lang": "es",
                "tld": "us",
                "slow": False,
            },
            "LadyCanuk": {
                "gender": "female",
                "module": "tts_google",
                "lang": "en",
                "tld": "ca",
                "slow": False,
            },
            "LoosyLush": {
                "gender": "female",
                "module": "gTTS",
                "lang": "en",
                "tld": "ie",
                "slow": False,
            },
            "BritLassi": {
                "gender": "female",
                "module": "tts_google",
                "lang": "en",
                "tld": "co.uk",
                "slow": False,
            },
            "AussiMate": {
                "gender": "female",
                "module": "tts_google",
                "lang": "en",
                "tld": "com.au",
                "slow": False,
            },
            "IndyGirl": {
                "gender": "female",
                "module": "tts_google",
                "lang": "en",
                "tld": "co.in",
                "slow": False,
            },
        }

        # NOTE:  Make sure ALL keys (voice names) are unique
        self.names = dict(self.tts_polly, **self.tts_pyx3, **self.tts_elevenLabs, **self.tts_google)
        self.list_of_names = [name for name in self.names.keys() ]

    # ---------------------------------------------------------------------------------------

    def get_module_name(self, voice):
        """"""
        trace(log=True)

        if voice in self.names:
            return self.names[voice]["module"]
        raise Exception(f"{__name__} VoiceError: Voice for '{voice}' does not exist")

    # ---------------------------------------------------------------------------------------

    def get_voices(self, module, gender=None):
        """"""
        trace(log=True)

        module_dict = getattr(self, module)
        if gender is None:
            return [voice[0] for voice in module_dict.items()]
        else:
            return [voice[0] for voice in module_dict.items() if voice[1]["gender"] == gender]

    # ---------------------------------------------------------------------------------------

    def get_voice_detail(self, module, voice):
        """"""
        trace(log=True)

        try:
            module_dict = getattr(self, module)
            return module_dict[voice]
        except Exception:
            raise Exception(f"{__name__}: No detail found for '{voice}' in module '{module}'")

    # ---------------------------------------------------------------------------------------

    def choose_voice(self, tts_module, voice):
        """"""
        trace(log=True)

        # Note: 'voice' is case-sensitive
        default_voice = self.get_voices(tts_module)[0]
        if voice is None:
            voice = default_voice
        elif voice.lower() == "male":
            voice = choice(self.get_voices(tts_module, gender="male"))
        elif voice.lower() == "female":
            voice = choice(self.get_voices(tts_module, gender="female"))
        else:
            if voice not in self.get_voices(tts_module):
                e = f"Unknown VoiceId '{voice}' in tts module '{tts_module}'. Defaulting to '{default_voice}'"
                chat_log.logger.error(f"{trace()}: {e}")
                voice = default_voice

        return voice

# ---------------------------------------------------------------------------------------


if __name__ == "__main__":
    voice = Voices()
    print("Male Voices in pollyTTS:", voice.get_voices("tts_polly", "male"))
    try:
        print("Brian's python module:", voice.get_module_name("Brian"))
        print("Bart's python module:", voice.get_module_name("Bart"))
    except Exception as e:
        print("Error:", e)


