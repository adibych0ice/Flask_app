from flask import Flask, render_template

app = Flask(__name__,template_folder="C:/Users/Public/OneDrive/Flask_app/templates",static_folder="C:/Users/Public/OneDrive/Flask_app/static")

@app.route('/')
def home():
    return render_template('testlayout.html')
@app.route("/about")
def about():
  return render_template('testabout.html',title="About")
if __name__ == '__main__':
   app.run(debug=True)