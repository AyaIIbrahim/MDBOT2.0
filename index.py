from flask import Flask, render_template, url_for, flash, redirect, request, session, escape, jsonify
from forms import RegistrationForm, LoginForm
import pandas as pd
import sqlite3
import os
import Question_Maker
import teeth_predict
from werkzeug.utils import secure_filename
import run
import addDisease
import random
import numpy as np
import pickle
import json
from flask_ngrok import run_with_ngrok
import nltk
from keras.models import load_model
from nltk.stem import WordNetLemmatizer

# nomalize
from normalizer import normalize

#log
import logging

app = Flask(__name__)

# Some Definitions
app.config['SECRET_KEY'] = '4f9a5c9c0b0e66722f11b04bbfb4949f'
app.config["UPLOAD_FOLDER"] = os.getcwd() + "/static/images/user_upload"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'webp', 'tiff', 'tif', 'bmp']) 

# Routes

@app.route('/')
@app.route('/home')
def home():
    return render_template('front_index.html')


@app.route('/medicalDomain', methods=['POST','GET'])
def chooseMedicalDom():
    return render_template('medicalDomain.html')


@app.route('/info')
def info():
    return render_template('info.html')


def allowed_file(filename): 
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 


@app.route('/dent', methods=['POST','GET'])
def dent():        
    if request.method == 'POST': 
            file=request.files['file']
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename) 
                
                if filename in os.listdir(app.config['UPLOAD_FOLDER']):
                    pred1 = teeth_predict.predict(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    pred2= teeth_predict.model2(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    path = pred2.save()
                    limit = len(pred2.pandas().xyxy[0].to_json())
                    return render_template('dent.html', pred1=pred1, limit=limit, path=os.path.join(path, filename))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
                pred1 = teeth_predict.predict(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                pred2 = teeth_predict.model2(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                path = pred2.save()
                limit = len(pred2.pandas().xyxy[0].to_json())
                return render_template('dent.html', pred1=pred1, limit=limit, path=os.path.join(path, filename))
        
    return render_template('dent.html')


@app.route('/booking', methods=['POST', 'GET'])
def appointment():

    con = sqlite3.connect("mydatabase.db")
    cur = con.cursor()
    spec = matched_specialist[0]
    query_string = """SELECT firstName,lastName FROM user WHERE specialization=?"""
    cur.execute(query_string, (spec,))
    doctors = cur.fetchall()
    con.close()
    if len(doctors) >= 0:
        return render_template('booking.html',doctors=doctors, specialist=matched_specialist)
    else:
        flash(f'Sorry no available doctor right now!','danger')        
    return render_template('booking.html')

    #log   
    app.logger.info('Info level log')
    app.logger.warning('Warning level log')  
 
     
@app.route('/my_appointments')
def appointments():
    return render_template('my_appointments.html')


@app.route('/symps', methods=['POST','GET'])
def symptoms():
    con = sqlite3.connect("mydatabase.db")
    cur = con.cursor()
    cur.execute("SELECT DISTINCT symptom FROM symptoms")
    symptom = cur.fetchall()    

    if request.method == 'POST':
        session['visitor'] = 'visitor'
        session['sex'] = request.form.get('gender','udefined')
        if session['sex'] == "udefined":
            flash(f'Please select your gender!','danger')
            return redirect(url_for('home'))
        session['age'] = request.form['age']
        return render_template('symps.html', symptom = symptom)
    if request.method == 'GET' and 'email' in session:
        return render_template('symps.html', symptom = symptom)
    else:
        return redirect(url_for('info'))


Q1=Q2=[]
@app.route('/questions', methods=['POST','GET'])
def questions():
    if request.method == 'GET':
        return redirect(url_for('info'))
    symptoms = request.form.getlist('sym[]')
    if len(symptoms) <= 1:
        flash(f'Please select atleast 2 symptoms!','danger')
        return redirect(url_for('home'))
    myQuestions1,myQuestions2 = Question_Maker.fillter(symptoms)
    if len(myQuestions2) > 0:
        global Q1
        Q1=myQuestions1
        global Q2
        Q2=myQuestions2
        return render_template('choose-one.html',symptoms=symptoms,myQuestions1=myQuestions1,
                                                    myQuestions2=myQuestions2)
    else:
        return render_template('questions.html',symptoms=symptoms,myQuestions=myQuestions1)
    


@app.route('/choose', methods=['POST','GET'])
def chooseOne():
    if request.method == 'GET':
        return redirect(url_for('info'))
    symptoms = request.form.getlist('sym[]')
    choosen = request.form['ans']
    if choosen[0] == '1':
        symptoms.pop(1)
        choosen = choosen.replace('1','')
        symptoms.append(choosen)
    else:
        symptoms.pop(0)
        choosen = choosen.replace('2','')
        symptoms.append(choosen)
    
    myQuestions1,myQuestions2 = Question_Maker.fillter(symptoms)
    if len(myQuestions2) > 0:
        global Q1
        Q1=myQuestions1
        global Q2
        Q2=myQuestions2
        return render_template('choose-one.html',symptoms=symptoms,myQuestions1=myQuestions1,
                                                    myQuestions2=myQuestions2)
    else:
        return render_template('questions.html',symptoms=symptoms,myQuestions=myQuestions1)

matched_specialist = []


@app.route('/diagnosis/<count>', methods=['POST','GET'])
def diagnosis(count):
    matched_specialist.clear()
    if request.method == 'GET':
        return redirect(url_for('info'))
    goodAnswer = []
    badAnswer = []
    ans = []
    for i in range(int(count)):
        ans = ans + request.form.getlist('ans['+str(i)+']')

    for x in range(len(ans)):
        if ans[x][-1] == '3' or ans[x][-1] == '2':
            badAnswer.append(ans[x])
        else:
            goodAnswer.append(ans[x])
    
    symptoms = request.form.getlist('sym[]')
    symptoms = list(set(symptoms+goodAnswer))
    diseases = run.run(symptoms)
    
    percent=[]
    diseasesSyms = []
    for i in range(len(diseases)):
        disSymps = getAllSyms(diseases[i])
        percent.append(getPercent(symptoms,disSymps))
        diseasesSyms.append(disSymps)


    for i in range(len(diseases)-1):
        for j in range(len(diseases)-i-1):
            if percent[j] < percent[j+1]:
                percent[j],percent[j+1] = percent[j+1],percent[j]
                diseases[j],diseases[j+1] = diseases[j+1],diseases[j]
                diseasesSyms[j],diseasesSyms[j+1] = diseasesSyms[j+1],diseasesSyms[j]
    
    if len(diseases) > 0:
        counter = 0
        finalDiseases = []
        finalPercent = []
        diseasesInfo = []
        finalDisSyms = []
        diseasesTips = []
        specialist = []
        for i in range(len(diseases)):
            if percent[i] == 0:
                continue
            finalDiseases.append(diseases[i])
            finalPercent.append(percent[i])
            finalDisSyms.append(diseasesSyms[i])
            diseasesInfo.append(getDiseaseData(diseases[i]))
            specialist.append(getSpecialist(diseasesInfo[i][4]))
            if getSpecialist(diseasesInfo[i][4]) not in matched_specialist:
                matched_specialist.append(getSpecialist(diseasesInfo[i][4]))
            diseasesTips.append(getTips(diseases[i]))
            counter = counter + percent[i]
            if counter > 75.0:
                break
        
        return render_template('diagnosis.html',diseases=finalDiseases,percent=finalPercent,
                symptoms=symptoms,diseasesInfo=diseasesInfo,diseasesSyms=finalDisSyms,diseasesTips=diseasesTips,specialist=specialist)
    else:
        flash(f'Sorry your symptoms dosn\'t match any disease, try again!','danger')
        return redirect(url_for('home'))


@app.route('/map', methods=['POST','GET'])
def goolge_map():
    address = address_value = "Cairo"
    if request.method == 'POST':
        address = address_value = request.form['map-address']
        address = address.replace(' ','+')
    return render_template('google-map.html',address=address,address_value=address_value)


@app.route('/feedback',methods=['POST'])
def feedback():
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        msg = request.form['feedback']
        usermail = session['email']
        rate = request.form['rate']
        con = sqlite3.connect("mydatabase.db")
        cur = con.cursor()
        query_string = """INSERT INTO feedback (usermail,message,rate) VALUES (?,?,?)"""
        cur.execute(query_string, (usermail,msg,rate))
        con.commit()
        cur.close()
        flash(f'Feedback sent','success')
        return redirect(url_for('home'))

def getDiseaseData(disease):
    con = sqlite3.connect("mydatabase.db")
    cur = con.cursor()
    query_string = """SELECT * FROM diseases WHERE disease=?"""
    cur.execute(query_string, (disease,))
    diseases = cur.fetchall()
    cur.close()
    if len(diseases) > 0:
        return diseases[0]
    return []


def getAllSyms(disease):
    con = sqlite3.connect("mydatabase.db")
    cur = con.cursor()
    query_string = """SELECT symptom FROM symptoms WHERE disease=?"""
    cur.execute(query_string, (disease,))
    symptoms = cur.fetchall()
    cur.close()
    result = []
    if len(symptoms) > 0:
        for s in symptoms:
            result.append(s[0])
        return result
    return []


def getTips(disease):
    con = sqlite3.connect("mydatabase.db")
    cur = con.cursor()
    query_string = """SELECT tips FROM tips WHERE disease=?"""
    cur.execute(query_string, (disease,))
    tips = cur.fetchall()
    cur.close()
    if len(tips) > 0:
        return tips[0][0]
    return []

def getPercent(mySymptoms,diseaseSymptoms):
    counter = 0
    for ms in mySymptoms:
        for ds in diseaseSymptoms:
            if ms == ds:
                counter +=1
    if len(diseaseSymptoms) == 0:
        return 0
    else :
        return int((counter * 100) / len(diseaseSymptoms))


def getSpecialist(organ):
    con = sqlite3.connect("mydatabase.db")
    cur = con.cursor()
    query_string = """SELECT specialist FROM specialist WHERE organ=?"""
    cur.execute(query_string, (organ,))
    specialist = cur.fetchall()
    cur.close()
    if len(specialist) > 0:
        return specialist[0][0]
    return ""

@app.route('/reg', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if request.method == 'GET' and 'email' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        if form.validate_on_submit():
            con = sqlite3.connect("mydatabase.db")
            cur = con.cursor()
            query_string = """SELECT * FROM user WHERE email=?"""
            cur.execute(query_string, (form.email.data,))
            users = cur.fetchall()
            if len(users) > 0:
                flash(f'Email used before!','danger')
                return render_template('reg.html', form=form)
            query_string = """INSERT INTO user (firstName,lastName,email,sex,age,password,accountType) VALUES(?,?,?,?,?,?,?)"""
            cur.execute(query_string, (form.firstName.data,form.lastName.data,form.email.data,
                                                    form.gender.data,form.age.data,form.password.data,form.acc_type.data))
            con.commit()
            con.close()
            flash(f'Account created for {form.firstName.data}!','success')
            return redirect(url_for('login'))
    return render_template('reg.html', form=form)

@app.route('/edit-profile', methods=['POST','GET'])
def edit_profile():
    form = RegistrationForm()
    if request.method == 'GET' and 'email' in session:
        con = sqlite3.connect("mydatabase.db")
        cur = con.cursor()
        query_string = """SELECT * FROM user WHERE email =?"""
        cur.execute(query_string, (session['email'],))
        user = cur.fetchall()
        con.close()
        return render_template('edit-profile.html',form=form,uFirstname=user[0][1],uLastname=user[0][2],
                        uEmail=user[0][3],uSex=user[0][5],uAge=user[0][6],uAccType=user[0][7])
    if request.method == 'POST':
        con = sqlite3.connect("mydatabase.db")
        cur = con.cursor()
        query_string = """UPDATE user SET firstName=?,lastName=?,age=?,password=? WHERE email=?"""
        cur.execute(query_string, (request.form['firstName'],request.form['lastName'],request.form['age'],request.form['password'],session['email']))
        con.commit()
        flash(f'Account updated!','success')
        return redirect(url_for('home'))
    
    return redirect(url_for('home'))
    


@app.route('/add-disease', methods=['GET','POST'])
def add_disease():
    if request.method == 'GET' and 'email' in session:
        if session['accType'] == 'doctor':
            con = sqlite3.connect("mydatabase.db")
            cur = con.cursor()
            cur.execute("SELECT organ FROM specialist")
            organs = cur.fetchall()
            return render_template('add-disease.html',organs=organs)
    elif request.method == 'POST':
        disease = request.form['dName']
        definition = request.form['dDefinition']
        organ = request.form['organ']
        degree = request.form['degree']
        tips = request.form['tips']
        symptoms = request.form.getlist('dSym[]')
        addDisease.add(disease,symptoms)
        con = sqlite3.connect("mydatabase.db")
        cur = con.cursor()
        query_string = """INSERT INTO diseases (disease,difinition,degree,organ) VALUES (?,?,?,?)"""
        cur.execute(query_string, (disease,definition,degree,organ))
        con.commit()
        query_string = """INSERT INTO tips (disease,tips) VALUES (?,?)"""
        cur.execute(query_string, (disease,tips))
        con.commit()
        for sym in symptoms:
            if sym != "":
                query_string = """INSERT INTO symptoms (disease,symptom) VALUES (?,?)"""
                cur.execute(query_string, (disease,sym))
                con.commit()
        con.close()
        flash(f'Disease added successfuy!','success')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'GET' and 'email' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        session.pop('visitor', None)
        if form.validate_on_submit():
            con = sqlite3.connect("mydatabase.db")
            cur = con.cursor()
            query_string = """SELECT * FROM user WHERE email=? AND password=?"""
            cur.execute(query_string, (form.email.data,form.password.data,))
            users = cur.fetchall()
            con.close()
            if len(users) > 0:
                session['email'] = form.email.data
                session['firstname'] = users[0][1]
                session['lastname'] = users[0][2]
                session['sex'] = users[0][5]
                session['age'] = users[0][6]
                session['accType'] = users[0][7]
                flash(f'Welcome back {users[0][1]}!','success')
                return redirect(url_for('home'))
            else :
                flash(f'Login Faild!','danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

@app.route('/doctor-contacts',methods=['GET'])
def doctor_contacts():
    if 'email' in session:
        con = sqlite3.connect("mydatabase.db")
        cur = con.cursor()
        query_string = """SELECT firstName,lastName,email,specialization FROM user WHERE accountType = 'doctor'"""
        cur.execute(query_string)
        doctors = cur.fetchall()
        con.close()
        if len(doctors) >= 0:
            return render_template('doctor-contacts.html',doctors=doctors)
        else:
            flash(f'Sorry no available doctor right now!','danger')        
    return redirect(url_for('home'))

@app.route('/search-disease',methods=['POST'])
def search_disease():
    if  request.method == 'POST' and 'email' in session:
        diseaseName = request.form['diseaseName']
        diseasesInfo = getDiseaseData(diseaseName)
        if len(diseasesInfo) > 0:
            diseasesSyms = getAllSyms(diseaseName)
            specialist = getSpecialist(diseasesInfo[4])
            diseasesTips = getTips(diseaseName)
            return render_template('search-disease.html',diseaseName=diseaseName,diseasesInfo=diseasesInfo,diseasesSyms=diseasesSyms,
                                                    specialist=specialist,diseasesTips=diseasesTips)
        else:
            flash(f'Disease not found, We will consider it soon!','danger')
    return redirect(url_for('home'))
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------

lemmatizer = WordNetLemmatizer()




# chat initialization
model = load_model("chatbot_model.h5")
intents = json.loads(open("intents.json").read())
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))


app.secret_key = 'chatsecret'

responsed_once = []

@app.route("/chat")
def chat_home():
    session['scenario']='chat'
    session['mode']=''

    # db.session.add(user)
    # db.session.commit()
    responsed_once.clear()
    return render_template("chatbot_index.html")



@app.route("/get", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]
    
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
    sentence = normalize(sentence)
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

DENT_SPECIALIZATIONS = ['Periodontics', 'Oral Medicine', 'Endodontics', 'Prosthodontics', 'Pediatric dentistry', 'Veterinary dentistry', 'Geriatric dentistry', 'Orthodontics', 'dentofacial orthopedics', 'dentofacial orthopedics']

def getResponse(ints, intents_json):
    tag = ints[0]["intent"]
    
    if tag in DENT_SPECIALIZATIONS and tag not in responsed_once:
        responsed_once.append(tag)
        result = random.choice([" علشان نتأكد اكتر, ممكن تقولي اعراض تانية؟" , "عشان اقدر اساعدك اكتر, ممكن تقولي اعراض تانية؟"])
        return result
        
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i["responses"])
            break
    return result




if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
