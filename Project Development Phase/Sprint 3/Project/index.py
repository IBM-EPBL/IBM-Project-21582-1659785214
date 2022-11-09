from random import randint
from flask import Flask,render_template,request,url_for,redirect,session,jsonify
from flask_mail import *
import ibm_db

try:
    conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31198;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=bjn03696;PWD=ef96tLJX2VjzaCPX;", "", "")
    print("Db connected")
except:
    print("Error")

dictionaryForEmailDonor={}
def printDonorData(conn):
    sql = "SELECT * FROM donorregistration"
    out = ibm_db.exec_immediate(conn, sql)
    document = ibm_db.fetch_assoc(out)
    while document != False:
        dictionaryForEmailDonor.update({document['EMAIL']:document['PASSWORD']})
        document = ibm_db.fetch_assoc(out)

dictionaryForEmailRecipient={}
def printRecipientData(conn):
    sql = "SELECT * FROM recipientregistration"
    out = ibm_db.exec_immediate(conn, sql)
    document = ibm_db.fetch_assoc(out)
    while document != False:
        dictionaryForEmailRecipient.update({document['EMAIL']:document['PASSWORD']})
        document = ibm_db.fetch_assoc(out)

dictionaryForEmailIncharge={}
def printInchargeData(conn):
    sql = "SELECT * FROM inchargeregistration"
    out = ibm_db.exec_immediate(conn, sql)
    document = ibm_db.fetch_assoc(out)
    while document != False:
        dictionaryForEmailIncharge.update({document['EMAIL']:document['PASSWORD']})
        document = ibm_db.fetch_assoc(out)

def insertDonorData(conn,username,firstname,lastname,age,gender,blood,email,phonenumber,password,district,pincode):
    sql="INSERT INTO donorregistration(username,firstname,lastname,age,gender,blood,email,phonenumber,password,district,pincode) VALUES ('{}','{}','{}',{},'{}','{}','{}',{},'{}','{}',{})".format(username,firstname,lastname,age,gender,blood,email,phonenumber,password,district,pincode)
    out = ibm_db.exec_immediate(conn,sql)
    print('Number of affected rows : ',ibm_db.num_rows(out),"\n")

def insertRecipientData(conn,username,firstname,lastname,age,gender,blood,email,phonenumber,password,district,pincode):
    sql="INSERT INTO recipientregistration(username,firstname,lastname,age,gender,blood,email,phonenumber,password,district,pincode) VALUES ('{}','{}','{}',{},'{}','{}','{}',{},'{}','{}',{})".format(username,firstname,lastname,age,gender,blood,email,phonenumber,password,district,pincode)
    out = ibm_db.exec_immediate(conn,sql)
    print('Number of affected rows : ',ibm_db.num_rows(out),"\n")

def insertInchargeData(conn,hospitalname,email,phonenumber,password,district,address,pincode):
    sql="INSERT INTO inchargeregistration(hospitalname,email,phonenumber,password,district,address,pincode) VALUES ('{}','{}',{},'{}','{}','{}',{})".format(hospitalname,email,phonenumber,password,district,address,pincode)
    out = ibm_db.exec_immediate(conn,sql)
    print('Number of affected rows : ',ibm_db.num_rows(out),"\n")

def deleteDonorData(conn,email):
    sql = "DELETE FROM donorregistration WHERE email={}".format(email)
    out = ibm_db.exec_immediate(conn, sql)
    print('Number of affected rows : ', ibm_db.num_rows(out), "\n")

def deleteRecipientData(conn,email):
    sql = "DELETE FROM recipientregistration WHERE email={}".format(email)
    out = ibm_db.exec_immediate(conn, sql)
    print('Number of affected rows : ', ibm_db.num_rows(out), "\n")

def deleteInchargeData(conn,email):
    sql = "DELETE FROM inchargeregistration WHERE email={}".format(email)
    out = ibm_db.exec_immediate(conn, sql)
    print('Number of affected rows : ', ibm_db.num_rows(out), "\n")

app=Flask(__name__)
app.config['SECRET_KEY']='-RFins9nLKTN-FHawdrPAQ'
app.config['MAIL_SERVER']='smtp.gmail.com'  
app.config['MAIL_PORT']=465  
app.config['MAIL_USERNAME'] = 'gowrishankarj1110@gmail.com'  
app.config['MAIL_PASSWORD'] = 'lzwzepnteyvcfibb'  # to be get changed 
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True  
mail = Mail(app)  
otp = randint(000000,999999)

@app.route("/",methods=['POST','GET'])
def index():
    return render_template("indexpage.html")

@app.route("/inchargelogin",methods=['POST','GET'])
def inchargelogin():
    if request.method=="POST":
        printInchargeData(conn)
        text=request.form['text']
        password=request.form['password']
        try:
            if dictionaryForEmailIncharge[text] == (password):
                session['inchargeloggedin']=True
                session['inchargeemail']=text
                return redirect(url_for('inchargehome'))
        except Exception as e:
            print(e)
            return "invalid email or password"
    return render_template("inchargelogin.html")

@app.route("/inchargeregister",methods=['POST','GET'])
def inchargeregister():
    if request.method=="POST":
        hospitalname = request.form['hospitalname']
        email = request.form['email']
        phonenumber=request.form['phonenumber']
        district=request.form['district']
        pincode=request.form['pincode']
        address=request.form['address']
        password = request.form['password']
        insertInchargeData(conn,hospitalname,email,phonenumber,password,district,address,pincode)
        return redirect(url_for('inchargeauthentication',email=email))
    return render_template('inchargeregister.html')

@app.route("/recipientlogin",methods=['POST','GET'])
def recipientlogin():
    if request.method=="POST":
        printRecipientData(conn)
        text=request.form['text']
        password=request.form['password']
        try:
            if dictionaryForEmailRecipient[text] == password:
                session['recipientloggedin']=True
                session['recipientemail']=text
                return redirect(url_for('recipienthome'))
        except Exception as e:
            print(e)
            return "invalid email or password"
    return render_template("recipientlogin.html")

@app.route("/recipientregister",methods=['POST','GET'])
def recipientregister():
    if request.method=="POST":
        username = request.form['username']
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        gender=request.form['gender']
        age=request.form['age']
        blood=request.form['blood']
        email = request.form['email']
        phonenumber=request.form['phonenumber']
        district=request.form['district']
        pincode=request.form['pincode']
        password = request.form['password']
        insertRecipientData(conn,username,firstname,lastname,age,gender,blood,email,phonenumber,password,district,pincode)
        return redirect(url_for('recipientauthentication',email=email))
    return render_template('recipientregister.html')

@app.route("/inchargeauthentication/<email>",methods=['GET','POST'])
def inchargeauthentication(email):
    msg = Message('OTP',sender = 'gowrishankarj1110@gmail.com', recipients = [email])  
    msg.body = str(otp)  
    mail.send(msg)
    return render_template('inchargeauthentication.html',email=email) 

@app.route('/inchargevalidate',methods=["POST"])  
def inchargevalidate():  
    user_otp = request.form['otp']  
    email=request.form['email']
    email.lower()
    if otp == int(user_otp):  
        return render_template("inchargelogin.html")
    else:
        deleteInchargeData(conn,email)
        return "<h3>failure</h3>"  

@app.route("/recipientauthentication/<email>",methods=['GET','POST'])
def recipientauthentication(email):
    msg = Message('OTP',sender = 'gowrishankarj1110@gmail.com', recipients = [email])  
    msg.body = str(otp)  
    mail.send(msg)
    return render_template('recipientauthentication.html',email=email) 

@app.route('/recipientvalidate',methods=["POST"])  
def recipientvalidate():  
    user_otp = request.form['otp']  
    email=request.form['email']
    email.lower()
    if otp == int(user_otp):  
        return render_template("recipientlogin.html")
    else:
        deleteRecipientData(conn,email)
        return "<h3>failure</h3>"  

@app.route("/donorauthentication/<email>",methods=['GET','POST'])
def donorauthentication(email):
    msg = Message('OTP',sender = 'gowrishankarj1110@gmail.com', recipients = [email])  
    msg.body = str(otp)  
    mail.send(msg)
    return render_template('donorauthentication.html',email=email) 

@app.route('/donorvalidate',methods=["POST"])  
def donorvalidate():  
    user_otp = request.form['otp']  
    email=request.form['email']
    email.lower()
    if otp == int(user_otp):  
        return render_template("donorlogin.html")
    else:
        deleteDonorData(conn,email)
        return "<h3>failure</h3>"  

@app.route("/donorlogin",methods=['POST','GET'])
def donorlogin():
    if request.method=="POST":
        printDonorData(conn)
        text=request.form['text']
        password=str(request.form['password'])
        try:
            if dictionaryForEmailDonor[text] == (password):
                session['donorloggedin']=True
                session['donoremail']=text
                return redirect(url_for('donorhome'))
        except Exception as e:
            print(e)
            return "invalid email or password"
    return render_template("donorlogin.html")

@app.route("/donorregister",methods=['POST','GET'])
def donorregister():
    if request.method=="POST":
        username = request.form['username']
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        gender=request.form['gender']
        age=request.form['age']
        blood=request.form['blood']
        email = request.form['email']
        phonenumber=request.form['phonenumber']
        district=request.form['district']
        pincode=request.form['pincode']
        password = request.form['password']
        insertDonorData(conn,username,firstname,lastname,age,gender,blood,email,phonenumber,password,district,pincode)
        return redirect(url_for('donorauthentication',email=email))
    return render_template('donorregister.html')

@app.route("/donorhome",methods=['POST','GET'])
def donorhome():
    try:
        if session['donorloggedin']==True:
            status='' # data we need, to be stored in this str
            query="SELECT donated FROM donationdetails WHERE email = '{}'".format(session['donoremail'])
            stmt = ibm_db.exec_immediate(conn,query)
            while ibm_db.fetch_row(stmt)!=False: #to store the db data
                status=(ibm_db.result(stmt,0))
            print("status = ",status)
            
            if status=='yes':
                send = "You have already donated, After 28 days from your donation date only, you can donate"
                firstname='' # data we need, to be stored in this str
                query="SELECT firstname FROM donationdetails WHERE email = '{}'".format(session['donoremail'])
                stmt = ibm_db.exec_immediate(conn,query)  # do the task
                while ibm_db.fetch_row(stmt)!=False: #to store the db data
                    firstname=(ibm_db.result(stmt,0))
                
                date='' # data we need, to be stored in this str
                query="SELECT donationdate FROM donationdetails WHERE email = '{}'".format(session['donoremail'])
                stmt = ibm_db.exec_immediate(conn,query)  # do the task
                while ibm_db.fetch_row(stmt)!=False: #to store the db data
                    date=(ibm_db.result(stmt,0))
                print("date = ",date)
                import datetime
                if (date.today() - date)>=datetime.timedelta(28):
                    print("Yes")
                    query="delete from donationdetails WHERE email = '{}'".format(session['donoremail'])
                    stmt = ibm_db.exec_immediate(conn,query) 
                    return render_template('donorhome.html',email=session['donoremail'],firstname=firstname)
                else:
                    print(date.today() - date)
                    print('No')
                return render_template('donorstatus.html',firstname=firstname,email=session['donoremail'],msg=send)

            districts=[]
            query3="select distinct district from inchargeregistration"
            stmt3=ibm_db.exec_immediate(conn,query3)
            while ibm_db.fetch_row(stmt3)!=False:
                districts.append(ibm_db.result(stmt3,0))
                print(districts)
            print(type(districts))

            hospitals=[]
            query2='select hospitalname from inchargeregistration'
            stmt2=ibm_db.exec_immediate(conn,query2)
            while ibm_db.fetch_row(stmt2)!=False:
                hospitals.append(ibm_db.result(stmt2,0))
                print(hospitals)
                
            firstname='' # data we need, to be stored in this str
            query="SELECT firstname FROM DONORREGISTRATION WHERE email = '{}'".format(session['donoremail'])
            stmt = ibm_db.exec_immediate(conn,query)  # do the task
            while ibm_db.fetch_row(stmt)!=False: #to store the db data
                firstname=(ibm_db.result(stmt,0))

            if request.method=='POST':
                print(request.form['age'])
                if request.form['age']=='yes':
                    if request.form['weight']=='yes':
                        if request.form['height']=='yes':
                            if request.form['drug']=='no':
                                if request.form['pregnant']=='no':
                                    if request.form['iron']=='no':
                                        if request.form['endoscopy']=='no':
                                            if request.form['cough']=='no':
                                                if request.form['vomit']=='no':
                                                    if request.form['covid']=='no':
                                                        if request.form['antibodies']=='no':
                                                            return render_template('donationform.html',email=session['donoremail'],firstname=firstname,status=status,districts=districts)
                                                        else:
                                                            return "not eligible to donate.<a href={{ url_for('donorlogout') }}><button>Log Out</button></a>"
                                                    else:
                                                        return "not eligible to donate.<a href={{ url_for('donorlogout') }}><button>Log Out</button></a>"
                                                else:
                                                    return "not eligible to donate.<a href={{ url_for('donorlogout') }}><button>Log Out</button></a>"
                                            else:
                                                return "not eligible to donate.<a href={{ url_for('donorlogout') }}><button>Log Out</button></a>"
                                        else:
                                            return "not eligible to donate.<a href={{ url_for('donorlogout') }}><button>Log Out</button></a>"
                                    else:
                                        return "not eligible to donate.<a href={{ url_for('donorlogout') }}><button>Log Out</button></a>"
                                else:
                                    return "not eligible to donate.<a href={{ url_for('donorlogout') }}><button>Log Out</button></a>"
                            else:
                                return "not eligible to donate.<a href={{ url_for('donorlogout') }}><button>Log Out</button></a>"
                        else:
                            return "not eligible to donate.<a href={{ url_for('donorlogout') }}><button>Log Out</button></a>"
                    else:
                        return "not eligible to donate.<a href={{ url_for('donorlogout') }}><button>Log Out</button></a>"
                else:
                    return "not eligible to donate.<a href={{ url_for('donorlogout') }}><button>Log Out</button></a>"
            return render_template('donorhome.html',email=session['donoremail'],firstname=firstname,status=status,districts=districts)
    except KeyError:
        return "You have been logged out."

@app.route("/hospitals/<district>")
def hospitalbydistrict(district):
    hospitals=[]
    query2="SELECT hospitalname FROM inchargeregistration WHERE district = '{}'".format(district)
    stmt2=ibm_db.exec_immediate(conn,query2)
    while ibm_db.fetch_row(stmt2)!=False:
        hospitals.append(ibm_db.result(stmt2,0))
    print(hospitals)
    return jsonify({'districthospital':hospitals})

@app.route("/hospitalhaving/<district>")
def hospitalhavingbydistrict(district):
    hospitals=[]
    query2="SELECT hospital FROM hospitalhaving WHERE district = '{}'".format(district)
    stmt2=ibm_db.exec_immediate(conn,query2)
    while ibm_db.fetch_row(stmt2)!=False:
        hospitals.append(ibm_db.result(stmt2,0))
    print(hospitals)
    return jsonify({'districthospital':hospitals})

@app.route("/blood/<hospital>")
def bloodbyhospital(hospital):
    bloods=[]
    query3="SELECT blood FROM hospitalhaving WHERE hospital = '{}'".format(hospital)
    stmt3=ibm_db.exec_immediate(conn,query3)
    while ibm_db.fetch_row(stmt3)!=False:
        bloods.append(ibm_db.result(stmt3,0))
    print(bloods)
    return jsonify({'bloodshospital':bloods})

@app.route("/donationdetails",methods=['POST','GET'])
def donationdetails():
    donated=False
    if request.method=='POST':
        firstname='' # data we need, to be stored in this str
        query="SELECT firstname FROM DONORREGISTRATION WHERE email = '{}'".format(session['donoremail'])
        stmt = ibm_db.exec_immediate(conn,query)  # do the task
        while ibm_db.fetch_row(stmt)!=False: #to store the db data
            firstname=(ibm_db.result(stmt,0))
        username=request.form['username']
        firstname=request.form['firstname']
        email=request.form['email']
        phonenumber=request.form['phonenumber']
        district=request.form['district']
        hospitalname=request.form['hospitalname']
        donationdate=request.form['donationdate']
        blood=request.form['blood']
        sql="INSERT INTO donationdetails(username,firstname,email,phonenumber,district,hospitalname,donationdate,blood) VALUES ('{}','{}','{}',{},'{}','{}','{}','{}')".format(username,firstname,email,phonenumber,district,hospitalname,donationdate,blood)
        stmt = ibm_db.exec_immediate(conn,sql)  # do the task
        donated=True
        send="{} have applied for donation on {} in {}, {}.".format(firstname,donationdate,hospitalname,district)
        hospitalemail=''
        query="SELECT email FROM inchargeregistration WHERE hospitalname = '{}'".format(hospitalname)
        stmt = ibm_db.exec_immediate(conn,query)  # do the task
        while ibm_db.fetch_row(stmt)!=False: #to store the db data
            hospitalemail=(ibm_db.result(stmt,0))
        msg = Message('Info',sender = 'gowrishankarj1110@gmail.com', recipients = [hospitalemail])  
        msg.body = send
        mail.send(msg)
        msg = Message('Info',sender = 'gowrishankarj1110@gmail.com', recipients = [email])  
        msg.body = send
        mail.send(msg)
        return render_template('donorstatus.html',donated=donated,email=session['donoremail'],firstname=firstname,msg=send)
    return render_template('donorhome.html',donated=donated)
    
@app.route("/donorlogout",methods=['POST','GET'])
def donorlogout():
    session.pop('donorloggedin',None)
    session.pop('donoremail',None)
    return redirect(url_for('index'))

@app.route("/recipienthome",methods=['POST','GET'])
def recipienthome():
    try:
        if session['recipientloggedin']==True:
            if request.method=='POST':
                recipientname=request.form['recipientname']
                email=request.form['email']
                phonenumber=request.form['phonenumber']
                district=request.form['district']
                hospital=request.form['hospitalname']
                requestedblood=request.form['blood']
                sql="INSERT INTO recipientrequested(recipientname,email,phonenumber,district,hospital,requestedblood) VALUES ('{}','{}',{},'{}','{}','{}')".format(recipientname,email,phonenumber,district,hospital,requestedblood)
                stmt = ibm_db.exec_immediate(conn,sql)
                hospitalemail=''
                query="SELECT email FROM inchargeregistration WHERE hospitalname = '{}'".format(hospital)
                stmt = ibm_db.exec_immediate(conn,query)  # do the task
                while ibm_db.fetch_row(stmt)!=False: #to store the db data
                    hospitalemail=(ibm_db.result(stmt,0))
                send="{} have applied for requesting blood on tomorrow in {}, {}.".format(recipientname,hospital,district)
                msg = Message('Info',sender = 'gowrishankarj1110@gmail.com', recipients = [hospitalemail])  
                msg.body = send
                mail.send(msg)
                msg1='You need get it tomorrow.'
                return render_template('recipientstatus.html',email=session['recipientemail'],send=send,msg1=msg1)
            districts=[]
            query3="select distinct district from hospitalhaving"
            stmt3=ibm_db.exec_immediate(conn,query3)
            while ibm_db.fetch_row(stmt3)!=False:
                districts.append(ibm_db.result(stmt3,0))
                print(districts)
            print(type(districts))
            return render_template('recipienthome.html',email=session['recipientemail'],districts=districts)
    except KeyError:
        return "You have been logged out."

@app.route("/recipientlogout",methods=['POST','GET'])
def recipientlogout():
    session.pop('recipientloggedin',None)
    session.pop('recipientemail',None)
    return redirect(url_for('index'))

@app.route("/inchargehome",methods=['POST','GET'])
def inchargehome():
    try:
        if session['inchargeloggedin']==True:
            return render_template('inchargehome.html',email=session['inchargeemail'])
    except KeyError:
        return "You have been logged out."

@app.route("/inchargelogout",methods=['POST','GET'])
def inchargelogout():
    session.pop('inchargeloggedin',None)
    session.pop('inchargeemail',None)
    return redirect(url_for('index'))

@app.route("/inchargedonor",methods=['POST','GET'])
def inchargedonor():
    try:
        if session['inchargeloggedin']==True:
            if request.method=='POST':
                email=request.form['email']
                donated=request.form['donated']
                query="update donationdetails set donated = '{}' where email = '{}';".format(donated,email)
                stmt = ibm_db.exec_immediate(conn,query)
                firstname='' # data we need, to be stored in this str
                query="SELECT firstname FROM donationdetails WHERE email = '{}'".format(email)
                stmt = ibm_db.exec_immediate(conn,query)
                while ibm_db.fetch_row(stmt)!=False: #to store the db data
                    firstname=(ibm_db.result(stmt,0))
                send="{} have finished the donation".format(firstname)
                msg = Message('Info',sender = 'gowrishankarj1110@gmail.com', recipients = [email])  
                msg.body = send
                mail.send(msg)
                return render_template('inchargehome.html',email=session['inchargeemail'])
            return render_template('inchargehome.html',email=session['inchargeemail'])
    except KeyError:
        return "You have been logged out."

@app.route("/inchargerecipient",methods=['POST','GET'])
def inchargerecipient():
    try:
        if session['inchargeloggedin']==True:
            if request.method=='POST':
                donoremail=request.form['email']
                hospitalname=request.form['hospitalname']
                query="delete from hospitalhaving where hospital = '{}' and email='{}';".format(hospitalname,donoremail)
                stmt = ibm_db.exec_immediate(conn,query)
                receiveremail=request.form['emailreceiver']
                send="You have finished the Receiving the blood"
                msg = Message('Info',sender = 'gowrishankarj1110@gmail.com', recipients = [receiveremail])  
                msg.body = send
                mail.send(msg)
                query="delete from recipientrequested where email='{}';".format(receiveremail)
                stmt = ibm_db.exec_immediate(conn,query)
                return render_template('inchargehome.html',email=session['inchargeemail'])
            return render_template('inchargehome.html',email=session['inchargeemail'])
    except KeyError:
        return "You have been logged out."

@app.after_request    #after session pop when we click back python flask
def after_request(response):
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response

if __name__ == "__main__":
    app.run(debug=True)