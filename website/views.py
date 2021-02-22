import base64
import io

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import matplotlib.pyplot as plt
import mplfinance as mpf

#file stuff
import os
from os.path import join, dirname, realpath
from flask import send_file, send_from_directory, safe_join, abort

#yahoo finance / pandas
from pandas_datareader import data as pdr
import yfinance as yf

views = Blueprint('views', __name__)
# views=Flask(__name__)

@views.route('/', methods=['GET', 'POST'])
def home():
#
    if request.method == 'POST':
        print("success")

    return render_template("home.html")


@views.route('/finance', methods=['POST', 'GET'])
def finance_landing():
    if request.method == 'POST':
        pass
    return render_template("finance.html")    

@views.route('/submittedfinance', methods=['POST', 'GET'])
def get_ticker():
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        print(ticker)
        yf.pdr_override() # <== that's all it takes :-)

        # download dataframe
        # data = pdr.get_data_yahoo("SPY", start="2017-01-01", end="2017-04-30")
        data = pdr.get_data_yahoo(ticker)

        # show this on html template, use DF for plotting.
        disp_data = data.tail(10)

        print("successful")
        print(disp_data)

        # data_index = data.index
        # print(data_index)

        # create image and pass to submitted_finance html template.
        img = io.BytesIO()
        plt.figure(figsize=(10, 10))
        # plt.plot(data.index, data['Close'])
        # plt.xlabel("date")
        # plt.ylabel("$ price")
        mpf.plot(data, type='candle', volume=True,
                 savefig=img,
                 title=f'\n{ticker.upper()} Historical Data',
                 ylabel_lower='Shares\nTraded')
        plt.title(f'{ticker} Stock Price:')

        plt.savefig(img, format='png')
        img.seek(0)

        plot_url = base64.b64encode(img.getvalue()).decode()


    return render_template("submittedfinance.html",
                           disp_data=disp_data.to_html(classes=["table-bordered", "table-striped", "table-hover"]),
                           plot_url=plot_url,
                           ticker=ticker.upper())









@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/design', methods=['GET'])
def design():
    return render_template("design.html")

@views.route('/guide', methods=['GET'])
def guide():
    return render_template("guide.html")             




# Upload folder
# UPLOAD_FOLDER = 'static/files'
# app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

@views.route('/submitted', methods=['POST','GET'])
def submit_info():
    if request.method == 'POST':
        print(request)
        message = request.form.get('options')
        print("selected unit is:")
        print(message)

        filename = request.form.get('col_elem')
        print(filename)

        output_vals = []

        #print all the values posted from design.html
        for key, val in request.form.items():
            #print(key,val)
            print(key, val)     
            output_vals.append(val)

        # uploaded_file=request.files['file']
        # if uploaded_file.filename !='':
        #     file_path = os.path.join(views.config['UPLOAD_FOLDER'],uploaded_file.filename)
        #     uploaded_file.save(file_path)            
              
        length=len(output_vals)
        print(length)             
    
    return render_template("submitted.html", output=output_vals, length=length)    