from flask import Flask, request,jsonify, render_template
import os
app = Flask(__name__,static_folder='dist', static_url_path='/')


@app.route('/')
def resume_home():
    return app.send_static_file("index.html")



@app.route('/vue')
def resume_vue_home():
    return app.send_static_file("vue_index.html")


@app.route('/bank-app')
def resume_bank_app():
    return "Under construction!"

@app.route('/split_check')
def split_check():
    return app.send_static_file("split_check.html")


@app.route('/text_app')
def text_app():
    return "Under construction!"


if __name__ =="__main__":
    port = int(os.environ.get("PORT",8000))
    app.run(host='0.0.0.0',port = port)

