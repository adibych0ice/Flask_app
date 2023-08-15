import json
import psycopg2
#Opening the JSON


def queryjsondat(jsondata):
    schemaname = jsondata['schema']
    tabname = jsondata['table']

    #Connecting to DB
    conn = psycopg2.connect(database = 'postgres',user='postgres',password='Tachyon_9667', host='localhost',port='5432')
    cursor = conn.cursor()
    cursor.execute(""" SELECT column_name FROM information_schema.columns WHERE table_schema=%s AND table_name=%s""",(schemaname,tabname))
    colrsult = cursor.fetchall()
    columns = [column[0] for column in colrsult]
    attribute = jsondata['attribute']
    atrrval = jsondata['attributevalue']
    
    if attribute not in columns:
        return None, f"The attribute {attribute} does not exist in the table {tabname}"
    
    curstr = f"SELECT {','.join(columns)} FROM {schemaname}.{tabname} WHERE {attribute} = %s"
    cursor.execute(curstr, (atrrval,))
    queryresult=cursor.fetchall()
    if queryresult:
        return queryresult,None
        
    else:
        return None,f" The value {atrrval} does not exist in the attribute {attribute}. Enter a valid value"
        
# filterval = input("Enter the value for filtering: ")


