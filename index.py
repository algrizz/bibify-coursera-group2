#Thanks for using this project
#By Alejandro Acosta 
#Sep 2017
#Capstone Project for the Cybersecurity Specialization

#Usage:
#python <thisfile>
#python index.py

from werkzeug.exceptions import HTTPException
from flask import Flask, abort, jsonify
from flask import Flask, render_template, flash, request, session, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from miforms import *  #In the file miforms.py are all the forms

#It´s recommended to usea server with a webserver in the frontend. Running directly for simplicity
PORT = 8000 #Port in which our APP will run
SALT = 'COURsera.1234' #We are using the Salt technique. Variable used append to the password

app = Flask(__name__,static_url_path='', static_folder='web/static' ) #new object
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a' #security to handle the form. Mandatory

@app.errorhandler(404)
def page_not_found(a=''):
  return render_template('404.html')

@app.errorhandler(Exception)
def handle_error(e):
  return render_template('404.html')


def BasicSanityCheckString(WHAT, VALUE):
  #The objetive of this function is to make very basic security checks of a input string
  #such as checking if it has spaces, ";", ",", "=", stripping and so on
  import re
  if WHAT == 'Email':
    return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", VALUE)) 
  if WHAT == 'Password':
    return bool(len(VALUE) > 7)
  if WHAT == 'CODE':
    return bool(len(VALUE) == 36)
  pass

def GENERATERANDOMSTRING():
  #The objetivo of this function is to return a random string. Used for registering and password recovery
  import uuid
  return str(uuid.uuid4())

def sendemail(email, code, name):
  #In this function we send the confirmation email after filling the registration form
  import smtplib

  sender = 'no-reply@coursera.acostasite.com'
  receivers = str(email)
  CODE=str(code)
  LINK='http://coursera.acostasite.com:8000/verify/'+str(CODE)

  message = """

  To confirm your registrion please 
  click in the following link:

  """

  message = message + LINK + "\n\n Thanks \n Team Cybersecurity Capstone"
  FROM = sender

  to = email
  smtpserver = smtplib.SMTP("127.0.0.1",25)
  smtpserver.ehlo()
  smtpserver.ehlo() # extra characters to permit edit
  header = 'To:' + to + '\n' + 'From: ' + FROM + '\n' + 'Subject:Confirm your email address. Coursera Capstone! \n'
  msg = header + message
  smtpserver.sendmail(FROM, to, msg)
  smtpserver.quit()

def secondfactor(email):
  #In this function we send a link to the email of the user
  #as a second factor auth of the user
  #We also save in DBs the info the system/user will need to satisfy secondfactor auth
  import smtplib

  sender = 'no-reply@coursera.acostasite.com'
  receivers = str(email)
  CODE=GENERATERANDOMSTRING() # CODE is used as validator for registration and password recovery
  LINK='http://coursera.acostasite.com:8000/verify2/'+str(CODE)

  message = """

  To complete your login
  click in the following link:

  """

  message = message + LINK + "\n\n Thanks \n Team Cybersecurity Capstone"
  FROM = sender

  to = email
  smtpserver = smtplib.SMTP("127.0.0.1",25)
  smtpserver.ehlo()
  smtpserver.ehlo() # extra characters to permit edit
  header = 'To:' + to + '\n' + 'From: ' + FROM + '\n' + 'Subject:Please click in the link to finish your login. Coursera Capstone! \n'
  msg = header + message
  smtpserver.sendmail(FROM, to, msg)
  smtpserver.quit()

  QUERY=("INSERT into SECONDFACTOR (`EMAIL`,`CODE`) values (%s,%s)")
  ARGS=(email,CODE)
  rows=QueryDB(QUERY,ARGS)

def SendLinkSetPassword(email, code):
  #In this function we send a new link to set a new password
  import smtplib
    
  sender = 'no-reply@coursera.acostasite.com'
  receivers = str(email)
  CODE=str(code)
  LINK='http://coursera.acostasite.com:8000/setnewpassword/'+str(CODE)
    
  message = """
  NOTE: In case you did not request this email please ignore it.

  Please to set a new passwod please follow the link below:

  """

  message = message + LINK + "\n\n Thanks \n Team Cybersecurity Capstone"
  FROM = sender

  to = email
  smtpserver = smtplib.SMTP("127.0.0.1",25)
  smtpserver.ehlo()
  smtpserver.ehlo() # extra characters to permit edit
  header = 'To:' + to + '\n' + 'From: ' + FROM + '\n' + 'Subject:Your password recovery link - Cybersecurity Capstone! \n'
  msg = header + message
  smtpserver.sendmail(FROM, to, msg)
  smtpserver.quit()

def PasswordRecovery(EMAIL):
  #returns 0 if positive
  RETURNVALUE=1
  QUERY="SELECT EMAIL FROM USERS WHERE EMAIL = %s LIMIT 1"
  rows=QueryDB(QUERY,EMAIL)
  if len(rows) == 0:  #In case the CODE was not found
     flash ('Error: Can not continue, email not found') #uncomment for debugging
     return 1
  CODE=GENERATERANDOMSTRING() # CODE is used as validator for registration and password recovery
  SendLinkSetPassword(EMAIL, CODE)  #We will send a link to the user in order to set a new password

  QUERY="UPDATE USERS SET VERIFIED = 1 WHERE EMAIL = %s "
  rows=QueryDB(QUERY,EMAIL)
  QUERY=("INSERT into UNVERIFIED_USER (`EMAIL`,`CODE`) values (%s,%s)")
  ARGS=(EMAIL,CODE)
  rows=QueryDB(QUERY,ARGS)
  return 0 #if the function reaches this point everything went well
  
@app.route('/lostpassword',methods=['GET','POST']) #decorator
def lostpassword():
    form = LostPasswordForm(request.form)

    print (form.errors)
    if request.method == 'POST':
        email=request.form['email']
        print (email)

        if form.validate(): #builtin Flask validation
            if PasswordRecovery(email) == 0 : #in case email not found
              flash('A new link to set your password has been sent to: ' + email)
        else:
            flash('Error: There was an error processing your form. Are you sure you are registered?. ')


    return render_template('lost_password.html', form=form)


def isloggedin():
  if 'username' in session:
    if 'secondauth' in session:
      print ('Your user is: ',session['username'])
      return session['username']
  return 1 #if the user is not logged in

@app.route('/messageboard') #decorator
def messageboard():
  username = isloggedin()
  if username == 1:
    flash ('Error: You must be logged in in order to use the message board')
    return redirect(url_for('login'))
  else:
    #flash ('Success: Your inbox is')
    #readinbox(username)
    #QUERY="SELECT * FROM USERSDE = %s "
    QUERY="SELECT MSG, TITLE, SOURCE, DESTINATION FROM MESSAGEBOARD WHERE DESTINATION = %s "
    rows=QueryDB(QUERY,str(username))
    if rows is not None:
      print ('Rows is not None')
      for row in rows:
        print (row)
      return render_template('inboxmessageboard.html', data = rows)
    else:
      rows = 'Epa'
      return render_template('404.html', data = rows)

@app.route('/sendnewmessage',methods=['GET','POST']) #decorator
def sendnewmessage():
  username = isloggedin()
  MSG=''
  form = NewMessage(request.form)
  if username == 1: #user is not logged in
    flash ('Error: You must be logged in in order to send messages')
    return redirect(url_for('login'))  #lets send the user to login page


  if request.method == 'GET':
    flash ('Success: Lets create a new message')

  if request.method == 'POST':
        MSG=str(request.form['MSG'])
        TO=str(request.form['TO'])
        SUBJECT=str(request.form['SUBJECT'])
        print (MSG)
        print (TO)
        print (SUBJECT)

        if form.validate(): #builtin Flask validation
              QUERY=("INSERT into MESSAGEBOARD (`MSG`,`DESTINATION`,`TITLE`,`SOURCE`) values (%s,%s,%s,%s)")
              ARGS=(MSG,TO,SUBJECT,username)
              rows=QueryDB(QUERY,ARGS)
              flash('Message Send!! ' + MSG)
        else:
            flash('Error: There was an error processing your form. Are you logged in? ')

  return render_template('sendnewmessage.html', form = form, login=username)

@app.route('/logout') #decorator
def logout():
  if 'username' in session:
    session.pop('username')
    session.pop('secondauth')
  return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST']) #decorator
def login():
    form = LoginForm(request.form)

    username = isloggedin()
    if username is not 1:
        print ('Username: ',username)
        flash ('Error: You can not use the login option. You are already logged in as: ' + username + ' you can logout using the link in the upper bar')
        return redirect(url_for('messageboard'))

    print (form.errors)
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        print (email)

        if form.validate(): #builtin Flask validation
          if BasicSanityCheckString('Email',email) == True: #Lets implement some extra validation. Email
            if BasicSanityCheckString('Password',password) == True: #Lets implement some extra validation. Password
              if AuthUser(email, password) == True: #Lets implement some extra validation. Combination user/pass
                session['username'] = email
                #flash('Login successful ' + email)
                flash('A link was sent to your email in order to finish the log in process. Please check your spam folder')
                secondfactor(email)
              else:
                flash('Error: There was an error processing your form. Are you sure you are registered?. ')
            else:
              flash('Error: There was an error processing your form. Are you sure you are registered?. ')
          else:
            flash('Error: There was an error processing your form. Are you sure you are registered?. ')
        else:
            flash('Error: There was an error processing your form. Are you sure you are registered?. ')


    return render_template('login.html', form=form)

def AuthUser(username,password):
  #This function received username and password
  #it returns True if user authenticated, False if not
  import hashlib #The password is store in DB in hash sha384
  username=str(username)
  #password=str(password)
  password=str(password) + SALT
  h = hashlib.new('sha384')
  h.update(password.encode('UTF-8'))
  myhash = h.hexdigest()
  print ('password:',str(myhash))
  QUERY="SELECT ID FROM USERS WHERE EMAIL = %s and PASS = %s and VERIFIED=0 LIMIT 1"
  ARGS=(username, str(myhash))
  rows=QueryDB(QUERY,ARGS)
  if len(rows) == 0:  #In case no registries were return from the DB
      flash ('Error: Can not continue. Combination of username/pass does not match')
      return False
  else:
     return True

@app.route('/setnewpassword/<CODE>/',methods=['GET','POST']) #decorator
def setnewpassword(CODE):
    #In this function we set a new password for a user
    import hashlib
    form = EnterNewPassword(request.form)

    print (form.errors)
    if request.method == 'POST':
        password=request.form['password']
        print (password)

        if form.validate(): #builtin Flask validation
              password=str(password) + SALT
              password2=hashlib.sha384()
              password2.update(password.encode('UTF-8'))
              QUERY="UPDATE USERS T2, (SELECT EMAIL FROM UNVERIFIED_USER WHERE CODE = %s LIMIT 1) T1 SET PASS = %s, VERIFIED=0 WHERE T2.EMAIL = T1.EMAIL "
              ARGS=(str(CODE), str(password2))
              rows=QueryDB(QUERY,ARGS)
              QUERY="DELETE FROM UNVERIFIED_USER WHERE CODE = %s "
              rows=QueryDB(QUERY,CODE)

              flash('Your password has been updated: ' )
        else:
            flash('Error: There was an error processing your form. Are you sure you are registered?. ')


    return render_template('setnewpassword.html', form=form)

@app.route('/') #decorator
def index():
    form = ReusableForm(request.form)
 
    print (form.errors)
    if request.method == 'POST':
        name=request.form['name']
        password=request.form['password']
        email=request.form['email']
        print (name, " ", email, " ", password)
 
        if form.validate():
            # Save the comment here.
            flash('An email was sent to ' + name + ' in order to confirm your registration. Please check your spam folder')
        else:
            flash('Error: There was an error processing your form. Please check the data. ')
  
 
    return redirect(url_for('login'))
    #return render_template('user.html', form=form)

def ValidateFormRegistry(name, password, email):
  #The objetive is to validate some input fields
  # 0 means valid, 1 means invalid

  #Validate name not empty, not null longer than 2 chars and less than 40 chars
  VALID=0
  if (name.strip()) and len(name) < 40 and len(name) > 2:  #name is not empty and also validate null
    flash('Name good ')
  else:
    VALID=1
    flash('Error: Invalid name. Is it empty?, too long? ', 'error' ) 
    #return 1

  #validate strong password. Min 8 chars, must contain uppercase, lowercase characters
  import re
  if re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
    flash('Password strong enough ')
    #return 0
  else:
    flash('Error: Invalid password ') 
    #return 1
  
  #validate valid email address. As a reminder, the DB validates uniqueness of the email adddress
  if (bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))):
    flash('Valid email address ')
  else:
    flash('Error: Invalid email  address') 

@app.route('/verify/<CODE>/') #decorator
def verify(CODE):
    #The objetive of this funcion is confirm registration/email address of a user
    form = ReusableForm(request.form)
    CODE=str(CODE)
    #flash('Good: ' + CODE)
    #return render_template('user.html', form=form)
    #QUERY="SELECT EMAIL, CODE FROM UNVERIFIED_USER WHERE CODE = %s", (str(CODE))
    QUERY="SELECT EMAIL, CODE FROM UNVERIFIED_USER WHERE CODE = %s LIMIT 1"
    rows=QueryDB(QUERY,CODE)
    if len(rows) == 0:  #In case the CODE was not found
      flash ('Can not continue, confirmation code not found. It might have been already confirmed')
      return render_template('user.html', form=form)

    QUERY="UPDATE USERS SET VERIFIED = 0 WHERE EMAIL = %s "
    EMAIL = rows[0][0] #rows[0][0] corresponds to email of the first rs
    rows=QueryDB(QUERY,EMAIL) 
    #print (rows, 'EMAIL: ', rows[0][0])
    #flash('Good: ' + rows[0][0])
    flash ('Good news, your user is now confirmed')

    QUERY="DELETE FROM UNVERIFIED_USER WHERE EMAIL = %s " #This user is not longer needed in UNVERIFIED table
    rows=QueryDB(QUERY,EMAIL) 

    return render_template('user.html', form=form)

@app.route('/verify2/<CODE>/') #decorator
def verify2(CODE):

    if (BasicSanityCheckString('CODE', CODE)) is not True:  #Let's check the CODE recevied in the URL
      flash ('Error: Code not found, cookie not found. Something wrong. Please try to logout and then login again')
      return render_template('404.html')

    if 'username' in session:
       username=session['username']
       print ('Your user is: ',session['username']) #in this stage this cookie should be in the browser
       form = ReusableForm(request.form)
       CODE=str(CODE)
       #flash('Good: ' + CODE)
       #return render_template('user.html', form=form)
       #QUERY="SELECT EMAIL, CODE FROM UNVERIFIED_USER WHERE CODE = %s", (str(CODE))
       QUERY="SELECT EMAIL, CODE FROM SECONDFACTOR WHERE CODE = %s AND EMAIL = %s LIMIT 1"
       ARGS=(CODE,username)
       rows=QueryDB(QUERY,ARGS)
       if len(rows) == 0:  #In case the CODE was not found
        flash ('Can not continue, confirmation code not found. It might have been already confirmed')
        return render_template('user.html', form=form)

        flash ('You are now logged in')

       QUERY="DELETE FROM SECONDFACTOR WHERE EMAIL = %s " #This user is not longer needed in SECONDFACTOR table
       rows=QueryDB(QUERY,username)
       session['secondauth']=True

       return redirect(url_for('messageboard'))
    else:
      flash ('Error: Code not found, cookie not found. Something wrong. Please try to logout and then login again')
      return render_template('404.html')


def QueryDB(QUERY, DATA):
  #Receive a SQL Query returns a record set
  print (QUERY)
  import dbconnect
  conn = dbconnect.dbconnect()
  conn.autocommit(True)
  cur = conn.cursor()
  cur.execute(QUERY, DATA)
  rows = cur.fetchall()
  if rows is not None:
    return rows
  else:
    return "Error"

@app.route('/registry',methods=['GET','POST']) #decorator
def registy():
    form = ReusableForm(request.form)
    username = isloggedin()
    if username is not 1:
        flash ('Error: You can not use the registry option because you are already logged in as: ' + username + ' you can logout using the link in the upper bar')
        return redirect(url_for('messageboard'))

    print (form.errors)
    if request.method == 'POST':
        name=request.form['name']  #Get the variables from the form
        password=request.form['password']
        email=request.form['email']
        password2=request.form['password2']
        #print (name, " ", email, " ", password)  #just for debugging in the Flask console

        #if (ValidateFormRegistry(name, password, email)): #Even when there is some sort of validation make an extra validation
        #    flash('Error: There was an error processing your form. Please check the data. ')

        if form.validate() and password==password2: #Flask internal validation and check if both password enter in the form match
            CODE=GENERATERANDOMSTRING() # CODE is used as validator for registration and password recovery
            SaveRegistrationInDB(name, password, email, CODE) #Only store in DB if passes validation
            sendemail(email, CODE, name)
            flash('Thanks for registration ' + name + 'an email was sent in order to confirm your registration. Please check your spam folder')
        else:
            flash('Error: There was an error processing your form. Please check the data. ')


    return render_template('user.html', form=form)

def SaveRegistrationInDB(name, password, email, CODE):
  #The objetive of the function is to store registration data of the user in DB
  import hashlib #The password is store in DB in hash sha224
  import dbconnect
  conn = dbconnect.dbconnect()
  conn.autocommit(True)
  cur = conn.cursor()
  name=str(name)
  #password=str(password)
  password=str(password) + SALT
  email=str(email)

  h = hashlib.new('sha384')
  h.update(password.encode('UTF-8'))
  myhash = h.hexdigest()

  cur.execute("INSERT into USERS (`FULLNAME`,`PASS`,`EMAIL`) values (%s,%s,%s)", (name, str(myhash),email))
  cur.execute("INSERT into UNVERIFIED_USER (`EMAIL`,`CODE`) values (%s,%s)", (email,str(CODE)))

  return

@app.route('/coursera') #decorator
def coursera():
  return 'returning coursera Ojala sirva'

if __name__ == '__main__':
  app.run(port=PORT,host='0.0.0.0') #Executing the server
