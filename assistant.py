import wolframalpha
import PySimpleGUI as sg
import speech_recognition as sr
import wikipedia as wk
import playsound
import os
import random
from gtts import gTTS
from time import ctime
import webbrowser


# wolfram API ID key
app_id = '' # put wolfram api key here to get wolfram results

client = wolframalpha.Client(app_id)

# Define the window's contents
layout = [   [sg.Text('Speak a question'),sg.Button('Speak')],
             [sg.Text('Or Enter your question here'), sg.Input(key='in1')],
             [sg.Button('Ok'), sg.Button('Cancel')] ]

# # Create the window
window = sg.Window('jarvis', layout)      # Part 3 - Window Defintion


def audio_recorder(ask = False):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if ask:
            jarvis_speak(ask)

        print('ask a question')
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(text)
        except sr.UnknownValueError:
            jarvis_speak('Sorry, I did not get that')
            gui()
        except sr.RequestError:
            jarvis_speak('Sorry, my speech service is down')

        try:
            return text
        except:
            print('try again')

def gui():

    # main loop event for gui
    while True:
        # Display and interact with the Window
        # returns dictionary
        event, values = window.read()  # Part 4 - Event loop or Window.read call


        if event == 'Cancel' or event == sg.WIN_CLOSED:
            print(event)
            break
        elif event == 'Speak':

            text = audio_recorder()

            if 'Wolfram' in text:
                jarvis_speak('what is your question?')
                text1 = audio_recorder()
                wolfwik(text1)
            if 'what is your name' in text:
                jarvis_speak('Jarvis')
            if 'what time is it' in text:
                jarvis_speak(ctime())
            if 'search' in text:
                search = audio_recorder('What do you want to search for?')
                url = 'https://google.com/search?q=' + search
                webbrowser.get().open(url)
                jarvis_speak('here is what i found for ' + search)

            if 'find location' in text:
                location = audio_recorder('What is the location?')
                url = 'https://google.nl/maps/place/' + location
                webbrowser.get().open(url)
                jarvis_speak('Here is the location of' + location)
            if 'exit' in text:
                exit()


        # read window input if user didnt press speak
        elif event == 'Ok':
            print(event,values)
            # get results of user search
            resul = values['in1']

            if resul:
                print(resul)
                wolfwik(resul)

            else:
                gui()


    # # Finish up by removing from the screen

    window.close()



def jarvis_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en-ca')
    r = random.randint(1, 1000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)

def wolfwik(value):
    print(value)

    # the results of the queried question

    res = client.query(value)

    # check if wolfram can answer the question if no try wikipedia
    try:
        wiki_res = wk.summary(value, sentences=1)
        wolfram_res = next(res.results).text
        sg.PopupNonBlocking(f'Wikipedia Results: {wiki_res}',
                            f'\n',
                            f'Wolfram Results: {wolfram_res}')
        jarvis_speak(wiki_res)
        jarvis_speak(wolfram_res)

    except wk.exceptions.DisambiguationError:
        wolfram_res = next(res.results).text
        sg.PopupNonBlocking(f'Wolfram Results: {wolfram_res}')
        jarvis_speak(wolfram_res)



    except wk.exceptions.PageError:
        wolfram_res = next(res.results).text
        sg.PopupNonBlocking(f'Wolfram Results: {wolfram_res}')
        jarvis_speak(wolfram_res)



    except:
         wiki_res = wk.summary(value, sentences=1)
         sg.PopupNonBlocking(f'Wikipedia Results: {wiki_res}')
         jarvis_speak(wiki_res)





if __name__ == '__main__':
    gui()

