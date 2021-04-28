from flask import Flask, request,jsonify, render_template
app = Flask(__name__)


@app.route('/')
def resume_home():
    return render_template("index.html")




@app.route('/bank-app')
def resume_bank_app():
    return "Under construction!"


@app.route('/text_app')
def text_app():
    return "Under construction!"

