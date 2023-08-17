from flask import Flask
from flask_restful import Resource,Api
import psycopg2
from psycopg2.extras import DictCursor
import datetime
app = Flask(__name__)
api = Api(app)
class GetTableDetails(Resource):


    def tabledetails(self,pwd,tablename,schemaname):
        
        conn = psycopg2.connect(database = 'postgres',user='postgres',password=pwd, host='localhost',port='5432')
        curs = conn.cursor()

        tabledetails = "SELECT column_name,data_type from information_schema.columns WHERE table_schema = %s AND table_name = %s "
        curs.execute(tabledetails,(schemaname,tablename))
        columns = curs.fetchall()
        collist = [{"columnname":name,"datatype":dattype}for name,dattype in columns]
        return  collist, conn
    
    def querytable(self,schemaname,colname, queryval,conn,collist,tabname):
        curs = conn.cursor(cursor_factory=DictCursor)

        colstring = ",".join([i["columnname"] for i in collist])

        querystring = f"SELECT {colstring} FROM {schemaname}.{tabname} WHERE {colname} = %s"

        curs.execute(querystring, (queryval,))
        filterresult = curs.fetchall()

        colnames = [x['columnname'] for x in collist]
        result = [{col: (value.isoformat() if isinstance(value, datetime.date) else value) for col, value in zip(colnames, row)} for row in filterresult]
        return result, 200
    def inserttotable(self,columns, values, connection,schemaname,tablename,collist):
        curs = connection.cursor()
        # for val in columns:
        #     if val not in collist:
        #         print(f"The column {val} does not exist in the table")
        #         return

        colstring = ",".join(columns);
        valuestring = ",".join(["%s"] * len(values));
        insertstr = f"""INSERT INTO {schemaname}.{tablename} ({colstring}) 
                        VALUES ({valuestring}) 
                        RETURNING *"""

        curs.execute(insertstr,values)
        insertresult = curs.fetchall()
        connection.commit()
        
        return insertresult,200


    def get(self, password,tablename,schemaname,columnname,colfilter):
        columnlist, connection = self.tabledetails(password,tablename,schemaname)
        filterresult, statcode = self.querytable(schemaname,columnname,colfilter,connection,columnlist,tablename)

        return filterresult,statcode


    def put(self,password,tablename,schemaname):
        collist,connection = self.tabledetails(password,tablename,schemaname)
        insertresult,statcode = self.inserttotable(['name','email','address','birthdate'],['Andrew Kazinsky','freddy@reddit.org','123 Maple Street, Suite 200, Springfield, IL 62701','08-07-1991'],connection,schemaname,tablename,collist)

        return insertresult,statcode
         
#The <> is to pass the paramater that will be passed when pinging the endpoint
api.add_resource(GetTableDetails,'/tabdetails/<string:password>/<string:tablename>/<string:schemaname>/<string:columnname>/<string:colfilter>')


if __name__ == "__main__":
    app.run(debug=True)