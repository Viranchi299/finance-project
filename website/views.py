import json
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import current_user

from . import db
from .models import Note
# file stuff
from .ticker_parsing import get_ticker_data, plot_ticker_data

views = Blueprint('views', __name__)
WEEKLY_TRADING_DAYS = 5
YEARLY_TRADING_DAYS = 250


# urllib.request.urlretrive()


# views=Flask(__name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print("success")

    return render_template("home.html")


@views.route('/finance', methods=['POST', 'GET'])
def finance_landing():
    if request.method == 'POST':
        pass
    return render_template("finance.html")


# alternative using API and amCharts
@views.route('/amcharts', methods=['POST', 'GET'])
def amCharts():
    if request.method == 'POST':
        pass
    test_array = [1, 2, 3, 4]  # test to try pass into amcharts page via index.js
    return render_template("amcharts.html", test_array=test_array)


@views.route('/submittedfinance', methods=['POST'])
def display_ticker_data():
    ticker_name = request.form.get('ticker')
    ticker_data = get_ticker_data(ticker_name)
    if not ticker_data:
        flash('No data for this ticker')
        return redirect(url_for('views.finance_landing'))

    trading_data, ticker_props = ticker_data['trading_data'], ticker_data['properties']
    # show this on html template, use DF for plotting 2 weeks of trading data.
    disp_data = trading_data.tail(WEEKLY_TRADING_DAYS * 2)

    # get plot for trading data
    plot_image = plot_ticker_data(trading_data, ticker_name)
    return render_template("submittedfinance.html",
                           disp_data=disp_data.to_html(classes=["table-bordered", "table-striped", "table-hover"]),
                           plot_image=plot_image, ticker=ticker_name.upper(), **ticker_props.info)


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

@views.route('/submitted', methods=['POST', 'GET'])
def submit_info():
    if request.method == 'POST':
        print(request)
        message = request.form.get('options')
        print("selected unit is:")
        print(message)

        filename = request.form.get('col_elem')
        print(filename)

        output_vals = []

        # print all the values posted from design.html
        for key, val in request.form.items():
            # print(key,val)
            print(key, val)
            output_vals.append(val)

        # uploaded_file=request.files['file']
        # if uploaded_file.filename !='':
        #     file_path = os.path.join(views.config['UPLOAD_FOLDER'],uploaded_file.filename)
        #     uploaded_file.save(file_path)            

        length = len(output_vals)
        print(length)

    return render_template("submitted.html", output=output_vals, length=length)
