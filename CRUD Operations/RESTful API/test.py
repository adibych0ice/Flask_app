from flask import Flask
from flask_restful import Resource,Api
import psycopg2
from psycopg2.extras import DictCursor
import datetime
from flask import jsonify
app = Flask(__name__)

def tabledetails(pwd,tablename,schemaname,tabname,colname,queryval,cols,values):
        
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
        
        # for val in cols:
        #     if val not in collist['columnname']:
        #         print(f"The column {val} does not exist in the table")
        #         return None,None,404
        colstring = ",".join(cols)
        placeholders = ",".join(["%s"] * len(values))

        insertstr = f"""INSERT INTO {schemaname}.{tablename} ({colstring}) 
                        VALUES ({placeholders})
                        RETURNING * """
        
        curs.execute(insertstr,values)
        insertresult = curs.fetchall()
        return result, insertresult,200

result, insertresult, stat_code = tabledetails("Tachyon_9667","users","decistech","users","email","ajackson@example.net",['name','email','address','birthdate'],['Timothy Gartner','timg@example.org','123 Maple Street, Suite 200, Springfield, IL 62701','08-05-1994'])

print(result)
print(insertresult)