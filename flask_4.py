import os
import urllib.request
# from app import app
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
import threading
from multiprocessing.pool import ThreadPool

app = Flask(__name__)

def encrypt_function(text,s):
    result = ""
    # traverse text
    for i in range(len(text)):
        char = text[i]
        if ord(char) in range(ord('A'), ord('Z')):
            result += chr((ord(char) + s-65) % 26 + 65)
        elif ord(char) in range(ord('a'),ord('z')):
            result += chr((ord(char) + s - 97) % 26 + 97)
        else:
            result += char
    print('encryption function completed')
    return result



@app.route('/multiple-files-upload', methods=['POST'])
def upload_file():
    uploaded_files = request.files.getlist("file")
    for file_name in uploaded_files:
        print(file_name.filename)

        file_name.save(f'/home/liril/Documents/Flask_22/{file_name.filename}')
        print('file saved')

        file1 = open(f'/home/liril/Documents/Flask_22/{file_name.filename}', 'r+')
        s = 25
        result_1 = ''
        for text_in_file in file1:
            pool = ThreadPool(processes=1)
            async_result = pool.apply_async(encrypt_function, (text_in_file, s))
            return_val = async_result.get()
            # print(async_result.get())
            result_1 += return_val

        with open(f'/home/liril/Documents/Flask_22/encrypted_{file_name.filename}', 'w+') as encrypted_file:
            encrypted_file.write(result_1)
        print(result_1)
    return 'Encryption completed'


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5055)



