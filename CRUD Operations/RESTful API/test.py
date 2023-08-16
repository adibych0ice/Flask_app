from flask import Flask
from flask_restful import Resource,Api
import psycopg2
from psycopg2.extras import DictCursor
import datetime
from flask import jsonify
app = Flask(__name__)

def tabledetails(pwd,tablename,schemaname,tabname,colname,queryval):
        
        conn = psycopg2.connect(database = 'postgres',user='postgres',password=pwd, host='localhost',port='5432')
        curs = conn.cursor()

        tabledetails = "SELECT column_name,data_type from information_schema.columns WHERE table_schema = %s AND table_name = %s "
        curs.execute(tabledetails,(schemaname,tablename))
        columns = curs.fetchall()
        collist = [{"columnname":name,"datatype":dattype}for name,dattype in columns]

        curs = conn.cursor(cursor_factory=DictCursor)

        colstring = ",".join([i["columnname"] for i in collist])

        querystring = f"SELECT {colstring} FROM {schemaname}.{tabname} WHERE {colname} = %s"

        curs.execute(querystring, (queryval,))
        filterresult = curs.fetchall()
        # result = []
        # for row in filterresult:
        #     row_dict = {}
        #     for i, col in enumerate(collist):
        #         value = row[i]
        #         if isinstance(value, datetime.date):
        #             value = value.isoformat()
        #         row_dict[col["columnname"]] = value
        #     result.append(row_dict)
        colnames = [x['columnname'] for x in collist]
        result = [{col: (value.isoformat() if isinstance(value, datetime.date) else value) for col, value in zip(colnames, row)} for row in filterresult]
        return result, 200

result, stat_code = tabledetails("Tachyon_9667","users","decistech","users","email","ajackson@example.net")

print(result)