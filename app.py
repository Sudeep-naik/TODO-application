from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///list.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Dolist(db.Model):
    slno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.slno}----{self.title}"

@app.route('/')
def home():
    alltodo=Dolist.query.all()
    return render_template("/index.html",alltodo=alltodo)    

@app.route("/add", methods=['GET','POST'])
def add():
    if request.method=='POST':
        title=request.form["title"]
        desc=request.form["desc"]
        todo=Dolist(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
        #this snippet will add the current data into the database when refreshed in order to avoid that we will redirect to home page and
        #from there we can display as show below
    # alltodo=Dolist.query.all()
    # return render_template("index.html")                   
    return redirect(url_for("home"))

@app.route("/update/<int:slno>",methods=["GET","POST"])
def update(slno):
    if request.method=="POST":
        title=request.form["title"]
        desc=request.form["desc"]
        todo=Dolist.query.filter_by(slno=slno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("home"))
    todo=Dolist.query.filter_by(slno=slno).first()
    return render_template("update.html",todo=todo)

@app.route("/delete/<int:slno>")
def delete(slno):
    todo=Dolist.query.filter_by(slno=slno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))
    
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist
    app.run(debug=True)


