from flask import Flask, render_template      

app = Flask(__name__)

@app.route("/")
def about():
    return render_template("about.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")


@app.route("/home")
def home():
    return render_template("home.html")

    

    
if __name__ == "__main__":
    app.run(debug=True)
  