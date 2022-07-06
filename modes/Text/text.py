import os
import get_coeff as comp
from PIL import Image, ImageEnhance
import stepic
import shutil
from flask import Blueprint, current_app, render_template, url_for, redirect, request, session, flash
# from datetime import timedelta
# from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

text = Blueprint("text", __name__, static_folder="static", template_folder="templates")

BLOCK_SIZE = 16
pad = lambda s: bytes(s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE), 'utf-8')
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


@text.route("/encode")
def text_encode():
    if os.path.exists(current_app.config['TEXT_CACHE_FOLDER']):
        shutil.rmtree(
            current_app.config['TEXT_CACHE_FOLDER'], ignore_errors=False)
    else:
        print("Not Found")

    if os.path.exists(os.path.join(current_app.config['UPLOAD_TEXT_FOLDER'], "encrypted_text_image.png")):
        # print("Found")
        os.remove(os.path.join(current_app.config['UPLOAD_TEXT_FOLDER'], "encrypted_text_image.png"))
    else:
        print("Not found")
    return render_template("encode.html")


@text.route("/encode-result", methods=['POST', 'GET'])
def text_encode_result():
    if request.method == 'POST':
        message = request.form['message']
        if 'file' not in request.files:
            flash('No image found')
        file = request.files['image']

        if file.filename == '':
            flash('No image selected')

        encrypted = encrypt(message)
        print(encrypted)
        key = encrypted[0]
        encrypted_msg = encrypted[1]
        print("key is:", key)
        print("encrypted message is:", encrypted_msg)

        h = hashlib.sha256()  # Construct a hash object using our selected hashing algorithm
        h.update(message.encode('utf-8'))  # Update the hash using a bytes object
        txt = h.hexdigest()  # Print the hash value as a hex string
        print("hashcode(digital signature):", txt)

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_TEXT_FOLDER'], filename))
            text_encryption = True
            encrypt_text(os.path.join(current_app.config['UPLOAD_TEXT_FOLDER'], filename), encrypted_msg)
        else:
            text_encryption = False
        result = request.form

        return render_template("encode-text-result.html", txt=txt, result=result, file=file, text_encryption=text_encryption, key=key, encrypted=encrypted_msg, message=message)
    return render_template("encode-text-result.html")


def encrypt(message):
    # private_key = hashlib.sha256(message.encode("utf-8")).hexdigest()
    private_key = hashlib.md5(message.encode("utf-8")).hexdigest()
    key = bytes(private_key, 'utf-8')
    raw = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return private_key, base64.b64encode(iv + cipher.encrypt(raw))


def decrypt(enc, key):
    print("started ---------------")
    print("key", key)
    print("type of key", type(key))
    print("enc", enc)
    print("type of enc", type(enc))
    enc = enc[2:-1]
    print("enc", enc)
    # private_key = bytes(key, 'UTF-8')
    enc1 = bytes(enc, 'UTF-8')
    print("enc", enc1)
    print("type of enc", type(enc1))
    enc = base64.b64decode(enc1)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))


@text.route("/decode")
def text_decode():
    return render_template("decode.html")


@text.route("/decode-result", methods=['POST', 'GET'])
def text_decode_result():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No image found')
        file = request.files['image']
        msg = request.form['message']
        key = request.form['key']
        print("Entered digital signature", msg)
        print("Entered key is", key)
        print(type(key))
        key = bytes(key, 'utf-8')
        print("Entered key is", key)
        print(type(key))

        # Decoding the text from image

        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_TEXT_FOLDER'], filename))
        text_decryption = True
        message = decrypt_text(os.path.join(current_app.config['UPLOAD_TEXT_FOLDER'], filename))
        print("Your decrypted message is:", message)

        # Decrypting the original text

        decrypted = decrypt(message, key)
        decrypted_msg = bytes.decode(decrypted)
        print("Your original message is:", decrypted_msg)

        # Finding digital signature for decrypted text

        h = hashlib.sha256()  # Construct a hash object using our selected hashing algorithm
        h.update(decrypted_msg.encode('utf-8'))  # Update the hash using a bytes object
        txt = h.hexdigest()  # Print the hash value as a hex string
        print(txt)

        # comparing the digital signatures

        if txt == msg:
            return render_template("decode-text-result.html", file=file, text_decryption=text_decryption, message=decrypted_msg)

        else:
            message = "Well tried mr.hacker Better luck next time ..."
            return render_template("decode-text-result.html", file=file, text_decryption=text_decryption, message=message)


def compress(file):
    # file = 'resident_1.jpg'
    print("Image compression started")
    # img = util.load_img(file)
    # img = Image.open(file)
    coefficient = comp.extract_rgb_coeff(file)
    image = comp.img_from_dwt_coeff(coefficient)
    comp_file = "Compressed_Images/compress" + '.jpg'
    image.save(comp_file)
    print("Image compression done")
    print("---------------------------")
    print("Image enhancement started")
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(2)
    file_enh = "Compressed_Images/enhanced" + '.jpg'
    image.save(file_enh)
    print("Image enhancement done")
    return file_enh


def encrypt_text(image_1, message):
    im = Image.open(image_1)
    img = compress(im)
    img = "Compressed_Images/enhanced" + '.jpg'
    img = Image.open(img)
    img.save(os.path.join(current_app.config['UPLOAD_TEXT_FOLDER'], "compressed_image.jpg"))
    im1 = stepic.encode(img, bytes(str(message), encoding='utf-8'))
    im1.save(os.path.join(current_app.config['UPLOAD_TEXT_FOLDER'], "encrypted_text_image.png"))

# Decryption function


def decrypt_text(image_1):
    im2 = Image.open(image_1)
    stegoImage = stepic.decode(im2)
    return stegoImage
