from modes.Text.text import text
from flask import Flask, render_template, request, session
# flash, Blueprint, current_app
from datetime import datetime
import random
import pandas as pd
from flask import send_file
# import os
# from modes.Image.image import image
# from flask_mysqldb import MySQL
# from flask import send_from_directory
# from werkzeug.utils import secure_filename
# import stepic
# from PIL import Image

# UPLOAD_IMAGE_FOLDER = 'modes\\Image\\static'
# IMAGE_CACHE_FOLDER = 'modes\\Image\\__pycache__'
UPLOAD_TEXT_FOLDER = 'modes\\Text\\static'
TEXT_CACHE_FOLDER = 'modes\\Text\\__pycache__'

# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = "hello"

# app.config['UPLOAD_IMAGE_FOLDER'] = UPLOAD_IMAGE_FOLDER
# app.config['IMAGE_CACHE_FOLDER'] = IMAGE_CACHE_FOLDER
app.config['UPLOAD_TEXT_FOLDER'] = UPLOAD_TEXT_FOLDER
app.config['TEXT_CACHE_FOLDER'] = TEXT_CACHE_FOLDER

# app.register_blueprint(image, url_prefix="/image")
app.register_blueprint(text, url_prefix="/text")


@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        pwd = request.form["password"]
        r1 = pd.read_excel('user.xlsx')
        for index, row in r1.iterrows():
            if row["email"] == str(email) and row["password"] == str(pwd):
                return render_template('home.html')
        else:
            msg = 'Invalid Login Try Again'
            return render_template('login.html', msg=msg)
    return render_template('login.html')


@app.route("/home")
def home():
    return render_template("home.html")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['Email']
        Pass = request.form['Password']
        col_list = ["name", "email", "password"]
        r1 = pd.read_excel('user.xlsx', usecols=col_list)
        new_row = {'name': name, 'email': email, 'password': Pass}
        r1 = r1.append(new_row, ignore_index=True)
        r1.to_excel('user.xlsx', index=False)
        print("Records created successfully")
        # msg = 'Entered Mail ID Already Existed'
        msg = 'Registration Successful !! U Can login Here !!!'
        return render_template('login.html', msg=msg)
    return render_template('register.html')


@app.route('/password', methods=['POST', 'GET'])
def password():
    if request.method == 'POST':
        current_pass = request.form['current']
        new_pass = request.form['new']
        verify_pass = request.form['verify']
        r1 = pd.read_excel('user.xlsx')
        for index, row in r1.iterrows():
            if row["password"] == str(current_pass):
                if new_pass == verify_pass:
                    r1.replace(to_replace=current_pass, value=verify_pass, inplace=True)
                    r1.to_excel("user.xlsx", index=False)
                    msg1 = 'Password changed successfully'
                    return render_template('password.html', msg1=msg1)
                else:
                    msg2 = 'Re-entered password is not matched'
                    return render_template('password.html', msg2=msg2)
        else:
            msg3 = 'Incorrect password'
            return render_template('password.html', msg3=msg3)
    return render_template('password.html')


def encrypt(file):
    fo = open(file, "rb")
    img = fo.read()
    fo.close()
    img = bytearray(img)
    key = random.randint(0, 256)
    for index, value in enumerate(img):
        img[index] = value ^ key
    fo = open("enc.jpg", "wb")
    imageRes = "enc.jpg"
    fo.write(img)
    fo.close()
    return key, imageRes


def decrypt(key, file):
    fo = open(file, "rb")
    img = fo.read()
    fo.close()
    img = bytearray(img)
    for index, value in enumerate(img):
        img[index] = value ^ key
    fo = open("dec.jpg", "wb")
    imageRes = "dec.jpg"
    fo.write(img)
    fo.close()
    return imageRes


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('encrypt.html', title='Encrypt', year=datetime.now().year, message='Upload the image here')


@app.route('/about1', methods=['POST'])
def about1():
    if request.method == 'POST':
        global f
        f = request.files['file']
        f.save(f.filename)
        key, image = encrypt(f.filename)
        return render_template('encrypt_result.html', title='Encrypted', year=datetime.now().year,
                               message='This is your encrypted image', name=f.filename, keys=key, images=image)


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template('decrypt.html', title='Decrypt', year=datetime.now().year,
                           message='Upload your encrypted image along with the key')


@app.route('/contact1', methods=['POST'])
def contact1():
    if request.method == 'POST':
        global f
        f = request.files['file']
        f.save(f.filename)
        txt = request.form['key']
        key = int(txt)
        img = decrypt(key, f.filename)
        return render_template('decrypt_result.html', title='Decrypted', year=datetime.now().year,
                               message='This is your Decrypted image', name=f.filename)


@app.route('/return-file')
def return_file():
    return send_file("enc.jpg", attachment_filename="enc.jpg")


@app.route('/return-file1')
def return_file1():
    return send_file("dec.jpg", attachment_filename="dec.jpg")


@app.route('/logout')
def logout():
    session.clear()
    msg = 'You are now logged out', 'success'
    return render_template('login.html', msg=msg)


if __name__ == "__main__":
    app.run(port=5002, debug=True)
