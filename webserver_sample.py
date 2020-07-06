from datetime import datetime
from flask import Flask, send_file
import random
import os
from os import path

app = Flask(__name__, template_folder='templates',
                    static_folder='static')

@app.route('/file')
def hello_world(request=None):
    try:
        root = path.dirname(path.abspath(__file__))
        filename ="/tmp/output.txt"
        with open(filename, "w+") as f:
            f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\r\n')
            ran = random.randint(0, 1000)
            for i in range(ran, ran + 10):
                f.write("This is line %d\r\n" % (i+1))
            f.close()
            return send_file(filename, attachment_filename='output.txt')
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    # defining server ip address and port
    app.run(host='0.0.0.0',port='5000', debug=True)