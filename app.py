from flask import Flask
from flask import render_template
from flask import request, flash, redirect, url_for, jsonify

from threading import Thread


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

import subprocess
import time

@app.route("/filesize")
def get_file_sizes():
    result = subprocess.run(['ls', '-lh', '/appsvctmp/volatile/logs/runtime'], stdout=subprocess.PIPE)
    print(result.stdout)
    l = str(result.stdout).split('\\n')
    return jsonify(l)


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/output', methods =['POST'])
def output():
    size = request.form['size']

    Thread(target=generate_stdout, args=(int(size),)).start()

    flash(size + "mb will be written to stdout using a seperate thread")
    return redirect(url_for('index'))
    
def generate_stdout(size: int) -> None:
    """
    Size is in mb, prints in chunks of 1mb
    """
    mb = 1000000
    totalbytes = size * mb
    chuncks = totalbytes // mb
    s = "".join(['x' for x in range(mb)])
    for i in range(chuncks):
        print(s)
        print("1 mb written")
        time.sleep(1)
    
    

    print("Wrote " + str(totalbytes) + " bytes to stdout")
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')