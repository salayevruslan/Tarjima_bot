TOKEN = '7160231101:AAG8T-VFOWIRYKlrGISPJZfvHWNP4dmXy2Q'

from gtts import gTTS

def speech(mytext, lan):
    myobj = gTTS(text=mytext, lang=lan, slow=False)
    myobj.save('audio.mp3')
     

