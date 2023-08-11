from flask import Flask
from flask import render_template

app = Flask(__name__,template_folder="C:/Users/Public/OneDrive/Flask_app/templates")
#app.config['TEMPLATE_FOLDER'] = "C:/Users/Public/OneDrive/Flask_app/templates"


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
@app.route("/")
@app.route("/home")
def hello():
  return render_template('home.html',posts=posts)

@app.route("/about")
def about():
  return render_template('about.html',title="About")

if __name__ == "__main__":
  app.run(debug=True)