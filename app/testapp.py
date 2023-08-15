from flask import Flask, render_template, url_for, jsonify, request
import json
import psycopg2
import sys

#from forms import registrationform,loginform
sys.path.append('C:/Users/Public/OneDrive/Flask_app/CRUD Operations/app')


import queryjson
from queryjson import queryjsondat

app = Flask(__name__,template_folder="C:/Users/Public/OneDrive/Flask_app/templates",static_folder="C:/Users/Public/OneDrive/Flask_app/static")

app.config['SECRET_KEY'] = 'f005dcccf0384a50035aae485cd58f30'

posts = [
    {
        "title": "My First Blog Post",
        "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce interdum lacus eget metus blandit, sit amet pellentesque lectus pellentesque. Donec vestibulum lacinia dui id finibus. Nunc eu risus sit amet dolor posuere malesuada quis ut tortor.",
        "author": "John Doe", 
        "date": "2022-01-01"
    },
    {   
        "title": "How to Make Pancakes",      
        "content": "In a large bowl, sift together the flour, baking powder, salt and sugar. Make a well in the center and pour in the milk, egg and melted butter; mix until smooth. Heat a lightly oiled griddle or pan over medium-high heat. Pour or scoop the batter onto the griddle, using approximately 1/4 cup for each pancake. Brown on both sides and serve hot.",
        "author": "Jane Doe",
        "date": "2022-02-15"
    },
    {
        "title": "My Favorite Books",
        "content": "Aliquam sodales, ipsum vel tristique porta, dui massa rhoncus dolor, sed fringilla velit enim id nibh. Donec tincidunt dictum lacus rutrum congue. Cras mattis a nunc nec porttitor. Morbi lectus turpis, gravida in magna sit amet, semper varius eros.",
        "author": "Bob Smith",
        "date": "2022-03-01"
    }
]


def querytablejson():

    with open('C:/Users/Public/OneDrive/Flask_app/Schema_JSON.json', 'r') as file:
        data = json.load(file)

    columns = data['columns']

    schemadef = data['schema']
    temp = ','.join([j['name'] for j in columns])
    tempstr = f"""SELECT {temp} FROM {schemadef} LIMIT 100"""
    return tempstr

@app.route('/')
@app.route('/home')
def home():
    return render_template('testhome.html',posts=posts)

@app.route("/about")
def about():
  return render_template('testabout.html',title="About")

@app.route('/query_table', methods=['GET'])
def querytable():
    sqlquery = querytablejson()

    conn = psycopg2.connect(database="postgres", user="postgres", password="Tachyon_9667", host="localhost", port="5432")
    curs = conn.cursor()
    curs.execute(sqlquery)
    results = curs.fetchall()
    conn.close()

    columns = [j['name'] for j in json.load(open('C:/Users/Public/OneDrive/Flask_app/Schema_JSON.json', 'r'))['columns']]
    results_dict = [dict(zip(columns, row)) for row in results]
    return render_template('query_results.html', results=results_dict, columns=columns)
#@app.route("/register")
#def register():
#   form = registrationform()
#   return render_template('register.html',title='Register',form=form)

#@app.route("/login")
#def login():
#   form = loginform()
#   return render_template('login.html',title='Login',form=form)


@app.route('/api/upload', methods=['POST'])
def queryjsondata():
    jsondata = request.json

    result, error = queryjsondat(jsondata) 


    if error:
        return jsonify({"error":error}),400
    
    return jsonify(result), 200

if __name__ == '__main__':
   app.run(debug=True)