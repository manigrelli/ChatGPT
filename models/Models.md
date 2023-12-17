This 'models' directory is for storing Speech-to-Text recognition models.
[alphacephei.com](https://alphacephei.com/vosk/models) has lots of vosk compatible models.
I recommend downloading [vosk-model-small-en-us-0.15 zip](https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip)
 (~40Mb).  Extract the zip file into this 'models' directory like this:

```
- main.py
- config.ini
- /models
    - models.md 
    + /vosk-model-small-en-us-0.15
```

Then update the config.ini like this:
```
[Default]

[Speech To Text]
# model=AWS Polly
model=vosk-model-small-en-us-0.15
.
.
.
```

when you re-launch main.py, you can check the status:
```
D:\> python main.py -i config.ini

   ___ ___ _____        ___ _         _     ___      _
  / __| _ \_   _|      / __| |_  __ _| |_  | _ ) ___| |_
 | (_ |  _/ | |       | (__| ' \/ _` |  _| | _ \/ _ \  _|
  \___|_|   |_|        \___|_||_\__,_|\__| |___/\___/\__|


Welcome to GPT ChatBot!  Enter 'help' to get started.

[1] Home> show config

Parameter                      Value
==================================================
Introduction                   None
GPT Voice                      David
TTS Driver                     tts_pyx3
max_words                      35
text_wrap                      100
max_chat                       0
log_level                      INFO
enable_limit                   True
ini_file                       config.ini
gpt_model                      gpt-3.5-turbo
stt_model                      vosk-model-small-en-us-0.15  <<<<<<<<<<<<
OpenAI                         Configured
ElevenLabs                     Configured
AWS                            Configured

[2] Home>

```
