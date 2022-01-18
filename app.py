from flask import Flask, request,jsonify, render_template
import os
application = Flask(__name__,static_folder='dist', static_url_path='/')


@application.route('/')
def resume_home():
    return application.send_static_file("index.html")



@application.route('/vue')
def resume_vue_home():
    return application.send_static_file("vue_index.html")


@application.route('/bank-app')
def resume_bank_app():
    return "Under construction!"

@application.route('/split_check')
def split_check():
    return app.send_static_file("split_check.html")


@application.route('/text_app')
def text_app():
    return "Under construction!"


if __name__ =="__main__":
    # port = int(os.environ.get("PORT",8000))
    application.run(port = 5000, debug = True)

