import spacy
import en_core_web_sm
import pandas as pd
import speech_recognition as sr 
import pyttsx3
from spacy.matcher import Matcher
def get_father(x):
    nlp = en_core_web_sm.load()
    doc = nlp(x)
    matcher = Matcher(nlp.vocab) 
    matcher.add("matching_father", pattern_father)
    matches = matcher(doc)
    sub_text = ''    
    if(len(matches) > 0):
        span = doc[matches[0][1]:matches[0][2]] 
        sub_text = span.text
    tokens = sub_text.split(' ')
    
    name, surname = tokens[1:-1]
    return name, surname
def Speaking():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio_data = r.record(source, duration=5)
        try:
            text = r.recognize_google(audio_data)
            print(text)
        except:
            Speak("please repeat again")
            text=Speaking()
        return text
def Speak(toSpeak):
    engine = pyttsx3.init() 
    engine.setProperty('rate', 150)  
    # rate = engine.getProperty('rate')
    # volume = engine.getProperty('volume')   
    engine.setProperty('volume',1.0)   
    voices = engine.getProperty('voices')      
    engine.setProperty('voice', voices[1].id)   
    # engine.say("Hello World!")
    engine.say(toSpeak)
    engine.runAndWait()
    engine.stop()
# Speak('Discribe about your self')
# a=Speaking()
# nlp = spacy.load('en_core_web_sm',disable=['ner','textcat'])
# text =a
# doc = nlp(text)
# for token in doc:
#     print(token.text,'->',token.pos_)
with open('info.txt', 'r') as f:
    a = [line for line in f.readlines()]
df = pd.DataFrame(a,columns=['text'])
# print(df.head())
text = df['text'][0]
nlp = en_core_web_sm.load()
doc = nlp(text)
features = []
for token in doc:
    features.append({'token' : token.text, 'pos' : token.pos_})
fdf = pd.DataFrame(features)
# print(fdf.head(len(fdf)))
first_tokens = ['to', 'father']
last_tokens = ['and', 'naming']
pattern_father = [[{'LOWER' : {'IN' : first_tokens}},
           {'POS':'PROPN', 'OP' : '+'},
           {'LOWER': {'IN' : last_tokens}} ]]
new_columns = ['father name','surname']
for n,col in enumerate(new_columns):
    df[col] = df['text'].apply(lambda x: get_father(x)).apply(lambda x: x[n])

print(df)