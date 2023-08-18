from flask import Flask
from flask_restful import Resource,Api, reqparse
import psycopg2
from psycopg2.extras import DictCursor
import datetime
app = Flask(__name__)
api = Api(app)
class GetTableDetails(Resource):
    def __init__(self,pwd, tablename,schemaname):
        super().__init__()
        self.connection = psycopg2.connect(database= 'postgres',user= 'postgres', password= pwd, host = 'localhost',port= '5432')
        self.tablename = tablename
        self.schemaname = schemaname
        self.putargs = reqparse.RequestParser();
        

    def tabledetails(self):
        
        curs = self.connection.cursor()

        tabledetails = "SELECT column_name,data_type from information_schema.columns WHERE table_schema = %s AND table_name = %s "
        curs.execute(tabledetails,(self.schemaname,self.tablename))
        columns = curs.fetchall()
        collist = [{"columnname":name,"datatype":dattype}for name,dattype in columns]
        return  collist
    
    def querytable(self,colname, queryval,collist):
        curs = self.connection.cursor()

        colstring = ",".join([i["columnname"] for i in collist])

        querystring = f"SELECT {colstring} FROM {self.schemaname}.{self.tablename} WHERE {colname} = %s"

        curs.execute(querystring, (queryval,))
        filterresult = curs.fetchall()

        colnames = [x['columnname'] for x in collist]
        result = [{col: (value.isoformat() if isinstance(value, datetime.date) else value) for col, value in zip(colnames, row)} for row in filterresult]
        return result, 200
    def inserttotable(self,columns, values):
        curs = self.connection.cursor()
        # for val in columns:
        #     if val not in collist:
        #         print(f"The column {val} does not exist in the table")
        #         return

        colstring = ",".join(columns);
        valuestring = ",".join(["%s"] * len(values));
        insertstr = f"""INSERT INTO {self.schemaname}.{self.tablename} ({colstring}) 
                        VALUES ({valuestring}) 
                        RETURNING *"""

        curs.execute(insertstr,values)
        insertresult = curs.fetchall()
        self.connection.commit()
        
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