# Колун Дэнилэ Васильевич, 373732 (Вар. 2) (Доп. задание)
import pyttsx3, pyaudio, vosk
import requests, json

tts = pyttsx3.init('sapi5')

voices = tts.getProperty('voices')
tts.setProperty('voices', 'en')

for voice in voices:
    print(voice.name)
    if voice.name == 'Microsoft Zira Desktop - English (United States)':
        tts.setProperty('voice', voice.id)

model = vosk.Model('vosk-model-small-en-us-0.15')
record = vosk.KaldiRecognizer(model, 16000)
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=16000,
                 input=True,
                 frames_per_buffer=8000)
stream.start_stream()


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if record.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(record.Result())
            if answer['text']:
                yield answer['text']


def speak(say):
    tts.say(say)
    tts.runAndWait()


def word_save(word):  # saving the word
    rp = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
    data = rp.json()
    with open("Dictionary.txt", "w") as f:
        json.dump(data, f)
    print("The data was saved to file Dictionary.txt")
    speak("The data was saved to file Dictionary.txt")


def definition(word):  # finding the definition of a word
    try:
        rp = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
        data = rp.json()
        print(data[0]['meanings'][0]['definitions'][0]['definition'])
        speak(data[0]['meanings'][0]['definitions'][0]['definition'])
    except Exception:
        print('The definition of the word was not found')
        speak('The definition of the word was not found')


def example(word):  # finding the example of the word
    try:
        rp = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
        data = rp.json()
        print(data[0]['meanings'][0]['definitions'][0]['example'])
        speak(data[0]['meanings'][0]['definitions'][0]['example'])
    except Exception:
        print('The example was not found')
        speak('The example was not found')


def source(word):  # finding the source of the word
    try:
        rp = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
        data = rp.json()
        speak('The source is shown in the console')
        print(data[0]['sourceUrls'][0])
    except Exception:
        print('The URL was not found')
        speak('The URL was not found')


if __name__ == '__main__':
    print('Please say "Find.." and then continue with a word to find it in the dictionary')
    speak('Please say "Find.." and then continue with a word to find it in the dictionary')
    for text in listen():
        if 'find' in text:
            term = text.split("find ")[1]
            try:
                rp = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{term}')
                data = rp.json()
                print(data['message'])
            except Exception as ex:
                print('The word', term, 'was found')
                speak('The word', term, 'was found')
        elif text == 'quit':
            print("Quitting..")
            speak('Quitting')
            break
        elif text == 'save':
            word_save(term)
        elif text == 'meaning':
            definition(term)
        elif text == 'example':
            example(term)
        elif text == 'source':
            source(term)
        else:
            print('The command that you said was not recognized')
            speak('The command that you said was not recognized')
