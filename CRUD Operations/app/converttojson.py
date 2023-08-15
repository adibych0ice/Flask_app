import psycopg2
import getpass
import json

try:
    pwd = getpass.getpass()
    conn = psycopg2.connect(database = 'postgres',user='postgres',password=pwd, host='localhost',port='5432')
    curs = conn.cursor()

    #Checking if the schema actually exists
    while True:
        schema = input("Enter the Schema Name: ")
        curs.execute("SELECT schema_name from information_schema.schemata WHERE schema_name = %s",(schema,))
        result_schema = curs.fetchone()

        if result_schema:
            #print(f"The Schema {result_schema[0]} exists")
            break
        else:
            print(f"The Schema {schema} does not exist. Please enter a valid schema.")
    
    #Checking if the table exists
    while True:
        tablename = input("Enter the name of the Table: ")
        tblsqlcheck = f""" SELECT EXISTS(SELECT 1 FROM pg_tables WHERE schemaname = %s AND tablename = %s) """
        curs.execute(tblsqlcheck, (schema,tablename))
        result_table = curs.fetchone()

        if result_table[0]:
            #print(f"The Table {tablename} exists")
            break
        else:
            print(f"The Table {tablename} does not exist")    
    #Now listing the columns in the table
    columndatstr = """ SELECT column_name, data_type FROM information_schema.columns WHERE table_schema=%s AND table_name=%s """
    curs.execute(columndatstr,(schema,tablename))  
    colnamedattypes = curs.fetchall()

    # for column_name, data_type in colnamedattypes:
    #     print(f"  - {column_name}: {data_type}")  
    cldictlist = [{"name":colname,"type":dattype} for colname,dattype in colnamedattypes]
    jsondict = {"schema":schema,"table":tablename}
    jsondict['columns'] = cldictlist
    # print(cldictlist)
    with open('Schema_and_Table.json','w') as jsonfile:
        json.dump(jsondict,jsonfile,indent=4)
except psycopg2.Error as e:
    print(f"An error occurred while connecting to the database or checking the schema: {e}")

finally:
    # Close the cursor and the connection, if they were successfully created
    if 'curs' in locals():
        curs.close()
    if 'conn' in locals():
        conn.close()