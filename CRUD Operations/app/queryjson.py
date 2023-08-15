import json
import getpass
import psycopg2
import re

with open('C:/Users/Public/OneDrive/Flask_app/CRUD Operations/Schema_and_Table.json','r') as jsonfile:
    jsondat = json.load(jsonfile)
colnameall = [x['name'] for x in jsondat['columns']]
schemaname = jsondat['schema']
tabname = jsondat['table']
conn = psycopg2.connect(database = 'postgres',user='postgres',password='Tachyon_9667', host='localhost',port='5432')
cursor = conn.cursor()
cursor.execute(""" SELECT column_name FROM information_schema.columns WHERE table_schema=%s AND table_name=%s""",(schemaname,tabname))
colrsult = cursor.fetchall()
columns = [column[0] for column in colrsult]
while True:
    attribute = input("Enter the name of the attribute you wish to filter by: ") 

    if attribute in columns:
        break
    
    else:
        print(f"The attribute {attribute} does not exist in the table {tabname}. Please enter a valid attribute.")

#Now doing the filtering of the code

# dattype = [x['type'] for x in jsondat['columns']]


# #For validating if the input actually matches the 
# regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
# conditions = [

#     (lambda x: x != "", "Value cannot be empty"),
#     (lambda x: x.isdigit(), "Value has to be a digit")
# ]

# def validateinput():
#     dattypes = [r['type'] for r in jsondat['columns']]
#     for i in jsondat['columns']:
#         if i['name'] == attribute:
#             datatype = i['type']



while True:
    atrrval = input("Enter the value you need to filter by: ")
    curstr = f"SELECT {','.join(colnameall)} FROM {schemaname}.{tabname} WHERE {attribute} = %s"
    cursor.execute(curstr, (atrrval,))
    queryresult=cursor.fetchall()
    if queryresult:
        print(queryresult)
        break
    else:
        print(f" The value {atrrval} does not exist in the attribute {attribute}. Enter a valid value")
        
# filterval = input("Enter the value for filtering: ")


