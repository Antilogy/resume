from posixpath import dirname
from flask import Flask, request,jsonify, render_template
from dotenv import load_dotenv
from user_agents import parse
from contextlib import suppress
import os, psycopg2, requests, ipinfo, asyncio
application = Flask(__name__,static_folder='dist', static_url_path='/')
dotenv_path = os.path.join(dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)
#only save ip address info for clients that visit the homepage
@application.route('/')
def resume_home():
    save_ip_info()
    return application.send_static_file("index.html")



@application.route('/vue')
def resume_vue_home():
    return application.send_static_file("vue_index.html")


@application.route('/bank-app')
def bank_app():
    return "Under construction!"

@application.route('/split_check')
def split_check():
    return application.send_static_file("split_check.html")


@application.route('/text_app')
def text_app():
    return "Under construction!"

#save client data

def save_ip_info():
    """Save client data
    """
    country = "None"
    region = "None"
    city = "None"
    postal = "None"
    timezone = "None"


    user_agent = parse(request.headers.get('User-Agent'))
    visitors_table = os.environ.get('DATABASE_VISITORS_TABLE')
    #connect to database
    url = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(
        host=os.environ.get('DATABASE_URL'),
        database = os.environ.get('DATABASE'),
        user=os.environ.get('DATABASE_USER'),
        password=os.environ.get('DATABASE_PASSWORD')
    )
    #make request to ipinfo
    ipinfo_token = os.environ.get('IPINFO_TOKEN')
    handler = ipinfo.getHandler(ipinfo_token)
    details = handler.getDetails(request.remote_addr)
    
    # update default info with ipinfo
    with suppress(AttributeError):
        country = details.country
    with suppress(AttributeError):
        region = details.region
    with suppress(AttributeError):
        city = details.city
    with suppress(AttributeError):
        postal = details.postal
    with suppress(AttributeError):
        timezone = details.timezone
    # end of ipinfo update


    #upload data
    cursor = conn.cursor()
    insert_query = f"""INSERT INTO {visitors_table} (ip_address, browser, brow_version, brow_language, country, region, city, postal_code, timezone) VALUES(%s,%s,%s, %s, %s, %s, %s, %s, %s)"""
    language = request.accept_languages.best
    
    
    


    record_to_insert = (request.remote_addr, user_agent.browser.family, user_agent.browser.version_string, language, 
    country,
    region,
    city,
    postal,
    timezone
    )
    cursor.execute(insert_query, record_to_insert)
    conn.commit()
    cursor.close()
    conn.close()
    return




if __name__ =="__main__":
    # port = int(os.environ.get("PORT",8000))
    application.run(port = 5000, debug = True)

