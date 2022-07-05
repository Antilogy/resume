from flask import Blueprint, Flask
from flask_mysqldb import MySQL
from flask import current_app as app
import json

import logging.config, logging.handlers, logging, os
'''This is my custom api for my resume app'''
api_bp = Blueprint('api_bp', __name__) # "API Blueprint"
mysql = None
logger = logging.getLogger()


# set the visitors table needed for sql
visitors_table = os.environ.get('DATABASE_VISITORS_TABLE')
@api_bp.route('/visitor_info')
def visitor():
    my_dict = {}
    # return three keys for browser, language, country
    code1 = 'Browser'
    code2 = 'Language'
    code3 = 'Country'
    my_dict[code1] = []
    my_dict[code2] = []
    my_dict[code3] = []
    try:
        
        # mysql = MySQL(app)
        mysql = app.mysql
        
        #return info from database connection here
        
        my_rows = None
        
        try:
            with mysql.connection.cursor() as cur:
                
                    cur.execute(f"""
                    (select 'Browser' as ip_info, 0 as total
                    from {visitors_table}
                    limit 1)
                    union
                    (select coalesce(browser,'No Browser') as ip_info, count(*) as total
                    from {visitors_table} 
                    where timestamp >= (Date(now()) - interval 7 day) group by browser limit 100)
                    union
                    (select 'Language', 0
                    from {visitors_table} 
                    limit 1)
                    union
                    (select coalesce(brow_language, 'No Language') as ip_info, count(*) as total 
                    from {visitors_table}
                    where timestamp >= Date(now()) - interval 7 day group by brow_language limit 100)
                    union 
                    (select 'Country', 0
                    from {visitors_table}
                    limit 1)
                    union
                    (select coalesce(country, 'No Country') as ip_info, count(*) as total
                    from {visitors_table} 
                    where timestamp >= Date(now()) - interval 7 day group by country limit 100)""",
                    )
                    my_rows = cur.fetchall()
                    #identify the browser
                    #identify the language
                    #identify the country
                    for row in my_rows:
                        # row [column_index]
                        #set the column label
                        #and skip the last row
                        if(row[0] == code1):
                            column_flag = code1
                            continue
                        elif(row[0] == code2):
                            column_flag = code2
                            continue
                        elif(row[0] == code3):
                            column_flag = code3
                            continue

                        my_dict[column_flag].append(f'{row[0]}:{row[1]}')
                        

                    mysql.connection.commit()
        except Exception as ex:
            logger.exception("Couldn't connect to db")
    except Exception as ex:
        logger.exception("Couldn't create mysql connection.")
        logger.exception(f"RDS_DB_NAME: {os.environ.get('RDS_DB_NAME')}")    
    return json.dumps(my_dict)