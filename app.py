from posixpath import dirname
from flask import Flask, request,jsonify, render_template
from dotenv import load_dotenv
from user_agents import parse
from contextlib import suppress
from flask_mysqldb import MySQL
import os, requests, ipinfo, logging.config,logging.handlers, sys
application = Flask(__name__,static_folder='dist', static_url_path='/')
dotenv_path = os.path.join(dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)
#setup logging
logger = None
logging_config = {
        'version':1,
        'disable_existing_loggers':False,
        'formatters':{
            'detailed':{
                'class': 'logging.Formatter',
                'format':'%(asctime)s-%(levelname)s-[%(filename)s:%(lineno)s] %(message)s',
                'datefmt':'%m-%d-%Y:%H:%M:%S',
            }
        },
        'handlers':{
            'file':{
                'level':'WARNING',
                'class':'logging.FileHandler',
                'filename':'resume.log',
                'mode':'a',
                'formatter':'detailed',
                

            },
            'console':{
                'level':'DEBUG',
                'class':'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'formatter':'detailed'
                
            }
        },
        'loggers':{
            'dev':{
                'handlers':['console'],
                'propagate':True,
            },
            'prod':{
                'handlers':['file'],
                'propagate':True,
            }
        },
    }
temp_file = logging_config['handlers']['file']['filename']
    #select loggers
if(not sys.gettrace()):
    #assume code doesn't run on debugger, its on production
    logging_config['handlers']['file']['filename'] = '/tmp/resume.log'
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger('prod')

else:
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger('dev')




#end of setup logging
application.config['MYSQL_HOST'] = os.environ.get('RDS_HOSTNAME')
application.config['MYSQL_USER'] = os.environ.get('RDS_USERNAME')
application.config['MYSQL_PASSWORD'] = os.environ.get('RDS_PASSWORD')
application.config['MYSQL_DB'] = os.environ.get('RDS_DB_NAME')
mysql = None
try:
    mysql = MySQL(application)
except Exception as ex:
    logger.exception("Couldn't create mysql connection.")
    logger.info(f"RDS_DB_NAME: {os.environ.get('RDS_DB_NAME')}")




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
    loc = "None"
    details = None

    user_agent = parse(request.headers.get('User-Agent'))
    visitors_table = os.environ.get('DATABASE_VISITORS_TABLE')
    #connect to database
    #use postgres
    url = os.environ.get('RDS_HOSTNAME')
    # conn = psycopg2.connect(
    #     host=os.environ.get('RDS_HOSTNAME'),
    #     database = os.environ.get('RDS_DB_NAME'),
    #     user=os.environ.get('RDS_USERNAME'),
    #     password=os.environ.get('RDS_PASSWORD')
    # )
    
    #using mysql
    # engine = create_engine(f"mysql://{os.environ.get('RDS_USERNAME')}:{os.environ.get('RDS_PASSWORD')}@{os.environ.get('RDS_HOSTNAME')}/{os.environ.get('RDS_DB_NAME')}",
    #                         encoding='utf8', echo=False)
    #make request to ipinfo
    ipinfo_token = os.environ.get('IPINFO_TOKEN')
    handler = ipinfo.getHandler(ipinfo_token)
    request_ip = request.access_route[0]
    #only insert ip that are public
    ip_parts = request_ip.split(".")

    if(ip_parts[0]=="172" and (16<=int(ip_parts[1]) <=31) ):
        return

    # logger.warning(request.access_route)
    try:
        details = handler.getDetails(request_ip)
    except Exception as ex:
        logger.exception("Couldn't connect to ipinfo service. Please Investigate.")
    language = request.accept_languages.best
    
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
    with suppress(AttributeError):
        loc = details.loc
    # end of ipinfo update
    data = {"ip": request_ip,
            "brow": user_agent.browser.family,
            "brow_ver": user_agent.browser.version_string,
            "language": language,
            "country": country,
            "region":region,
            "city":city,
            "postal":postal,
            "timezone":timezone
            }

    #upload data
    #using sqlalchemy
    # with engine.connect() as con:
    #     # cursor = conn.cursor()
    #     insert_query = text(f"""INSERT INTO {visitors_table} (ip_address, browser, brow_version, brow_language, country, region, city, postal_code, timezone) VALUES(:ip,:brow,:brow_ver, :language, :country, :region, :city, :postal, :timezone)""")
    #     con.execute(insert_query,data)
    try:
        with mysql.connection.cursor() as cur:
            
                cur.execute(f"""INSERT INTO {visitors_table} (ip_address, browser, brow_version, brow_language, country, region, city, postal_code, timezone, loc) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (request_ip,
                user_agent.browser.family,
                user_agent.browser.version_string,
                language,
                country,
                region,
                city,
                postal,
                timezone,
                loc))
                mysql.connection.commit()
    except Exception as ex:
         logger.exception("Couldn't insert into db")

    
    # using mysql
    

    
    


    # record_to_insert = (request.remote_addr, user_agent.browser.family, user_agent.browser.version_string, language, 
    # country,
    # region,
    # city,
    # postal,
    # timezone
    # )
    # cursor.execute(insert_query, record_to_insert)
    # conn.commit()
    # cursor.close()
    # conn.close()
    return




if __name__ =="__main__":
    # port = int(os.environ.get("PORT",8000))
    application.run(port = 5000, debug = True)

