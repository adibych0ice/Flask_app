import psycopg2

db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'Tachyon_9667',
    'host': 'localhost',
    'port': '5432'
}

conn = psycopg2.connect(**db_params)

# Create a cursor object
cur = conn.cursor()


with open('C:/Users/adity/Downloads_None_OneDrive/load_departments.sql', 'r') as f:
    sql_script = f.read()
cur.execute(sql_script)
conn.commit()
cur.close()
conn.close()