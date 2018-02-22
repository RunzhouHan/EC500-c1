# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from HW1_API import main
from shutil import copyfile
app = Flask(__name__)

@app.route('/')
def firstpage():
    return render_template('index.html')
@app.route('/api')
def second():
    main()
    response = app.response_class(
       response = 'static/output.mp4',
       status = 200
    )
    #copyfile('/Users/rzhan/Desktop/EC500/output.mp4', '/Users/rzhan/Desktop/EC500/static/output.mp4')
    return response
if __name__ == '__main__':
    app.run()