from flask import Flask, request,jsonify, render_template
app = Flask(__name__, static_folder='../public/', static_url_path='/')


@app.route('/')
def resume_home():
    return app.send_static_file("index.html")




@app.route('/bank-app')
def resume_bank_app():
    return "Under construction!"


@app.route('/text_app')
def text_app():
    return "Under construction!"

