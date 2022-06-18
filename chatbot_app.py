# libraries
import random
import numpy as np
import pickle
import json
from flask import Flask, render_template, request, session, redirect, url_for, escape
from flask_ngrok import run_with_ngrok
import nltk
from keras.models import load_model
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# chat initialization
model = load_model("chatbot_model.h5")
intents = json.loads(open("intents.json").read())
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))

app = Flask(__name__)
app.secret_key = 'chatsecret'



@app.route("/chatbot")
def home():
    session['scenario']='chat'
    session['mode']=''

    #user=User(email='monu.k.john6598@gmail.com', name='Monu John2', occupation='front end developer')
    # db.session.add(user)
    # db.session.commit()

    return render_template("chatbot_index.html")


@app.route("/chatbot_get", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]
    #checks is a user has given a name, in order to give a personalized feedback

    if session['mode']!='':
        if session['mode']=='formreply':
            if session['field']==0:
                res = 'Name field response added. What is age?'
                session['field'] = session['field']+1
            elif session['field']==1:
                res = 'Age added. What is city?'
                session['field'] = session['field']+1
            elif session['field']==2:
                res = 'City added. What is profession?'
                session['field'] = session['field']+1
            elif session['field']==3:
                res = 'Profession added. Thanks'+str(session['field'])
                session['mode']=''
                
    else:
        if msg.startswith('my name is'):
            name = msg[11:]
            ints = predict_class(msg, model)
            res1 = getResponse(ints, intents)
            res =res1.replace("{n}",name)
        elif msg.startswith('hi my name is'):
            name = msg[14:]
            ints = predict_class(msg, model)
            res1 = getResponse(ints, intents)
            res =res1.replace("{n}",name)
        #if no name is passed execute normally
        else:
            ints = predict_class(msg, model)

            session['intent'] = ints[0]['intent']

            res = getResponse(ints, intents)

            if session['intent'] == 'add':
                session['mode']='formreply'
                session['field']=0
                form_field = 'What is the name?'
                res = res+'. '+form_field

    
    return res


# chat functionalities
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i["responses"])
            break
    return result