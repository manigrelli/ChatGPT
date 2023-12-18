<h1 align="center">Chat GPT</h1>
<p align="center">Desktop Application</p>

<p align="center">Powered by</p>


<p align="center">
  <img width="50" src="./public/open-ai.png" alt="ChatGPT">
  <img width="80" src="./public/python.png" alt="Python">
  <img width="40" src="./public/aws-polly.jpg" alt="AwsPolly">
  <img width="80" height="45" src="./public/alphacephei.png" alt="alphacephei">
  <img width="100" height="45" src="./public/lame.png" alt="lame">
  <img width="60" src="./public/aws.png" alt="aws">
  <img width="80" height="45" src="./public/mpg123.png" alt="mpg123">
</p>

---

This is an unofficial project solely intended for personal learning and research. It was inspired by this
[YouTube video](https://youtu.be/4y1a4syMJHM) by Travis Rogers. Watch his demo -very cool. The solution you create
with him comes up short with respect to recording your voice and making it usable. So that's what sparked my
enthusiasm.  Many thanks to Travis!

---

## Overview:
At its core, this application uses [Open-AI ChatGPT](https://openai.com/chatgpt) service to provide an interactive
user experience. The text from ChatGPT is converted to audio using one of four Text-To-Speech (TTS) methods
described below. The audio is then played out the speaker using [mpg123](https://www.mpg123.de/) application. Next, you 
respond by either typing in text or start an audio recording with your microphone. Your audio is converted to text using
one of two Speech-to-Text (STT) methods described below. Now, with your response in text format, the interaction
with ChatGpt repeats. All of these services are either free or very inexpensive.  It is fun to play with and 
remarkably my son found a great use case:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
"Quiz me on the parts of a plant cell"

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
"Tell me an easy way to remember what the chloroplast does"

---

When launched, the application begins with a familiar operating system like prompt or 
[CLI](https://en.wikipedia.org/wiki/Command-line_interface).  From there you experience an intuitive menu
to navigate several options:

1. __Interactive Chat with ChatGPT Bot:__  This allows you to either type in text (free) or record your voice (free)
and automatically convert it to text (free and not free). To save on token usage with ChatGBT (not free) you can
limit the history of the HTTP request message sent to Open-AI. See the example below.
 
2. __Bot vs. Bot:__  You are prompted to optionally re-define the role of two ChatBots. By default one is a male and the 
other is female. You set up their 'roles' and they 'talk' to each other, literally!  It is humorous at times. At the
end of the day you will realize the Open-AI model is programmed to be extremely sympathetic.  See the example below.

3. __Change, Show, and Test the APIs:__  What's a CLI with out dorky ways to set, show and execute quick unit tests.
This was useful in testing...

---

### Text-to-Speech (TTS) drivers:
Four TTS drivers are supported totalling 18 different voices. Dig into the code and you can add more. The one that 
Travis uses in his demo is [ElevenLabs.io](https://elevenlabs.io/).  I gotta be honest - It is awesome!!!
Only problem is the free version includes only ~10k characters per month.  That won't last long. While exploring 
Speech-To-Text from AWS, I picked up their [Polly](https://docs.aws.amazon.com/polly/latest/dg/what-is.html) TTS
service.  AWS pricing is extremely reasonable. Several hours of fun for 30 cents!  Polly's voices are pretty good and
they do have advanced models at a higher cost. Then, there's the free TTS: [Google's gTTS](https://pypi.org/project/gTTS/)
and [Python pyTTSx3](https://pypi.org/project/pyttsx3/).  You get what you pay for.  Honestly, gTTS has some great 
voices if you choose an accent other than us/eng. You will find some MP3 samples in the
[/content](https://github.com/manigrelli/ChatGPT/tree/main/content) directory.

---

### Speech-to-Text (STT) drivers:
Two STT drivers are supported.  The free version provided by [alphacephei.com](https://alphacephei.com/vosk/models) 
requires you to download a 40Mb model.  For more specific details on how to configure it, go
[here](https://github.com/manigrelli/ChatGPT/blob/main/models/Models.md). It is very simple to do. This method
streams the recording right to the vosk api. There's no file system read/writes.

Alternatively [Amazon Whisperer](https://aws.amazon.com/codewhisperer/resources/#Getting_started/) also does a 
great job.  This service is not free but is very inexpensive.  The microphone records the WAV file and that
is converted to MP3 format using [LAME](https://lame.sourceforge.io/). Then the MP3 is translated to text using the
[Amazon Whisperer](https://aws.amazon.com/codewhisperer/resources/#Getting_started/) service.

---

Also included (if you trust me) is a stand-alone executable,
[bin/chatbot_v1.exe](https://github.com/manigrelli/ChatGPT/tree/main/bin).  It was created with pyInstaller
on Windows 11 Home Edition using 64bit.  I tried to launch the exe on a 32 bit Windows 7 and it complained.
Win XP - forget it!  It worked fine on both my wife's and son's comparable Windows OS.

---

### Here is a brief example (sans the audio):

```
D:\> python main.py -h
usage: main.py [-h] [-i <file>] [-l <level>] [-o <file>] [-v]

options:
  -h, --help  show this help message and exit
  -i <file>   dot-ini file path
  -l <level>  logging level
  -o <file>   log-file file path
  -v          show version and exit

D:\>
```

<br>

```
D:\> python main.py -i config.ini

   ___ ___ _____        ___ _         _     ___      _
  / __| _ \_   _|      / __| |_  __ _| |_  | _ ) ___| |_
 | (_ |  _/ | |       | (__| ' \/ _` |  _| | _ \/ _ \  _|
  \___|_|   |_|        \___|_||_\__,_|\__| |___/\___/\__|


Welcome to GPT ChatBot!  Enter 'help' to get started.

[1] Home> help

<text>           : Play <text> out speaker using TTS
chat     | c     : Start a fresh chat session
listen   | l     : Listen to 'Bot vs Bot'
set      | s     : Show 'set' commands
show     | sh    : Show 'show' commands
help     | h     : For this help message
quit     | q     : To return to Top Menu
exit             : To exit application

[2] Home> chat
[3] Home(Chat)>         
[3] Home(Chat)>
[3] Home(Chat)>
[3] Home(Chat)> help

[3..10]          : Number of seconds to record yourself
<text>           : Type a message in lieu of recording yourself
clear    | cl    : Clear chat session (same intro)
start    | st    : Start a random preset chat
set      | s     : Show 'set' commands
show     | sh    : Show 'show' commands
help     | h     : For this help message
quit     | q     : To return to Top Menu
exit             : To exit application

[4] Home(Chat)> tell me a short joke

ChatBot #2:
Why don't scientists trust atoms? Because they make up everything!

[5] Home(Chat)> 4
** Start Recording...4 seconds
** Stop!

User:  What is 1 plus 1?


ChatBot #3:
The sum of 1 plus 1 is 2.

[6] Home(Chat)>
[6] Home(Chat)> quit
[7] Home> listen

----------------------------------------------------------------------------------------------------
Male Role:
Rainy days are great. Jane's opinions are wacky. Add humor.

Female Role:
You disagree with David's view on weather. Add humor.
----------------------------------------------------------------------------------------------------

Do you want to change the roles (y|n|q): n
Do you want to change voices (y|n|q): n

David:
Rainy days are great because they give me an excuse to stay in my pajamas, drink hot chocolate, and
avoid responsibilities. Plus, Jane's wacky opinions are like a comedy show—I never know what she'll
say next!

Jane:
Oh, come on! Rainy days are perfect for pretending to be a fancy British detective, dramatically
looking out the window and saying, "The game is afoot!" David clearly needs to up his entertainment
game.

Do you want to continue (y|n): y

David:
Jane, please. Rainy days are just the universe's way of giving us an excuse to stay in bed, wrapped
in blankets, and binge-watching our favorite shows. It's a scientific fact.

Jane:
Oh David, you clearly haven't experienced the joy of stepping in a puddle and unintentionally
reenacting a scene from Singin' in the Rain. It's like being the star of your own quirky musical!

Do you want to continue (y|n): n
Thanks for listening!  Goodbye...

[8] Home>
```

<br>

### Before getting started you need to obtain API keys and put them in 'config.ini':

##### 1. [MUST]: [Open-AI ChatGpt](https://platform.openai.com/api-keys):
  - OPEN_AI_ORG
  - OPEN_AI_KEY

##### 2. [Recommended] Speech-to-Text: [AWS Whisper ](https://docs.aws.amazon.com/toolkit-for-visual-studio/latest/user-guide/builder-id.html)
  - AWS_ACCESS_KEY_ID
  - AWS_SECRET_ACCESS_KEY
  - AWS_DEFAULT_REGION

##### 3. [Optional] Awesome TTS from: [ElevenLabs.io](https://elevenlabs.io/sign-up)
  - ELEVENLABS_KEY


### Example config.ini:

```
[Default]

[Speech To Text]
model=AWS

[Open AI]
api_key=sk-000000000000000000000000000000000000000000000000
organization_key=org-000000000000000000000000
gpt_model=gpt-3.5-turbo

[Eleven Labs]
api_key=00000000000000000000000000000000

[Amazon Web Services]
access_key=00000000000000000000
secret_access_key=0000000000000000000000000000000000000000
default_region=us-east-1
```

### MD5 hashes:
```
$ md5sum.exe bin/*
1c6312d6e0702d8cdf0c032ab6fa1d6a *bin/chatbot_v1.exe
3c44d972d292a75bff8f9df6a50670d5 *bin/lame.exe
41991ca4d9201eb5914a617ac1423148 *bin/mpg123.exe
$ 
```




